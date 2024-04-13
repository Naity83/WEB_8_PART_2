from random import randint
from faker import Faker
from model import Contact
import connect

fake = Faker()


def fill_contacts():
    Contact.drop_collection()
    for i in range(10):
        record = Contact()
        record.full_name = fake.name()
        record.email = fake.email()
        record.age = randint(12, 90)
        record.phone = fake.phone_number()
        record.date_registration = fake.date_between(start_date='-1y')
        record.email_priority = bool(randint(0, 1))
        record.save()


if __name__ == '__main__':
    fill_contacts()