import bs4
import requests
import sys
import time
from tqdm import tqdm
import json
import os
import glob

SRC_PAGE = "https://m.pch24.pl/dzial/wiadomosci/page/{}/"


def download_page(page):
    """Download page from wp.pl"""
    url = SRC_PAGE.format(page)
    response = requests.get(url)
    return response.text


def download_all_pages():
    """Download all pages from pch24.pl"""
    page = 1
    while True:
        html = download_page(page)
        if not html:
            break
        with open("data/pch24/aritcle_list_pch24_{}.html".format(page),
                  "w",
                  encoding="utf-8") as file:
            file.write(html)
        page += 1


def find_wp_author(parsed_html):
    author = parsed_html.find("a title", {"class": "title"})
    if author:
        return author.text.replace("/author", "").replace("-",
                                                          " ").capitalize()

    author = parsed_html.find('span', {'class': 'signature--author'})
    if author:
        return author.text

    return ''


def clean_text(text):
    """Clean text"""
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")
    text = text.replace("  ", " ")
    text = text.replace("   ", " ")
    text = text.replace("    ", " ")
    return text


def download_article_text(url):
    """Download article from pch24.pl"""
    response = requests.get(url, timeout=20)
    article_text = bs4.BeautifulSoup(response.text, "html.parser")
    author = find_wp_author(article_text)
    try:
        date = article_text.find('span', {'class': 'date'}).text
    except AttributeError:
        date = ''
    content = article_text.find("article", {"class": "pch-article"})
    full_content = []
    for scontent in content.find_all("p"):
        full_content.append(scontent.text)
    target_json = {
        "author": author,
        "claimed_source": 'pch24.pl',
        "date": date,
        "title": article_text.select("h1")[0].text,
        "content": clean_text(" ".join(full_content)),
        "url": url,
        'source': 'pch24',
    }
    return target_json


def iterate_over_pages():
    """Iterate over all pages"""
    indx = 0
    for page in tqdm(list(glob.glob("data/pch24/*.html"))):
        with open(page, "r", encoding="utf-8") as file:
            contents = file.read()
            soup = bs4.BeautifulSoup(contents, "html.parser")
            articles = soup.find_all("h3", {"class": "heading"})
            for sarticle in articles:
                target_save = f"data/pch24_articles/{indx}.json"
                if os.path.exists(target_save):
                    indx += 1
                    continue
                try:
                    url = sarticle.find("a")
                    url = url.get("href")
                    article_json = download_article_text(url)
                    with open(
                            target_save,
                            "w",
                    ) as file:
                        json.dump(article_json, file)

                except (AttributeError, requests.exceptions.ConnectionError,
                        requests.exceptions.ReadTimeout,
                        FileNotFoundError) as ex:
                    print("Error: {}".format(ex))
                time.sleep(0.5)
                indx += 1


if __name__ == "__main__":
    # download_all_pages()
    iterate_over_pages()