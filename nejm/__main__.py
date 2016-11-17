"""package entry"""
from nejm.article import abstract
from nejm.doi_codes import doi_page_navigate

for page in doi_page_navigate(1, 100):
    for code in page:
        print('DOI', code, abstract(code))
