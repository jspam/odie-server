#! /usr/bin/env python3

from datetime import datetime as time
from marshmallow import Schema, fields

import config
from models.documents import Document
from models.odie import Order


class IdSchema(Schema):
    id = fields.Int()

class DocumentSchema(IdSchema):
    lectures = fields.List(fields.Str())
    examinants = fields.List(fields.Int(), attribute='examinants_ids')
    date = fields.Date()
    number_of_pages = fields.Int()
    solution = fields.Str()
    comment = fields.Str()
    documentType = fields.Str(attribute='document_type')
    available = fields.Method('is_available_for_printing')

    def is_available_for_printing(self, obj):
        return obj.file_id is not None


class ExaminantSchema(IdSchema):
    name = fields.Str()


class OrderLoadSchema(IdSchema):
    name = fields.Str(required=True)
    creation_time = fields.Date()
    # list of document ids
    documents = fields.List(fields.Int(), required=True)

    def make_object(self, data):
        return Order(name=data['name'],
                     creation_time=time.now(),
                     document_ids=data['documents'])


class OrderDumpSchema(OrderLoadSchema):
    documents = fields.List(fields.Nested(DocumentSchema))


class LectureSchema(IdSchema):
    name = fields.Str()
    aliases = fields.List(fields.Str())
    subject = fields.Str()
    comment = fields.Str()

class LectureDocumentsSchema(LectureSchema):
    documents = fields.List(fields.Nested(DocumentSchema))


class DepositSchema(IdSchema):
    price = fields.Int()
    name = fields.Str()
    lectures = fields.List(fields.Str())


class PrintJobLoadSchema(Schema):
    coverText = fields.Str(required=True)
    documents = fields.List(fields.Int(), required=True)
    depositCount = fields.Int(required=True)
    printer = fields.Str(required=True, validate=lambda s: s in config.FS_CONFIG['PRINTERS'])

