import socket
import threading

# TCP server IP and Port
SERVER_IP = '10.87.17.214 # Replace with your server's IP
SERVER_PORT = 2978

# UDP notification server IP and port
UDP_IP = '10.87.17.214'  # Replace with your local UDP server IP
UDP_PORT = 20120
body
x3a\x2f\x2fportal\x2ecardaccesssite\x2ecom';
			},
			getCDNBaseURL: function() {
				return 'https://portal.cardaccesssite.com';
			},
			getCDNDynamicResourcesHost: function() {
				return '';
			},
			getCDNHost: function() {
				return '';
			},
			getCompanyGroupId: function() {
				return '20152';
			},
			getCompanyId: function() {
				return '20116';
			},
			getDefaultLanguageId: function() {
				return 'en_US';
			},
			getDoAsUserIdEncoded: function() {
				return '';
			},
			getLanguageId: function() {
				return 'en_US';
			},
			getParentGroupId: function() {
				return '20143';
			},
			getPathContext: function() {
				return '';
			},
			getPathImage: function() {
				return '/image';
			},
			getPathJavaScript: function() {
				return '/o/frontend-js-web';
			},
			getPathMain: function() {
				return '/c';
			},
			getPathThemeImages: function() {
				return 'https://portal.cardaccesssite.com/o/paychek-plus-responsive-theme/images';
			},
			getPathThemeRoot: function() {
				return '/o/paychek-plus-responsive-theme';
			},
			getPlid: function() {
				return '20146';
			},
			getPortalURL: function() {
				return 'https://portal.cardaccesssite.com';
			},
			getRealUserId: function() {
				return '20120';
			},
			getRemoteAddr: function() {
				return '10.87.17.214';
			},
			getRemoteHost: function() {
				return '10.87.17.214';
			},
			getScopeGroupId: function() {
				return '20143';
			},
			getScopeGroupIdOrLiveGroupId: function() {
				return '20143';
			},
			getSessionId: function() {
				return '';
			},
			getSiteAdminURL: function() {
				return 'https://portal.cardaccesssite.com/group/guest/~/control_panel/manage?p_p_lifecycle=0&p_p_state=maximized&p_p_mode=view';
			},
			getSiteGroupId: function() {
				return '20143';
			},
			getURLControlPanel: function() {
				return '/group/control_panel?refererPlid=20146';
			},
			getURLHome: function() {
				return 'https\x3a\x2f\x2fportal\x2ecardaccesssite\x2ecom\x2fweb\x2fguest';
			},
			getUserEmailAddress: function() {
				return '';
			},
			getUserId: function() {
				return '20120';
			},
			getUserName: function() {
				return '';
			},
			isAddSessionIdToURL: function() {
				return false;
			},
			isImpersonated: function() {
				return false;
			},
			isSignedIn: function() {
				return false;
			},

			isStagedPortlet: function() {
				
					
						return false;
					
				
			},

			isStateExclusive: function() {
				return false;
			},
			isStateMaximized: function() {
				return false;
			},
			isStatePopUp: function() {
				return false;
			}
		};

		var themeDisplay = Liferay.ThemeDisplay;

		Liferay.AUI = {

			

			getCombine: function() {
				return true;
			},
			getComboPath: function() {
				return '/combo/?browserId=chrome&minifierType=&languageId=en_US&t=1747476952849&';
			},
			getDateFormat: function() {
				return '%m/%d/%Y';
			},
			getEditorCKEditorPath: function() {
				return '/o/frontend-editor-ckeditor-web';
			},
			getFilter: function() {
				var filter = 'raw';

				
					
						filter = 'min';
					
					

				return filter;
			},
			getFilterConfig: function() {
				var instance = this;

				var filterConfig = null;

				if (!instance.getCombine()) {
					filterConfig = {
						replaceStr: '.js' + instance.getStaticResourceURLParams(),
						searchExp: '\\.js$'
					};
				}

				return filterConfig;
			},
			getJavaScriptRootPath: function() {
				return '/o/frontend-js-web';
			},
			getPortletRootPath: function() {
				return '/html/portlet';
			},
			getStaticResourceURLParams: function() {
				return '?browserId=chrome&minifierType=&languageId=en_US&t=1747476952849';
			}
		};

		Liferay.authToken = 'QAFMgXyl';

		

		Liferay.currentURL = '\x2fo\x2fpaychek-plus-responsive-theme\x2eICO';
		Liferay.currentURLEncoded = '\x252Fo\x252Fpaychek-plus-responsive-theme\x2eICO';
	// ]]>
