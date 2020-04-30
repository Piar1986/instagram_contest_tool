import argparse
import os
import re
from instabot import Bot
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser(description='Инструмент для конкурсов в Instagram')
    parser.add_argument('--post_link', help='Ссылка на пост', type=str)
    parser.add_argument('--post_author', help='Автор поста', type=str)
    return parser


def get_user_mention(comment_text):
    # https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
    result = re.findall("(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)", comment_text)
    return result


def is_user_exist(username):
    return bot.get_user_id_from_username(username) is not None


def get_comments_with_friend(comments):
    comments_with_friend = []
    for comment in comments:
        usernames = get_user_mention(comment['text'])
        for username in usernames:
            if is_user_exist(username):
                comment_user_id = int(comment['user_id'])
                comment_username = comment['user']['username']
                comments_with_friend.append((comment_user_id, comment_username))
    return comments_with_friend


def get_comments_with_friend_like(post_likers_users, comments):
    comments_with_friend_like = []
    for comment in comments:
        for liker in post_likers_users:
            liker_id = int(liker)
            comment_user_id = comment[0]
            if liker_id==comment_user_id:
                comments_with_friend_like.append(comment)
    return comments_with_friend_like


def get_comments_with_friend_like_follow(follower_users, comments):
    comments_with_friend_like_follow = []
    for comment in comments:
        for user in follower_users:
            folower_id = int(user)
            comment_user_id = comment[0]
            if folower_id==comment_user_id:
                comments_with_friend_like_follow.append(comment)
    return comments_with_friend_like_follow


def show_winners(winners):
    for winner in winners:
        winner_username = winner[1]
        print(winner_username)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if not args.post_link:
        exit('Введите ссылку на пост')

    if not args.post_author:
        exit('Введите Instagram логин автора поста')

    load_dotenv()
    login = os.getenv("INSTAGRAM_LOGIN")
    password = os.getenv("INSTAGRAM_PASSWORD")
    bot = Bot()
    bot.login(username=login, password=password)
    
    media_id = bot.get_media_id_from_link(args.post_link)
    comments = bot.get_media_comments_all(media_id)
    post_likers_users = bot.get_media_likers(media_id)
    follower_users = bot.get_user_followers(args.post_author)
    
    comments_with_friend = get_comments_with_friend(comments)
    comments_with_friend_like = get_comments_with_friend_like(post_likers_users, comments_with_friend)
    comments_with_friend_like_follow = get_comments_with_friend_like_follow(follower_users, comments_with_friend_like)
    
    winners = set(comments_with_friend_like_follow)
    show_winners(winners)