import json

import bs4
import requests


def read_page():
    with open("scrapping/wpolityce/Nbp.html") as f:
        return f.read()


def fetch_article_wgospodarce(link: str):
    article = {"url": link, "source": "wgospodarce"}
    article_response = requests.get(link)
    if article_response.ok:
        article_text = article_response.text
        article_soup = bs4.BeautifulSoup(article_text, "html.parser")
        title = article_soup.find("h2", class_="publication__title").get_text()
        article["title"] = title
        date = article_soup.find("li", class_="meta__item meta__item--dates").get_text()
        article["date"] = date
        author = article_soup.find("p", class_="author__name").get_text()
        article["author"] = author
        content = article_soup.find("main", class_="publication__body").get_text()
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
        author = article_soup.find("h3", class_="article__author-name").get_text()
        article["author"] = author
        content = article_soup.find("section", class_="article__main").get_text()
        article["content"] = content
    return article


def scrap():
    data = []
    for article_link in get_article_links():
        if "wgospodarce" in article_link:
            try:
                content = fetch_article_wgospodarce(article_link)
            except:
                pass
            else:
                data.append(content)
        elif "wpolityce" in article_link:
            try:
                content = fetch_article_wpolityce(article_link)
            except:
                pass
            else:
                data.append(content)
    json.dump(
        data,
        open("scrapping/wpolityce/data.json", mode="w"),
        indent=4,
        sort_keys=True,
    )


def get_article_links():
    page_html = read_page()
    page_soup = bs4.BeautifulSoup(page_html, "html.parser")
    for anchor in page_soup.find_all("a", class_="tile__link"):
        yield anchor["href"]


if __name__ == "__main__":
    scrap()
