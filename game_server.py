import socket
import tkinter as tk
import threading
from time import sleep

HOST_ADDR = "192.168.0.102"
HOST_PORT = 9090

#UI
root = tk.Tk()
root.title("Server")
root.configure(bg="#5E6472")

top = tk.Frame(root)
start_btn = tk.Button(top, text="Start", command=lambda: run_server())
start_btn.pack(side=tk.LEFT)
stop_btn = tk.Button(top, text="Stop", command=lambda: stop_server(), state=tk.DISABLED)
stop_btn.pack(side=tk.LEFT)
top.pack(side=tk.TOP, pady=(4, 4))

add_port_frame = tk.Frame(root)
host_lbl = tk.Label(add_port_frame, text="Host Address:")
host_lbl.pack(side=tk.LEFT)
port_lbl = tk.Label(add_port_frame, text="Port:")
port_lbl.pack(side=tk.LEFT)
add_port_frame.pack(side=tk.TOP, pady=(4, 4))

client_list_frame = tk.Frame(root)
lblLine = tk.Label(client_list_frame, text="Connected Clients").pack()
sb = tk.Scrollbar(client_list_frame)
sb.pack(side=tk.RIGHT, fill=tk.Y)
display = tk.Text(client_list_frame, height=10, width=30)
display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
sb.config(command=display.yview)
display.config(yscrollcommand=sb.set, background="#B8F2E6", state="disabled")
client_list_frame.pack(side=tk.BOTTOM, pady=(4, 4))

server = None
client_name = " "
clients_list = []
clients_names = []
player_data = []

def run_server():
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(4) 
    print("AF_INET:{}, SOCK_STREAM:{}".format(socket.AF_INET, socket.SOCK_STREAM))
    print("server started successfully...")
    threading.Thread(target=accept_clients, args=(server, " ")).start()

    host_lbl["text"] = "Host Address: {}".format(HOST_ADDR)
    port_lbl["text"] = "Port: {}".format(str(HOST_PORT))

def stop_server():
    global server
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    print("server stopped")


def accept_clients(current_server, nothing):
    while True:
        if len(clients_list) < 2:
            print("accepting clients...")
            client, address = current_server.accept()
            clients_list.append(client)
            threading.Thread(target=client_communication, args=(client, address)).start()


# Function to receive message from current client AND
# Send that message to other clients_list
def client_communication(client_connection, add):
    global server, client_name, clients_list, player_data, player_0, player_1
    client_name = client_connection.recv(4096)
    if len(clients_list) < 2:
        client_connection.send("welcome1".encode())
    else:
        client_connection.send("welcome2".encode())

    clients_names.append(client_name)
    client_display_update(clients_names)

    if len(clients_list) > 1:
        sleep(1)
        clients_list[0].send("other_player_name: {}".format(str(clients_names[1])).encode())
        clients_list[1].send("other_player_name: {}".format(str(clients_names[0])).encode())

    while True:
        data = client_connection.recv(4096)
        if not data:
            break

        player_choice = data[11:len(data)]
        msg = {
            "choice": player_choice,
            "socket": client_connection}

        if len(player_data) < 2:
            player_data.append(msg)

        if len(player_data) == 2:
            player_data[0].get("socket").send("other_player_choice: {}".format(player_data[1].get("choice")).encode())
            player_data[1].get("socket").send("other_player_choice: {}".format(player_data[0].get("choice")).encode())

            player_data = []

    index = get_client_idx(clients_list, client_connection)
    del clients_names[index]
    del clients_list[index]
    client_connection.close()
    client_display_update(clients_names)  # update client names display

def get_client_idx(client_list, current_client):
    index = 0
    for connection in client_list:
        if connection == current_client:
            break
        index = index + 1
    return index

def client_display_update(clients_names):
    display.config(state=tk.NORMAL)
    display.delete('1.0', tk.END)

    for c in clients_names:
        display.insert(tk.END, "{} \n".format(str(c)))
    display.config(state=tk.DISABLED)

root.mainloop()
