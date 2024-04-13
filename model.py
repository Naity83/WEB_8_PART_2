from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField


class Contact(Document):
    full_name = StringField(min_lenght=5, required=True)
    email = StringField(min_length=3, unique=True)
    age = IntField()
    phone = StringField()
    date_registration = DateTimeField()
    send_message = BooleanField(default=False)
    email_priority = BooleanField()

    meta = {'collection': 'contacts'}

