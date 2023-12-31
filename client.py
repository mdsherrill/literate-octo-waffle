# Matthew Sherrill, 010956298
import socket

# Setup socket information
client_socket = socket.socket()
port = 12234
client_socket.connect(('localhost', port))

def printMenu():
    choice = "null"
    while choice != '4':
        print('''
        -----------------------------------------------------------------------------
        --------------------     Welcome to SherrillATM!       ----------------------
        -----------------------------------------------------------------------------\n
        Please choose from one of the following options:
        1: Deposit
        2: Withdrawal
        3: Check Balance
        4: Exit SherrillATM
        ''')
        choice = input('Enter your choice: ')

        if choice == '1':
            deposit()
        elif choice == '2':
            withdrawal()
        elif choice == '3':
            tempBal = checkBalance()
            print(f'Your balance is ${tempBal}.')
        elif choice == '4':
            client_socket.sendall('e'.encode())
            print("Closing SherrillATM...")
            client_socket.close()  # Close connection to server
            exit()
        else:
            choice = input('You did not choose one of the options. Try again: ')
            continue

def deposit():
    # print('In deposit.')
    while True:
        depAmount = input('Please enter the amount for deposit: ')

        try:
            depAmount = int(depAmount)
        except ValueError:
            print('Invalid input. Please input a valid integer.')
            continue

        if depAmount < 0:
            print('Invalid input. Deposit cannot be negative.')
            continue
        else:
            break

    dep_send = 'd' + str(depAmount)
    # print(f'Sending {dep_send}')
    client_socket.send(dep_send.encode())  # Sending deposit amount to the server, to add to the balance.

    response = client_socket.recv(1024).decode()
    # print(f'Response from server: {response}')
    if 'y' in response:
        print(f'${depAmount} was successfully deposited into your account.')
    else:
        print("Deposit failed to reach server.")

def withdrawal():
    # Check to see balance for error checking
    serverBal = checkBalance()
    while True:
        drawAmount_str = input('Please enter the amount for withdrawal: ')

        try:
            drawAmount = int(drawAmount_str)
        except ValueError:
            print('Invalid input. Please enter a valid integer.')
            continue

        if drawAmount < 0:
            print('Withdrawal amount cannot be negative.')
            continue
        elif drawAmount > serverBal:
            print('Insufficient funds. Enter a smaller amount.')
            continue
        else:
            break

    drawSent = 'w' + drawAmount_str
    client_socket.send(drawSent.encode())

    response = client_socket.recv(1024).decode()
    # print(f'Response from server: {response}')
    if 'y' in response:
        print(f'${drawAmount_str} was successfully withdrawn into your account.')
    else:
        print("Deposit failed to reach server.")

def checkBalance():
    client_socket.send('b'.encode())
    balance = client_socket.recv(1024).decode() # s
    if 'r' in balance:
        balance = balance.strip('bdwrc')
        # print(f'Your balance is {balance}.')
    return int(balance)


printMenu()
