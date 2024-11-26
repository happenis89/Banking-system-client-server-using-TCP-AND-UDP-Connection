import socket
import threading

# Server configuration
SERVER_IP = '192.168.56.1'  # Replace with your server's IP
SERVER_PORT = 12345
UDP_PORT = 54321

# Mock database for user details and balances
users = {"user1": "pass1", "user2": "pass2"}
accounts = {"user1": 1000, "user2": 2000}

# To store active client addresses for notifications
client_addresses = {}
lock = threading.Lock()

def handle_client(client_sock, addr):
    print(f"Connection from {addr}")
    username = None
    authenticated = False
    client_udp_port = None
    
    while True:
        try:
            data = client_sock.recv(1024).decode()
            
            if not data:
                break
            
            if data.startswith("SIGNUP"):
                # Handle new user registration
                _, new_username, password, mobile_number = data.split()
                with lock:
                    if new_username in users:
                        client_sock.send("Username already exists".encode())
                    else:
                        users[new_username] = password
                        accounts[new_username] = 0  # Initialize balance
                        client_sock.send("Sign Up successful".encode())
            
            elif data.startswith("LOGIN"):
                # Handle user login
                _, username, password, client_udp_port = data.split()
                client_udp_port = int(client_udp_port)
                with lock:
                    if username in users and users[username] == password:
                        authenticated = True
                        client_addresses[username] = (addr[0], client_udp_port)  # Track client UDP address
                        client_sock.send("Login successful".encode())
                    else:
                        client_sock.send("Invalid credentials".encode())
            
            elif data == "VIEW_DETAILS":
                # Show account details if logged in
                if authenticated:
                    client_sock.send(f"Account Details: Username: {username}, Balance: ${accounts[username]}".encode())
                else:
                    client_sock.send("Please log in first.".encode())
            
            elif data.startswith("TRANSFER"):
                # Handle fund transfer if logged in
                if authenticated:
                    _, amount, recipient_username = data.split()
                    amount = float(amount)
                    with lock:
                        if accounts[username] >= amount and recipient_username in users:
                            accounts[username] -= amount
                            accounts[recipient_username] += amount
                            client_sock.send(f"Transferred {amount} to {recipient_username}. New balance: {accounts[username]}".encode())
                            
                            # Send UDP notification to the recipient if online
                            if recipient_username in client_addresses:
                                recipient_addr = client_addresses[recipient_username]
                                notification = f"You received ${amount} from {username}"
                                send_udp_notification(recipient_addr, notification)

                            # Server notification
                            print(f"Transaction Notification: {username} transferred ${amount} to {recipient_username}.")
                            print(f"Updated Balances - {username}: ${accounts[username]}, {recipient_username}: ${accounts[recipient_username]}")
                        else:
                            client_sock.send("Insufficient balance or recipient not found.".encode())
                else:
                    client_sock.send("Please log in first.".encode())
            
            elif data == "CHECK_BALANCE":
                # Send balance information if logged in
                if authenticated:
                    client_sock.send(f"Balance: ${accounts[username]}".encode())
                else:
                    client_sock.send("Please log in first.".encode())

            elif data.startswith("DELETE_ACCOUNT"):
                # Handle account deletion
                _, del_username, del_password = data.split()
                with lock:
                    if del_username in users and users[del_username] == del_password:
                        del users[del_username]
                        del accounts[del_username]
                        client_sock.send("Account deleted successfully.".encode())
                        print(f"Account Deleted: {del_username}")  # Server side notification
                        # Notify other clients
                        for client in client_addresses:
                            if client != del_username:
                                notification = f"Account {del_username} has been deleted."
                                send_udp_notification(client_addresses[client], notification)
                    else:
                        client_sock.send("Invalid username or password. Account deletion failed.".encode())

            elif data == "EXIT":
                print(f"Client {addr} disconnected.")
                break
        
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break
    
    # Clean up on client disconnect
    if username:
        with lock:
            client_addresses.pop(username, None)
    client_sock.close()
    print(f"Server connection closed for {addr}.")

def send_udp_notification(client_addr, message):
    """Send a real-time notification via UDP to the specified client address."""
    try:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.sendto(message.encode(), client_addr)
        udp_sock.close()
    except Exception as e:
        print(f"Error sending UDP notification: {e}")

def start_server():
    # Set up the TCP server
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.listen(5)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        client_sock, addr = server_sock.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
