"""
Get some abstracts from the New England Journal of Medicine
"""
from html.parser import HTMLParser
import requests

# BASEURL = 'http://www.nejm.org/doi/pdf/10.1056/'
BASEURL = 'http://www.nejm.org/doi/full/10.1056/'
ABSTRACT_CLASS = 'class', 'abstract-content'
ABSTRACT_FULL_CLASS = 'id', 'abstract'


class NewEngArticleParser(HTMLParser):
    """simple article parser class"""
    abstract = ''
    simple_flag = False
    complex_abstract = False

    def handle_starttag(self, tag, attrs):
        """
        starting tag <p> with class="abstract-content"
        """
        if tag not in ('p', 'dd'):
            return

        if self.complex_abstract and tag == 'p':
            self.simple_flag = True

        for name, value in attrs:
            if (name, value) == ABSTRACT_CLASS:
                self.simple_flag = True
            elif (name, value) == ABSTRACT_FULL_CLASS:
                self.complex_abstract = True

    def handle_data(self, data):
        """
        if found starting tag with abstract, means the text will come next

        no in-between garbage tags to worry about
        """
        if self.simple_flag:
            self.simple_flag = False
            # if not data.startswith('Full Text of'):
            if self.abstract:
                self.abstract = '%s %s' % (self.abstract, data.strip())
            else:
                self.abstract = data.strip()

    def handle_endtag(self, tag):
        """
        starting tag <p> with class="abstract-content"
        """
        if tag == 'dd' and self.complex_abstract:
            self.complex_abstract = False


def parse_article(html):
    """
    parse html and return it in a dict

    since only the abstract matters, we focus on that for now
    """
    parser = NewEngArticleParser()
    parser.feed(html)

    return {'abstract': parser.abstract}


def abstract(doicode):
    """return the abstract of the article"""
    r = requests.get(BASEURL + doicode)
    if r.status_code == 200:
        return parse_article(r.text).get('abstract', '')

    return ''


if __name__ == '__main__':
    print(abstract('NEJMimc0900128'))
    print(abstract('NEJMra063052'))
    print(abstract('NEJMoa1413579'))
