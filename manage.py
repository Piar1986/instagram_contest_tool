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


def get_users_mentions(comment_text):
    # https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
    result = re.findall(r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)', comment_text)
    return result


def is_user_exist(username):
    return bot.get_user_id_from_username(username) is not None


def get_username(user_id):
    return bot.get_username_from_user_id(user_id)


def get_comments_with_friend_users_ids(comments):
    comments_with_friend_users_ids = []
    for comment in comments:
        comment_text = comment['text']
        usernames = get_users_mentions(comment_text)
        for username in usernames:
            if is_user_exist(username):
                comment_user_id = str(comment['user_id'])
                comments_with_friend_users_ids.append(comment_user_id)
    return comments_with_friend_users_ids


def show_winners_usernames(winners):
    print('Участники, выполнившие условия конкурса:')
    for winner in winners:
        winner_username = get_username(winner)
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
    
    post_media_id = bot.get_media_id_from_link(args.post_link)
    post_comments = bot.get_media_comments_all(post_media_id)
    
    comments_with_friend_users_ids = get_comments_with_friend_users_ids(post_comments)
    post_likers_users_ids = bot.get_media_likers(post_media_id)
    followers_users_ids = bot.get_user_followers(args.post_author)
        
    comments_with_friend_users_ids_set = set(comments_with_friend_users_ids)
    post_likers_users_ids_set = set(post_likers_users_ids)
    followers_users_ids_set = set(followers_users_ids)

    winners_users_ids = comments_with_friend_users_ids_set & post_likers_users_ids_set & followers_users_ids_set
    show_winners_usernames(winners_users_ids)