from collections import UserDict
from datetime import datetime
import re

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, records):
        self.current_value = 0
        self.records = records
        names = []
        for i in range(self.records):
            names.append(self.data[list(self.data.keys())[i]])
        self.current_value += self.records
        yield names

class Field():
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
       self._value = new_value

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        self.value = value

class Birthday(Field):
     # def __init__(self, value):
     #     super().__init__(value)
     #     # self.__value = value
     #
     # @property
     # def value(self):
     #     return self.__value

     @Field.value.setter
     def value(self, new_value):
         if re.match('\d{4}[.]\d{2}[.]\d{2}', new_value):
             self._value = new_value
         else:
             print("Input date in format YYYY.MM.DD")

class Record():
    def __init__(self, name, *phones):
        self.name = Name(name)
        self.phones = []
        if phones:
            for phone in phones:
                self.put_phone_list(phone)
        self.birthday = ''

    def put_phone_list(self, phone_new):
        phone_new = Phone(phone_new).value
        for phone in self.phones:
            if phone_new == phone.value:
                print(f"{phone_new} already recorded for {self.name.value}")
        self.phones.append(Phone(phone_new))

    def change(self, phone_old, phone_new):

        phone_old = Phone(phone_old).value
        phone_new = Phone(phone_new).value
        match = False

        for phone in self.phones:

            if phone.value == phone_new:
                return f"{phone_new} already recorded for {self.name.value}"

            if phone.value == phone_old:
                match = True

        if not match:
            return f"{phone_old} exist in the contact {self.name.value}"

        for index, phone in enumerate(self.phones):
            if phone.value == phone_old:
                self.phones.remove(phone)
                self.phones.insert(index, Phone(phone_new))
                return f"{phone_old} changed to {phone_new}"

    def add_birthday(self, birthday):
        self.birthday = birthday
        return f"{birthday} added to {self.name.value}"

    def days_to_birthday(self):
        today = datetime.today()
        bday = datetime(2022, int(self.birthday.split('.')[1]), int(self.birthday.split('.')[2]))
        bday1 = datetime(2023, int(self.birthday.split('.')[1]), int(self.birthday.split('.')[2]))
        timediff = (bday - today).days + 1 if (today - bday).days < 0 else (bday1 - today).days + 1
        return f'{timediff} days till {self.name.value} birthday left!'
