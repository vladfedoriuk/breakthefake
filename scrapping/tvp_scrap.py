import bs4
import requests
import sys
import time
from tqdm import tqdm
import json
import os

PER_PAGE = 12
SRC_PAGE = "https://www.tvpparlament.pl/aktualnosci?id=&sort_by=RELEASE_DATE&sort_desc=true&start_rec={}&listing_mod=&with_video="


def download_page(page):
    """Download page from tvpparlament.pl"""
    url = SRC_PAGE.format(page)
    response = requests.get(url)
    return response.text


def download_all_pages():
    """Download all pages from tvpparlament.pl"""
    page = 0
    while True:
        html = download_page(page)
        if not html:
            break
        with open("data/tvp/aritcle_list_tvp_{}.html".format(page // PER_PAGE),
                  "w",
                  encoding="utf-8") as file:
            file.write(html)
        page += PER_PAGE


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
    """Download article from tvpparlament.pl"""
    response = requests.get(url, timeout=15)
    article_text = bs4.BeautifulSoup(response.text, "html.parser")
    author = article_text.find("span", {"class": "signature"}).text
    try:
        dcontent = article_text.find("div", {"class": "date"}).text.split(';')
        date = dcontent[0]
        author = dcontent[1]
        source = dcontent[2]
    except AttributeError:
        date = ''
        source = ''
        author = ''
    content = article_text.select("div.mainContent")
    full_content = []
    for scontent in content:
        cand_text = " ".join(
            [x.text for x in scontent.find_all("div", {"class": "txt"})])
        full_content.append(cand_text)
    target_json = {
        "author": author,
        "claimed_source": source,
        "date": date,
        "title": article_text.select("h1")[0].text,
        "content": clean_text(" ".join(full_content)),
        "url": url,
        'source': 'tvp'
    }
    return target_json


def iterate_saved_article_pages():
    """Iterate over all saved pages"""
    indx = 0
    for page in tqdm(range(0, 94)):
        with open("data/tvp/aritcle_list_tvp_{}.html".format(page),
                  "r",
                  encoding="utf-8") as file:
            html = file.read()
            scrapper = bs4.BeautifulSoup(html, "html.parser")

            for article in scrapper.find_all("div", {"class": "news"}):
                target_save = f"data/tvp_articles/article_tvp_{indx}.json"
                if os.path.exists(target_save):
                    indx += 1
                    continue
                try:
                    article_url = article.find("a")["href"]
                    article_text = download_article_text(article_url)
                    if not len(article_text):
                        continue
                    with open(target_save, "w") as article_file:
                        json.dump(article_text, article_file)
                except (AttributeError, requests.exceptions.ReadTimeout,
                        FileNotFoundError) as ex:
                    print("Error: {}".format(ex))
                time.sleep(0.5)
                indx += 1


if __name__ == "__main__":
    # download_all_pages()
    iterate_saved_article_pages()