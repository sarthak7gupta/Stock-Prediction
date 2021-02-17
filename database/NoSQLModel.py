from functools import partial
from json import dumps

from bson import json_util
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine.fields import (DateTimeField, ListField, ObjectId,
                                ObjectIdField, ReferenceField, StringField,
                                URLField)

dumps = partial(dumps, default=json_util.default)


class Article(EmbeddedDocument):
    title = StringField()
    html = StringField()
    text = StringField()
    summary = StringField()
    tags = ListField(StringField())
    keywords = ListField(StringField())

    meta = {"collection": "articles"}

    def json(self):
        return dumps({
            "title": self.title,
            "html": self.html,
            "text": self.text,
            "summary": self.summary,
            "tags": self.tags,
            "keywords": self.keywords,
        })


class Entry(Document):
    link = URLField(required=True, primary_key=True)
    title = StringField()
    summary = StringField()
    published = DateTimeField()
    feed = ReferenceField("Feed")
    article = EmbeddedDocumentField(Article)

    meta = {"collection": "entries"}

    def json(self):
        return dumps({
            "link": self.link,
            "title": self.title,
            "summary": self.summary,
            "published": self.published,
            "article": self.article
        })


class Feed(Document):
    href = URLField(required=True, primary_key=True)
    title = StringField()
    subtitle = StringField()
    generator = StringField()
    last_updated = DateTimeField()
    entries = ListField(ReferenceField(Entry))

    meta = {"collection": "feeds"}

    def json(self):
        return dumps({
            "href": self.href,
            "title": self.title,
            "subtitle": self.subtitle,
            "generator": self.generator,
        })