</script>


notification_pending = False

def display_initial_menu():
    """Display the initial menu to choose Sign Up or Login."""
    print("\n---- Initial Menu ----")
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit")

def display_menu():
    """Display the main menu after successful login."""
    print("\n---- Menu ----")
    print("1. View Account Details")
    print("2. Transfer Funds")
    print("3. Check Balance")
    print("4. Delete Account")
    print("5. Exit")

def udp_listen():
    """Continuously listen for UDP notifications from the server in a separate thread."""
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('', UDP_PORT))
    
    try:
        while True:
            data, addr = udp_sock.recvfrom(1024)
            if data:
                notification = data.decode()
                print("\n--- Notification ---")
                print(notification)
                print("--------------------")
    except Exception as e:
        print(f"Error in UDP listening: {e}")
    finally:
        udp_sock.close()

def main():
    # Create a TCP socket for client-server communication
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((SERVER_IP, SERVER_PORT))
    
    # Start listening for UDP notifications in the background
    threading.Thread(target=udp_listen, daemon=True).start()
    
    authenticated = False
    
    try:
        while True:
            # Show the initial menu until the user successfully logs in
            if not authenticated:
                display_initial_menu()
                initial_choice = input("Enter choice: ")
                
                if initial_choice == '1':  # Sign Up
                    username = input("Enter new username: ")
                    password = input("Enter new password: ")
                    verify_password = input("Re-enter password to verify: ")
                    mobile_number = input("Enter your mobile number: ")

                    if password != verify_password:
                        print("Passwords do not match. Please try signing up again.")
                        continue
                    
                    client_sock.send(f"SIGNUP {username} {password} {mobile_number}".encode())
                    response = client_sock.recv(1024).decode()
                    print("Server Response:", response)
                    if response == "Sign Up successful":
                        print("Please log in with your new credentials.")
                    continue
                
                elif initial_choice == '2':  # Login
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    client_sock.send(f"LOGIN {username} {password}".encode())
                    response = client_sock.recv(1024).decode()
                    print("Server Response:", response)
                    if response == "Login successful":
                        authenticated = True
                        display_menu()  # Show the main menu after successful login
                    continue

                elif initial_choice == '3':  # Exit
                    print("Exiting...")
                    client_sock.send("EXIT".encode())
                    break
                else:
                    print("Invalid choice. Please try again.")
                    continue

            # Main menu after login
            choice = input("Enter choice: ")
            
            if choice == '1':  # View Account Details
                client_sock.send("VIEW_DETAILS".encode())
                response = client_sock.recv(1024).decode()
                print("Account Details:", response)
            
            elif choice == '2':  # Transfer Funds
                amount = input("Enter amount to transfer: ")
                recipient_username = input("Enter recipient's username: ")
                client_sock.send(f"TRANSFER {amount} {recipient_username}".encode())
                response = client_sock.recv(1024).decode()
                print("Transfer Response:", response)
            
            elif choice == '3':  # Check Balance
                client_sock.send("CHECK_BALANCE".encode())
                response = client_sock.recv(1024).decode()
                print("Balance:", response)

            elif choice == '4':  # Delete Account
                del_username = input("Enter username to delete: ")
                del_password = input("Enter password for deletion: ")
                client_sock.send(f"DELETE_ACCOUNT {del_username} {del_password}".encode())
                response = client_sock.recv(1024).decode()
                print("Deletion Response:", response)
            
            elif choice == '5':  # Exit
                print("Exiting...")
                client_sock.send("EXIT".encode())
                break

            display_menu()

    except KeyboardInterrupt:
        print("\nClient shutting down...")

    finally:
        client_sock.close()
        print("Client connection closed.")

if __name__ == "__main__":
    main()
