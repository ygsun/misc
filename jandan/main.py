from peewee import *
import datetime
import random
import string

db = SqliteDatabase('people.db')


class BaseModel(Model):
    class Meta:
        database = db

    def __repr__(self):
        return '<{} name={}>'.format(self.__class__.__name__, self.name)


class User(BaseModel):
    username = CharField(unique=True)

    @classmethod
    def gen_random_chars(cls, count):
        return ''.join(random.sample(string.ascii_letters, count))

    @classmethod
    def create_random_user(cls, count=10):
        with db.atomic():
            for _ in range(count):
                cls.insert(username=cls.gen_random_chars(5)).execute()

    def __repr__(self):
        return '<{} username={}>'.format(self.__class__.__name__, self.username)


class Tweet(BaseModel):
    user = ForeignKeyField(User, related_name='tweets')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)

    @classmethod
    def gen_random_datetime(cls):
        now = datetime.datetime.now()
        td = datetime.timedelta(weeks=random.randint(-100, 0),
                                days=random.randint(-10, 0),
                                hours=random.randint(-10, 0),
                                minutes=random.randint(-10, 0),
                                seconds=random.randint(-10, 0))
        return now + td

    @classmethod
    def create_random_tweet(cls, count=10):
        with db.atomic():
            for _ in range(count):
                cls.insert(message=User.gen_random_chars(16),
                           user=random.randint(1, 10000),
                           created_date=cls.gen_random_datetime(),
                           is_published=random.choice((True, False))).execute()

    def __repr__(self):
        return '<{} message={}>'.format(self.__class__.__name__, self.message)


class Relation(BaseModel):
    user_src = ForeignKeyField(User, related_name='srcs')
    user_dst = ForeignKeyField(User, related_name='dsts')

    @classmethod
    def gen_random_id(cls, lower, upper):
        return random.randint(lower, upper)

    @classmethod
    def create_random_rel(cls, count=10):
        with db.atomic():
            for _ in range(count):
                cls.insert(user_src=cls.gen_random_id(0, 10000),
                           user_dst=cls.gen_random_id(0, 10000)).execute()

    def __repr__(self):
        return '<{} src={} dst={}>'.format(self.__class__.__name__, self.user_src, self.user_dst)