from model import *


def menu1():
    while True:
        try:
            print(f'''\033[1;44m{"MAIN MENU":^100}\033[m\n[1] CREATE A PROFILE\n[2] SIGN UP\n[3] LOGOUT''')
            opt = int(input('Choose your option: '))
            assert opt >=1 and opt <= 3
        except:
            print('\033[31mINVALID OPTION. PLEASE TRY AGAIN\033[m')
            continue
        else:
            if opt == 1:
                insert_person()
            elif opt == 2:
                return opt
            elif opt == 3:
                return opt


def menu2():
    lista = sign_up()
    if lista is None:
        print('\033[31mWRONG PASSWORD OR EMAIL\033[m')
        return 2
    else:
        while True:
            try:
                print(f'''Welcome {lista[0].upper()}\n\033[1;44m{"CUSTOMER MENU":^100}\033[m\n[1] CREATE A BANK ACCOUNT\n[2] ACCESS YOUR BANK ACCOUNT\n[3] LOGOUT''')
                opt = int(input('Choose your option: '))
                assert opt >=1 and opt <= 3
            except:
                print('\033[31mINVALID OPTION. PLEASE TRY AGAIN\033[m')
                continue
            else:
                if opt == 1:
                    create_account()
                elif opt == 2:
                    try:
                        check_account = lambda: session.query(Account).filter(
                            Account.owner_id == lista[3]).first() is not None
                        exists = check_account()
                        if exists:
                            return lista
                        else:
                            raise ValueError
                    except:
                        print('\033[31mACCOUNT NOT FOUND\033[m')
                        continue
                    finally:
                        session.close()
                elif opt == 3:
                    return opt

def menu3():
    while True:
        try:
            print(f'Welcome {opt2[0].upper()}\n\033[1;44m{"BANK ACCOUNT MENU":^100}\033[m\n[1] STATEMENT\n[2] LODGE CASH\n[3] WITHDRAW CASH\n[4] LOGOUT')
            opt = int(input('Choose your option: '))
            assert opt >= 1 and opt <= 4
        except:
            print('\033[31mINVALID OPTION\033[m')
        else:
            if opt == 1:
                statement()
            elif opt == 2:
                lodge_cash()
            elif opt == 3:
                withdraw_cash()
            elif opt == 4:
                return opt
        

# MAIN PROGRAM
while True:
    opt1 = menu1()
    if opt1 == 2:
        opt2 = menu2()
        if opt2 == 3:
            print('Thanks for using our services...')
            break
        elif type(opt2) == list:
            opt3 = menu3()
            if opt3 == 4:
                print('Thanks for using our services...')
                break
    elif opt1 == 3:
        print('Thanks for using our services...')
        break