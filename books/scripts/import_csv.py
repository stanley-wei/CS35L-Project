import os.path
import re

from books.models import Book
from olclient.openlibrary import OpenLibrary

def run():
    ol = OpenLibrary()

    file = open(os.path.dirname(__file__) + '/../datasets/books.csv', 'r');
    headers = file.readline().split(',');
    title_index = headers.index('title')
    authors_index = headers.index('authors')
    date_index = headers.index('publication_date')
    pages_index = headers.index('num_pages')

    isbn_index = headers.index('isbn')
    language_index = headers.index('language_code')
    num_ratings_index = headers.index('ratings_count')

    while(True):
        line = file.readline()
        if not line.strip():
            break;
        line = line.strip().split(',');

        if int(line[num_ratings_index]) > 100000 and line[language_index] == "eng":
            book = Book(title = line[title_index].split("(")[0].strip(), 
                            author = ', '.join(line[authors_index].split('/')).strip(),
                            num_pages = int(line[pages_index]))
            
            try:
                edition = ol.Edition.get(isbn=line[isbn_index])
                book.olid = edition.olid
                try:
                    work = ol.Work.get(edition.work_olid)
                    date = work.first_publish_date
                except:
                    date = edition.publish_date

                t = re.search('\d{% s}'% 4, date)
                book.pub_year = (int(t.group(0)) if t else None)
            except:
                book.pub_year = int(line[date_index].split('/')[2])
                
            print(book.title)

            book.save()
