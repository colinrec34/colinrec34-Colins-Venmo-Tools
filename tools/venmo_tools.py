#This is a toolbox of venmo functions
from venmo_api import Client

import tools.json_tools as json_tools
import tools.csv_tools as csv_tools

#======================================Login/Logout======================================
def login(username='', password='', token=''):
    global client
    try:
        client = Client(access_token=token)
    except:
        print("Invalid Access Token; attempting to get token with OTP...")
        #tkinter.simpledialog.askstring("Enter OTP", "Enter the OTP sent by Venmo:")
        try: 
            token = Client.get_access_token(username=username, password=password)
            client = Client(access_token=token)
        except:
            print('Login Failed')
            raise ConnectionRefusedError
    print(f'Login Success! ({client.user.get_my_profile().username})')
    if json_tools.load_setting("remember"):
        json_tools.write("remember", True)
    json_tools.write("token", str(token))
    return client, token
#-------------------------------------------------------------------------------------------
def logout() -> None: 
    client.log_out(access_token=json_tools.load_setting('token'))
    print("Successfully Revoked Access Token and Logged Out")

#==================================Retrieval (Get) Commands===================================
def getTransactions():
    my_id = client.user.get_my_profile().id
    return client.user.get_user_transactions(my_id)
#-------------------------------------------------------------------------------------------
def get_username_list():
    with open('./config/users.txt', 'r') as file:
        return file.read().splitlines()
    
#=================================Equal Split Requesting======================================
def requestEqualSplit(totalAmount, note, usernameList=get_username_list(), include=True):
    if include:
        splitAmount = totalAmount/(len(usernameList)+1)
    else:
        splitAmount = totalAmount/(len(usernameList))
    targetUsers = []
    for username in usernameList:
        targetUsers.append(client.user.get_user_by_username(username=username))
    
    for target in targetUsers:
        client.payment.request_money(splitAmount, note, target.id)
        print(f'Requested ${splitAmount:.2f} from {target.first_name} for {note}')
    return splitAmount, note, [target for target in targetUsers]

#========================Default Mass Requests (Not Implemented)========================
def monthlyRequest(monthMessage, include, term=False):
    if term:
        username = input('Username: ')
        password = input('Password: ')
        login(username=username, password=password)
    usernames = ["QuinnCarlson26", "Fineas-Herrera", "Ben-Kinkor", "Lucas-Johnson-175", "Noah-Lau-3", "jj-timo"]
    print('Requesting for the month {monthMessage}')
    requestEqualSplit(2000, monthMessage+ ' Rent', usernames, include)
    requestEqualSplit(100, monthMessage+ ' Utilities', usernames, include)
    requestEqualSplit(65, monthMessage+ ' Internet', usernames, include)
    print(f'The regular request for {monthMessage} has been completed!')
    logout()

#==================================Record Functions (Incomplete)===================================
