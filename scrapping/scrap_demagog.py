import pandas
import requests

import os

import bs4


topics = [
    "finanse",
    "gospodarka",
    "polityka-krajowa",
    "media",
    "polityka-spoleczna",
]
base_url_format = "https://demagog.org.pl/tematy/{topic}/page/{page}/"


def create_path_if_not_exist(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def download_page(topic: str, page: int):
    url = base_url_format.format(page=page, topic=topic)
    response = requests.get(url)
    return response.ok, response.text


def download_all_pages():
    for topic in topics:
        page = 1
        while True:
            ok, html = download_page(topic, page)
            if not ok or not html:
                break
            create_path_if_not_exist(f"scrapping/demagog/{topic}")
            create_path_if_not_exist(f"scrapping/demagog/{topic}/{page}")
            with open(
                f"scrapping/demagog/{topic}/{page}/page.html", "w", encoding="utf-8"
            ) as file:
                file.write(html)
            page += 1


def get_links_and_labels():
    for topic in topics:
        page_id = 1
        while os.path.exists(f"scrapping/demagog/{topic}/{page_id}"):
            with open(f"scrapping/demagog/{topic}/{page_id}/page.html") as page:
                page_soup = bs4.BeautifulSoup(page.read(), "html.parser")
                articles = page_soup.find_all("article")
                for article in articles:
                    label = article.find("div", class_="post-label")
                    links = article.select(
                        ".border, .border-primary, .d-block, .photo-article"
                    )
                    if not links:
                        continue
                    link = links[0]["href"]
                    yield {"label": label.get_text().strip(), "link": link}
                page_id += 1


def generate_links_labels():
    data = list(get_links_and_labels())
    df = pandas.DataFrame(columns=["link", "label"], data=data)
    df.to_csv("scrapping/demagog/articles.csv")


def fetch_link(link: str):
    response = requests.get(link)
    data = {"source": "demagog", "url": link}
    if response.ok:
        text = response.text
        soup = bs4.BeautifulSoup(text, "html.parser")
        title = soup.find("h1", class_="w-100 mb-1").get_text()
        data["title"] = title
        date = soup.find("p", class_="date w-100").get_text()
        data["date"] = date
        try:
            author = soup.find(
                "div", class_="h2 person-name mt-0 count-text"
            ).get_text()
        except:
            author = ""
        data["author"] = author
        container = soup.find(
            "div",
            class_="row-custom col-12 px-0 pb-5 big-txt-2 content-editor target-blank count-text",
        )
        texts = []
        for span in container.find_all("span"):
            text = span.get_text()
            texts.append(text.strip())
        content = " ".join(texts)
        data["content"] = content
    return data


def scrap_single_pages():
    df = pandas.read_csv("scrapping/demagog/articles.csv")
    data = []
    for _, row in df.iterrows():
        label = row["label"]
        link = row["link"]
        try:
            data.append({"label": label, **fetch_link(link)})
        except:
            pass
    df = pandas.DataFrame(
        columns=["source", "url", "date", "author", "title", "content", "label"],
        data=data,
    )
    df.to_csv("scrapping/demagog/dataset.csv")


if __name__ == "__main__":
    # print(next(iter(get_links_and_labels())))
    # generate_links_labels()
    scrap_single_pages()
