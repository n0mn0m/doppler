import os
from requests_html import HTMLSession
from requests import HTTPError


class ContentExtractor:
    """
    Provided a site structure where links are a combination of the base URL
    and page specific URL along with a sitemap this crawler will scrape
    the core content of the class provided and save the content to your
    local directory.
    """

    def __init__(self, base_url, sitemap, data_dir, search_tag):
        self.base_url = base_url
        self.sitemap = sitemap
        self.parsed_links = set()
        self.wiki_pages = set()
        self.data_dir = data_dir
        self.html_dir = self._make_data_dirs("html")
        self.contents_dir = self._make_data_dirs("contents")
        self.search_tag = search_tag

    def _make_data_dirs(self, dir):
        if not os.path.exists(os.path.join(self.data_dir, dir)):
            os.mkdir(os.path.join(self.data_dir, dir))

        return os.path.join(self.data_dir, dir)

    def parse_sitemap(self):
        session = HTMLSession()

        sitemap = session.get(self.sitemap)
        self.parsed_links.update(sitemap.html.links)

    def filter_wiki_pages(self):
        for link in self.parsed_links:
            if "/wiki/" in link and "." not in link:
                self.wiki_pages.add(link)

    def download_and_parse_pages(self):
        for page in self.wiki_pages:
            self._save_page(self.base_url + page)

    def _save_page(self, page):
        name = page.split(r"/")[-1]
        session = HTMLSession()

        try:
            wiki_page = session.get(page)
        except HTTPError:
            print(f"Could not download {wiki_page}")

        with open(os.path.join(self.html_dir, name + ".html"), "w+") as f:
            f.write(str(wiki_page.html))

        self._save_page_contents(wiki_page, name)

    def _save_page_contents(self, page, name):
        contents = page.html.find(self.search_tag, first=True)
        with open(os.path.join(self.contents_dir, name + ".txt"), "w+") as f:
            f.write(contents.text)


if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.getcwd(), "data")):
        os.mkdir(os.path.join(os.getcwd(), "data"))

    parser = ContentExtractor(
        "http://eclipse-phase.wikia.com",
        "http://eclipse-phase.wikia.com/wiki/Local_Sitemap",
        os.path.join(os.getcwd(), "data"),
        "#mw-content-text",
    )

    parser.parse_sitemap()
    parser.filter_wiki_pages()
    parser.download_and_parse_pages()
