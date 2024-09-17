import logging
import re
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import engine, Contact

def is_phone_valid(pn):
    pass

class PhoneBook:
    def __init__(self):
        self.session = Session(engine)
        
    def create(self, firstName, lastName, phoneNumber, emailAddress=None, address=None):
        contact = Contact(firstName=firstName, lastName=lastName, phoneNumber=phoneNumber, emailAddress=emailAddress, address=address)
        self.session.add(contact)
        self.session.commit()
        
    def retrieve(self, **kwargs):
        param = {}
        for key,value in enumerate(kwargs):
            if key in {"firstName", "lastName", "phoneNumber", "emailAddress", "address"}:
                param[key] = value
        result = self.session.execute(select(Contact).filter_by(**param)).scalars().all()
        print("|| First Name || Last Name || Phone Number || Email Address || Address ||")
        for contact in result:
            print(contact)
        
    def update(self, firstName, lastName, phoneNumber, emailAddress=None, address=None):
        pass
        
    def delete(self, firstName, lastName, phoneNumber, emailAddress=None, address=None):
        pass

if __name__=="__main__":
    pb = PhoneBook()
    # pb.create("Yicheng", "Wang", "(613)853-4670", "ywang087@uottawa.ca", "190 Lees Ave")
    # pb.create("Yicheng", "Wang", "(613)866-4670", "ywang087@uottawa.ca", "190 Lees Ave")
    pb.retrieve(firstName="Yicheng")