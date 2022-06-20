#!/usr/bin/python

import datetime
import json
import os.path
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup


def get_html(url):
    req = requests.get(url)
    src = req.text

    with open("habr/index.html", "w", encoding="utf-8") as file:
        file.write(src)


def get_data(file, date):
    with open(file, "r", encoding="utf-8") as dat:
        src = dat.read()

    soup = BeautifulSoup(src, "lxml")

    articles = soup.find_all("article")
    posts = []
    for article in articles:
        post_datetime = article.find("time").get("datetime")
        post_date = post_datetime.split("T")[0]
        post_time = post_datetime.split("T")[1].split(".")[0]
        time = f"{post_date}, {post_time}"
        title = article.find(class_="tm-article-snippet__title-link").text
        link = article.find("a", class_="tm-article-snippet__title-link").get("href")
        post = {
            "time": time,
            "title": title,
            "link": f"https://habr.com{link}"
        }
        posts.append(post)
        if post_date < str(date) and post_time < "24:00:00":
            break
    return posts


def main():
    print("program for print posts from habr.com/ru/all into json file"
          "\n\tposts gets by current date, but if you want get posts "
          "from other date put your date into param:"
          "\n\t\tparseHabr.py yyyy-mm-dd"
          "\n\tfor example: $ parseHabr.py 2022-06-18")
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = str(datetime.date.today())
    if not os.path.exists("habr"):
        os.mkdir("habr")
    html_path = "habr/index.html"
    url = "https://habr.com/ru/all"
    page = 1
    data = []
    while True:
        print(f"parse page {page}")
        full_url = f"{url}/page{page}"
        get_html(full_url)
        posts = get_data(html_path, date)
        for post in posts:
            data.append(post)
        if posts[-1].get("time").split(", ")[1] < "24:00:00" \
                and posts[-1].get("time").split(", ")[0] < date:
            with open("habr/posts.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            break
        page += 1
        sleep(1)
    os.remove("habr/index.html")


if __name__ == "__main__":
    main()
