#!/usr/bin/python

import datetime
import json
import os.path

import requests
from bs4 import BeautifulSoup

cookies = {
    '_ym_uid': '1653764274471504054',
    '_ym_d': '1653764274',
    'habr_web_home_feed': '/all/',
    'hl': 'ru',
    'fl': 'ru',
    '_ga': 'GA1.2.1631445463.1653764275',
    'visited_articles': '715134:717556:71839:656609:716434:713992:508192:716394:493852',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.8 Chrome/87.0.4280.144 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'DNT': '1',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    # 'Cookie': '_ym_uid=1653764274471504054; _ym_d=1653764274; habr_web_home_feed=/all/; hl=ru; fl=ru; _ga=GA1.2.1631445463.1653764275; visited_articles=715134:717556:71839:656609:716434:713992:508192:716394:493852',
}


def lookup():
    page = 1
    all_posts = []
    cur_datetime = datetime.datetime.now()

    delta_time = datetime.timedelta(days=1, minutes=30)

    exit_program = False
    while True:
        if not exit_program:
            req = requests.get(f"https://habr.com/ru/all/page{page}", cookies=cookies, headers=headers)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')

            try:
                articles = soup.find_all("article")
                for article in articles:
                    try:
                        post_time = article.find('time').get('title')
                        post_time = datetime.datetime.strptime(post_time, '%Y-%m-%d, %H:%M')

                        if cur_datetime - post_time > delta_time:
                            exit_program = True
                            break

                        post_title = article.find(
                            'h2', class_="tm-article-snippet__title tm-article-snippet__title_h2"
                        ).text.strip()
                        post_link = article.find('a',
                                              class_='tm-article-snippet__title-link').get('href')
                        post_link = f"https://habr.com{post_link}"

                        post_post = article.find(
                            'div',
                            class_="tm-article-body tm-article-snippet__lead").text.strip()

                        post = {
                            'time': post_time.strftime("%Y-%m-%d, %H:%M"),
                            'title': post_title,
                            'link': post_link,
                            'post': post_post}
                        all_posts.append(post)
                    except Exception:
                        pass
                page = page + 1
            except Exception:
                pass
        else:
            break
    return all_posts


if __name__ == "__main__":
    posts = lookup()
    with open(f"/home/{os.getlogin()}/habr/posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)
