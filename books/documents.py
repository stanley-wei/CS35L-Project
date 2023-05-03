from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.fields import FloatField, IntegerField, TextField
from django_elasticsearch_dsl.registries import registry
from .models import Book

@registry.register_document
class BookDocument(Document):
    class Index:
        name = 'books'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Book

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000
    
    title = TextField(attr='title', index=True)
    author = TextField(attr='author', index=True)
    pub_year = IntegerField(attr='pub_year', index=True)
    avg_overall = FloatField(attr='avg_rating', index=True)
