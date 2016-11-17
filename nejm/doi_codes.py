"""
Find some nejm doi's for us
"""
from html.parser import HTMLParser
import requests

QUERY = 'heart'
URL = 'http://www.nejm.org/search?q={}&page='.format(QUERY)
DOI_LINK = '/doi/abs/10.1056/'


class NewEngSearchParser(HTMLParser):
    """simple search parser"""
    def __init__(self):
        """empty set"""
        super(NewEngSearchParser, self).__init__()
        self.doi_links = set()

    def handle_starttag(self, tag, attrs):
        """
        starting tag <p> with class="abstract-content"
        """
        if tag != 'a':
            return

        for name, value in attrs:
            if name == 'href' and DOI_LINK in value:
                self.doi_links.add(value.replace(DOI_LINK, ''))


def parse_doi(html):
    """get the doi codes from the page """
    parser = NewEngSearchParser()
    parser.feed(html)

    return parser.doi_links


def find_doi_codes(url):
    """find a doi code list"""
    r = requests.get(url)
    if r.status_code == 200:
        return parse_doi(r.text)

    return set()


def doi_page_navigate(n, m):
    """navigate in page range"""

    for n in range(n, m):
        yield find_doi_codes('{}{}'.format(URL, n))


if __name__ == '__main__':
    for page in doi_page_navigate(1, 5):
        print(page)
