import os.path

from books.models import Book

def run():
    file = open(os.path.dirname(__file__) + '/../datasets/books.csv', 'r');
    headers = file.readline().split(',');
    title_index = headers.index('title')
    authors_index = headers.index('authors')
    date_index = headers.index('publication_date')

    isbn_index = headers.index('isbn')
    language_index = headers.index('language_code')
    num_ratings_index = headers.index('ratings_count')

    while(True):
        line = file.readline()
        if not line.strip():
            break;
        line = line.strip().split(',');

        if int(line[num_ratings_index]) > 100000:
            book = Book(title = line[title_index].split("(")[0].strip(), 
                            author = ', '.join(line[authors_index].split('/')).strip(),
                            pub_year = int(line[date_index].split('/')[2]))
            book.save()
