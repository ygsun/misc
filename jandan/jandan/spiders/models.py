from playhouse.db_url import connect
from peewee import *

from ..settings import DB_CONFIG

database_proxy = Proxy()  # Create a proxy for our db.


class BaseModel(Model):
    class Meta:
        # Use proxy for our DB.
        database = database_proxy

    def __repr__(self):
        return '<{} name={}>'.format(self.__class__.__name__, self.name)


class Author(BaseModel):
    name = CharField(max_length=256)


class Catelog(BaseModel):
    name = CharField(max_length=256)

    def __repr__(self):
        return '<{} name={}>'.format(self.__class__.__name__, self.name)


class Picture(BaseModel):
    author = ForeignKeyField(Author, related_name='pictures')
    catelog = ForeignKeyField(Catelog, related_name='catelogs')
    pub_date = DateTimeField()
    url = CharField(max_length=256)
    path = CharField(max_length=256)

    def __repr__(self):
        return '<{} url={}>'.format(self.__class__.__name__, self.url)


# Based on configuration, use a different database.
if DB_CONFIG == 'DEVEL':
    database = connect('sqlite:///devel.db')
elif DB_CONFIG == 'TESTING':
    database = connect('sqlite:///:memory:')
elif DB_CONFIG == 'PROD':
    database = connect('mysql://root:1111@localhost/jandan')
else:
    database = connect('sqlite:///devel.db')

# Configure our proxy to use the db we specified in config.
database_proxy.initialize(database)
database_proxy.create_tables([Author, Picture, Catelog], True)
