from sqlalchemy.orm import sessionmaker
from bank_system import Person, Account, engine

Session = sessionmaker(bind=engine)
session = Session()

#################################################################################################################
# DEALING WITH THE PERSON
def name():
    try:
        name = str(input('Full Name: ')).title().strip()[0:50]
        for letter in name:
            if not letter.isalpha() and not letter.isspace():
                raise ValueError
    except:
        print('\033[31mONLY LETTERS (A-Z) ARE ACCEPTED.\033[m')
    else:
        return name
    

def email():
    try:
        email = str(input('Email: ')).lower().strip()[0:30]
        for letter in email:
            if letter.isspace():
                raise ValueError
    except:
        print('\033[31mINVALID EMAIL\033[m')
    else:
        if '@' not in email:
            email += '@gmail.com'
        return email


def pps():
    from random import randint
    pps = randint(1000000, 9999999)
    return str(pps)


def password():
    from hashlib import sha256
    while True:
        password = str(input('Password: '))
        if len(password) < 8 or len(password) > 30:
            print('Your password MUST have at least 8 and at most 30 characteres.')
            continue
        elif not any(letter.isupper() for letter in password):
            print('Your password MUST have at least one upper case letter.')
        elif not any(letter.isnumeric() for letter in password):
            print('Your password MUST have at least one number.')
        else:
            password = sha256(password.encode()).hexdigest()
            return password


# CREATING THE PERSON AND INSERTING INTO THE DATABASE
def insert_person():
    try:
        person = Person(name=name(),
                        email=email(),
                        pps=pps(),
                        password=password())
        person.pps += person.name[0:2].upper()
        check = lambda x: session.query(Person).filter(
            Person.email == person.email).first() is not None
        exists = check(person.email)
        if exists:
            print('\033[31mEMAIL ALREADY EXISTS IN THE DATABASE.\033[m')
            raise ValueError
    except:
        print(f'\033[31m{person.name.upper()} NOT ADDED.\033[m')
        session.rollback()
    else:
        session.add(person)
        session.commit()
        print(f'\033[32m{person.name.upper()} ADDED SUCCESSFULLY.\033[m')
    finally:
        session.close()

#################################################################################################################
# DEALING WITH THE AUTHENTICATION
def gen_ac_number():
    from random import randint
    ac = randint(10000000, 99999999)
    return ac


def sign_up():
    print('For sign up please insert your Email and your password: ')
    check = lambda x: session.query(Person).filter(Person.email == x).first() is not None
    email_find = email()
    exists = check(email_find)
    if exists:
        data = session.query(Person).filter(Person.email == email_find).first()
        if data.password == password():
            session.close()
            return [data.name, data.email, data.password, data.id, data.pps]
    else:
        print('\033[31mEMAIL NOT FOUND\033[m')


def create_account():
    check = lambda x: session.query(Person).filter(Person.email == x).first() is not None
    print('Please insert your data once again.')
    email_find = email()
    exists = check(email_find)
    if exists:
        try:
            data = session.query(Person).filter(Person.email == email_find).first()
            if data.password != password():
                print('\033[31mWRONG PASSWORD.\033[m')
                raise ValueError
            id = data.id
            check_id = lambda x: session.query(Account).filter(Account.owner_id == x).first() is not None
            exists_id = check_id(id)
            if exists_id:
                print(f'\033[31m{data.name.upper()} ALREADY HAS A BANK ACCOUNT\033[m')
                raise ValueError
            account = Account(account_number=gen_ac_number(), funds=0 ,owner_id=id)
        except:
            session.rollback()
            print(f'\033[31mOPERATION CANCELLED.\033[m')
        else:
            session.add(account)
            session.commit()
            print(f'\033[32m{data.name.upper()} HAS SUCCESSFULLY CREATED A BANK ACCOUNT WITH THE NUMBER {account.account_number}.\033[m')
        finally:
            session.close()
    else:
        print('\033[31mEMAIL NOT FOUND\033[m')


#################################################################################################################
# DEALING WITH THE BANK OPTIONS
def statement():
    from datetime import datetime
    person = sign_up()
    print(person)
    try:
        data = session.query(Account).filter(Account.owner_id == person[3]).one()
        funds = data.funds
        print('\033[32m='*38)
        print(f'|   {"TEST BANK - STATEMENT":^30}   |')
        print('='*38)
        print(f'|{"":^36}|')
        print(f'|   {"Account Owner":<15}: {person[0][0:13]:<15} |')
        print(f'|   {"PPS Number":<15}: {person[4]:<15} |')
        print(f'|   {"Account Number":<15}: {data.account_number:<15} |')
        print(f'|   {"Funds":<15}: € {funds:<13.2f} |')
        print(f'|{"":^36}|')
        print(f'|{"":^36}|')
        print(f'|   {"For more information":^30}   |')
        print(f'|   {"Contact us":^30}   |')
        print(f'|   {"@TestBank":^30}   |')
        now = datetime.now()
        now = now.strftime("%A %d %B %y %I:%M")
        print(f'|{"":^36}|')
        print(f'|   {now:^30}   |')
        print('='*38, '\033[m')
    except Exception as erro:
        print(erro)
        print('\033[31mINVALID DATA\033[m')


def lodge_cash():
    person = sign_up()
    while True:
        try:
            amount = int(input('Type how much you want to lodge: '))
            assert amount >= 10
        except:
            print('\033[31mInsert a valid amount (more than € 10).\033[m')
            continue
        else:
            data = session.query(Account).filter(Account.owner_id == person[3]).one()
            data.funds += amount
            session.commit()
            session.close()
            print(f'\033[32mYou have successfully lodged € {amount:.2f}\033[m')
            break


def withdraw_cash():
    person = sign_up()
    while True:
        try:
            amount = int(input('Type how much you want to lodge: '))
            assert amount >= 10
        except:
            print('\033[31mInsert a valid amount (more than € 10).\033[m')
            continue
        else:
            data = session.query(Account).filter(Account.owner_id == person[3]).one()
            if data.funds > amount:
                data.funds -= amount
                session.commit()
                session.close()
                print(f'\033[32mYou have successfully withdrawn € {amount:.2f}\033[m')
            else:
                print('\033[31mYou do not have enough money for that transaction\033[m')
                session.rollback()
            break