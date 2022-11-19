import json
import os

import bs4
import requests
from tqdm import tqdm


def read_page(src_name: str):
    with open(f"data/wpolityce/{src_name}.html") as f:
        return f.read()


def fetch_article_wgospodarce(link: str):
    article = {"url": link, "source": "wgospodarce"}
    article_response = requests.get(link)
    if article_response.ok:
        article_text = article_response.text
        article_soup = bs4.BeautifulSoup(article_text, "html.parser")
        title = article_soup.find("h2", class_="publication__title").get_text()
        article["title"] = title
        date = article_soup.find(
            "li", class_="meta__item meta__item--dates").get_text()
        article["date"] = date
        author = article_soup.find("p", class_="author__name").get_text()
        article["author"] = author
        content = article_soup.find("main",
                                    class_="publication__body").get_text()
        article["content"] = content
    return article


def fetch_article_wpolityce(link: str):
    article = {"url": link, "source": "wpolityce"}
    article_response = requests.get(link)
    if article_response.ok:
        article_text = article_response.text
        article_soup = bs4.BeautifulSoup(article_text, "html.parser")
        title = article_soup.find("h1", class_="article__title").get_text()
        article["title"] = title
        date = article_soup.find("time", class_="js-relative-date")["title"]
        article["date"] = date
        author = article_soup.find("h3",
                                   class_="article__author-name").get_text()
        article["author"] = author
        content = article_soup.find("section",
                                    class_="article__main").get_text()
        article["content"] = content
    return article


def scrap(src_name: str):
    indx = 0
    links = get_article_links(src_name)
    for article_link in tqdm():
        save_path = f"data/wpolityce_articles/{src_name.lower()}_{indx}.json"
        if os.path.exists(save_path):
            continue
        try:
            if "wgospodarce" in article_link:
                content = fetch_article_wgospodarce(article_link)
            elif "wpolityce" in article_link:
                content = fetch_article_wpolityce(article_link)
        except:
            continue
        json.dump(content, open(save_path, "w"), indent=True, sort_keys=True)
        indx += 1


def get_article_links(src_name: str):
    page_html = read_page(src_name)
    page_soup = bs4.BeautifulSoup(page_html, "html.parser")
    print("Scraping links from", src_name)
    for anchor in page_soup.find_all("a", class_="tile__link"):
        yield anchor["href"]


if __name__ == "__main__":
    for src_name in ["Gospodarka", "NBP"]:
        scrap(src_name)
