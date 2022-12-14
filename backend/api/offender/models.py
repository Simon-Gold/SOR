from datetime import datetime
# internals
from api import db


class OffenderCharge(db.EmbeddedDocument):
    description = db.StringField(max_length=1024)
    offense_date = db.DateTimeField()


class OffenderCase(db.Document):
    case_number = db.StringField(max_length=64, unique=True)
    charges = db.ListField(db.EmbeddedDocumentField(OffenderCharge))

    def __str__(self):
        return self.case_number

class DateOfBirth(db.EmbeddedDocument):
    """Offender date of birth object"""
    year = db.IntField(min=1900)
    month = db.IntField(min=1, max=12)
    day = db.IntField(min=1, max=12)

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}"

class Demographic(db.EmbeddedDocument):
    height = db.StringField(max_length=24)
    weight = db.StringField(max_length=24)
    sex = db.StringField(max_length=24)
    race = db.StringField(max_length=64)

class OffenderAddress(db.EmbeddedDocument):
    """OffenderAddress object"""
    line = db.StringField(max_length=60)

class OffenderName(db.EmbeddedDocument):
    """ OffenderName object"""
    first_name = db.StringField(max_length=60)
    middle = db.StringField(max_length=60)
    last_name = db.StringField(max_length=60, required=True)

class Offender(db.Document):
    """Offender main object"""
    names = db.ListField(db.EmbeddedDocumentField(OffenderName))
    addresses = db.ListField(db.EmbeddedDocumentField(OffenderAddress))
    is_deleted = db.BooleanField(default=False)
    date_of_birth = db.DateTimeField()
    created_date = db.DateTimeField(default=datetime.now)
    updated_date = db.DateTimeField(default=datetime.now)
    dob = db.EmbeddedDocumentField(DateOfBirth)
    demographic = db.EmbeddedDocumentField(Demographic)
    age = db.IntField(min=1, max=12)
    state = db.StringField(max_length=2)
    cases = db.ListField(db.ReferenceField(OffenderCase))
    

    def __str__(self):
        return f"{self.names[0].first_name} {self.names[0].last_name}"