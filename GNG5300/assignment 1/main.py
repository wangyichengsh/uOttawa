import os
import logging
import re
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, update

from db import engine, Contact

logger = logging.getLogger(__name__)

def is_phone_valid(phoneNumber):
    return re.fullmatch(r"\([0-9]{3}\)[0-9]{3}-[0-9]{4}", phoneNumber)!=None 

def is_email_valid(emailAddress):
    return re.fullmatch(r".+@.+\..+", emailAddress)!=None 

class PhoneBook:
    def __init__(self):
        self.session = Session(engine)
    
    def print_result(self, result):
        print("id || First Name || Last Name || Phone Number || Email Address || Address || Created At")
        for contact in result:
            print(contact)
    
    def create(self, firstName, lastName, phoneNumber, emailAddress=None, address=None):
        if not is_phone_valid(phoneNumber):
            logger.error('Wrong Phone Number!')
            return None
        if len(emailAddress)>0 and not is_email_valid(emailAddress):
            logger.error('Wrong Email Address!')
            return None  
        contact = Contact(firstName=firstName, lastName=lastName, phoneNumber=phoneNumber, emailAddress=emailAddress, address=address)
        self.session.add(contact)
        self.session.commit()
        return contact
        
    def retrieve(self, **kwargs):
        param = {}
        for key,value in enumerate(kwargs):
            if key in {"firstName", "lastName", "phoneNumber", "emailAddress", "address"} and value!=None:
                param[key] = value
        result = self.session.execute(select(Contact).filter_by(**param)).scalars().all()
        self.print_result(result)
        return result
        
    def update(self, cid, new_contact):
        result = self.session.execute(select(Contact).filter_by(cid=cid)).scalar_one_or_none()
        if result != None:
            param = {}
        else:
            return False 
        for key,value in enumerate(new_contact):
            if key in {"firstName", "lastName", "phoneNumber", "emailAddress", "address"} and value!=None:
                if key =='phoneNumber':
                    if not is_phone_valid(new_contact[key]):
                        logger.error('Wrong Phone Number!')
                        return False
                if key =='emailAddress' and len(new_contact[key])>0:
                    if not is_email_valid(new_contact[key]):
                        logger.error('Wrong Email Address!')
                        return False    
                param[key] = value
            new_contact['cid'] = cid   
            self.session.execute(update(Contact),[new_contact])
            self.session.commit()
            return True
        return False
            
    def delete(self, cid_list):
        result_list = []
        if isinstance(cid_list, int):
            cid_list = [cid_list]
        for cid in cid_list:
            result = self.session.execute(select(Contact).filter_by(cid=cid)).scalar_one_or_none()
            if result != None:
                self.session.delete(result)
                self.session.commit()
                result_list.append(True)
            else:
                result_list.append(False)
        return result_list
            
    def load_csv(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    param = line.split(',')
                    param[-1] = param[-1].rstrip('\n')
                    self.create(*param)
    
    def wildcard_search(self, keyword):
        result = []
        all_contact = self.session.execute(select(Contact)).scalars().all()
        for contact in all_contact:
            if (keyword in contact.firstName) or (keyword in contact.lastName) or (keyword in contact.phoneNumber)or (keyword in contact.emailAddress) or (keyword in contact.address):
                result.append(contact)
        self.print_result(result)
        return result
        
    def search_by_add_time(self, begin_time, end_time):
        try:
            begin_ts = datetime.fromisoformat(begin_time)
            end_ts = datetime.fromisoformat(end_time)
        except Exception as e:
            logger.error('Wrong Time Zone!')
            return None
        result = []
        all_contact = self.session.execute(select(Contact)).scalars().all()
        for contact in all_contact:
            if (begin_ts <= contact.add_ts) and (end_ts >= contact.add_ts):
                result.append(contact)
        self.print_result(result)
        return result
        
    def sort(self, field):
        pass
        
    def group(self):
        pass
        
if __name__=="__main__":
    pb = PhoneBook()
    # pb.create("Yicheng", "Wang", "(613)853-4670", "ywang087@uottawa.ca", "190 Lees Ave")
    # pb.create("Yicheng", "Wang", "(613)866-4670", "ywang087@uottawa.ca", "190 Lees Ave")
    # pb.retrieve()
    # new_contact = {"firstName":'Yisheng'}
    # pb.update(2, new_contact)
    # pb.retrieve()
    # pb.delete(3)
    # pb.retrieve()
    pb.load_csv('loadtest.csv')
    # pb.retrieve()
    # pb.wildcard_search('070')
    pb.search_by_add_time('2024-09-19', '2024-09-20')