# Matthew Sherrill, 010956298
import socket
import select

# Create a socket object
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TIMEOUT_VAL = 20.0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12234
server_socket.bind(('localhost', port))
server_socket.listen(1)
userBalance = 100


print(f'Server started up. Starting up balance at ${userBalance}.')
# print(f'Connection created from {client_address}. Balance: ${userBalance}')

# -----------------------------------------------------------------------------

while True:
    # Use select to wait for incoming connections with a timeout of 10 seconds
    ready, _, _ = select.select([server_socket], [], [], TIMEOUT_VAL)
    if not ready:
        print(f'No incoming connections within the last {TIMEOUT_VAL} seconds. Exiting server.')
        break

    client_socket, client_address = server_socket.accept()
    print(f"User connected from {client_address}")
    while True:
        try:
            # Receive and send data
            data = client_socket.recv(1024).decode()  # RECEIVE
            # print(f'Received {data}')

            if not data:
                break

            if 'b' in data:
                print('Received Balance Check.')
                sendBalance = 'r' + str(userBalance)
                client_socket.send(sendBalance.encode())        # SEND
            elif 'd' in data:
                print('Received Deposit')
                add_amt = data.strip('bdrwc')
                userBalance += int(add_amt)
                print(f'Added {add_amt}. New balance: ${userBalance}')

                response = 'y' + str(userBalance)
                client_socket.send(response.encode())           # SEND
                # print(f'Sending {response}.')
            elif 'w' in data:
                print('Received valid withdrawal.')
                sub_amt = data.strip('bdwrc')
                userBalance -= int(sub_amt)
                print(f'Subtracted {sub_amt}. New balance: ${userBalance}')

                response = 'y' + str(userBalance)
                client_socket.send(response.encode())
                # print(f'Sending {response}.')
            elif 'e' in data:
                print('Received ending signal.')
                client_socket.close()
                server_socket.listen(1)
                client_socket, client_address = server_socket.accept()
                # break
        except Exception as e:
            print('Server crashed :( ', e)
            # client_socket.close()
            exit(1)


server_socket.close()
