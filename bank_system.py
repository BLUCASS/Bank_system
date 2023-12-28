from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///Banco_do_Brasil.db', echo=False)
Base = declarative_base()


# CREATING THE CLASS FOR THE PERSON
class Person(Base):
    '''Importing from Base and creating the person'''
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(30), nullable=False)
    pps = Column(String(9), nullable=False)
    password = Column(String(64), nullable=False)


# CREATING THE CLASS FOR THE BANK ACCOUNT
class Account(Base):
    '''Importing from Base and creating the Bank Account'''
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, nullable=False)
    account_number = Column(Integer, unique=True, nullable=False)
    funds = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        'person.id', ondelete='CASCADE'), nullable=False)


Base.metadata.create_all(engine)