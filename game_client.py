import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from time import sleep
import threading

client = None
HOST_ADDR = "192.168.0.102"
HOST_PORT = 9090

root = tk.Tk()
root.title("Client/Player")
root.configure(bg="#5E6472")

current_round = 0
total_rounds_count = 5
timer = 3

my_name = ""
my_score = 0
my_choice = ""

other_player_name = ""
other_player_score = 0
other_player_choice = ""

top = tk.Frame(root)
lbl_name = tk.Label(top, text="Name:")
lbl_name.pack(side=tk.LEFT)
player_name = tk.Entry(top)
player_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top, text="Connect", command=lambda: connect_with_server())
btn_connect.pack(side=tk.LEFT)
top.pack(side=tk.TOP)

msg_frame = tk.Frame(root)
msg_frame.configure(bg="#B8F2E6")
lbl_line = tk.Label(msg_frame, text="========================").pack()
lbl_welcome = tk.Label(msg_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(msg_frame, text="===========================")
lbl_line_server.pack_forget()
msg_frame.pack(side=tk.TOP)

top_frame = tk.Frame(root)
name_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green")
lbl_my_name = tk.Label(name_frame, text="Player 1: " + my_name, font="{Segoe UI Black} 10")
sep_lbl = tk.Label(name_frame, text="===========================")
lbl_other_player_name = tk.Label(name_frame, text="Player 2: " + other_player_name, font="{Segoe UI Black} 10")
lbl_my_name.grid(row=0, column=0, padx=5, pady=8)
lbl_other_player_name.grid(row=1, column=0, padx=5, pady=8)
name_frame.pack( padx=(10, 10))

game_round_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green")
sep2_lbl = tk.Label(game_round_frame, text="===========================")
lbl_current_round = tk.Label(game_round_frame, text="Game round (x) starts in", foreground="#6918b4",
                             font="{Segoe UI Black} 14 bold")
lbl_timer = tk.Label(game_round_frame, text=" ", font="{Segoe UI Black} 20 bold", foreground="#6918b4")
lbl_current_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
game_round_frame.pack( padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(root)
sep3_lbl = tk.Label(middle_frame, text="===========================")
lbl_line = tk.Label(middle_frame, text="Leader board", font="{Segoe UI Black} 12 bold", foreground="#57500c").pack()
lbl_line = tk.Label(middle_frame, text="============================").pack()



rock_img = PhotoImage(file=r"rock.png")
paper_img = PhotoImage(file=r"paper.png")
scissor_img = PhotoImage(file=r"scissor.png")
button_frame = tk.Frame(root)
rock_btn = tk.Button(button_frame, command=lambda: choice("rock"), state=tk.DISABLED,
                     image=rock_img)
paper_btn = tk.Button(button_frame,command=lambda: choice("paper"), state=tk.DISABLED,
                      image=paper_img)
scissor_btn = tk.Button(button_frame, command=lambda: choice("scissor"), state=tk.DISABLED,
                        image=scissor_img)
rock_btn.grid(row=0, column=0)
paper_btn.grid(row=0, column=1)
scissor_btn.grid(row=0, column=2)
button_frame.pack(side=tk.TOP)

round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack()
lbl_my_choice = tk.Label(round_frame, text="My choice: " + "None", font="{Segoe UI Black} 14 bold")
lbl_my_choice.pack()
lbl_other_player_choice = tk.Label(round_frame, text="Other player choice: " + "None")
lbl_other_player_choice.pack()
lbl_result = tk.Label(round_frame, text=" ", foreground="#57500c", font="{Segoe UI Black} 14 bold")
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="==============================").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font="{Segoe UI Black} 9 bold", foreground="#57500c")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="==============================").pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()




def game_rules(you, opponent):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissor = "scissor"
    player0 = "you"
    player1 = "opponent"

    if opponent in you:
        winner = "draw"
    elif you == rock:
        if paper in opponent:
            winner = player1
        else:
            winner = player0
    elif you == scissor:
        if rock in opponent:
            winner = player1
        else:
            winner = player0
    elif you == paper:
        if scissor in opponent:
            winner = player1
        else:
            winner = player0
    return winner


def enable_disable_buttons(todo):
    if todo == "disable":
        rock_btn.config(state=tk.DISABLED)
        paper_btn.config(state=tk.DISABLED)
        scissor_btn.config(state=tk.DISABLED)
    else:
        rock_btn.config(state=tk.NORMAL)
        paper_btn.config(state=tk.NORMAL)
        scissor_btn.config(state=tk.NORMAL)


def connect_with_server():
    global my_name
    if len(player_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        my_name = player_name.get()
        lbl_my_name["text"] = "Player 1: " + my_name
        connect_to_server(my_name)


def count_down(my_timer, nothing):
    global current_round
    if current_round <= total_rounds_count:
        current_round = current_round + 1

    lbl_current_round["text"] = "Next round {} in".format(str(current_round))

    while my_timer > 0:
        my_timer = my_timer - 1
        print("game timer is: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Round - " + str(current_round)
    lbl_final_result["text"] = ""


def choice(arg):
    global my_choice, client, current_round
    my_choice = arg
    lbl_my_choice["text"] = "My choice: " + my_choice

    if client:
        client.send("current_round {} {}".format(str(current_round), my_choice).encode())
        enable_disable_buttons("disable")


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, my_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode())  # Send name to server after connecting

        # disable widgets
        btn_connect.config(state=tk.DISABLED)
        player_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons("disable")

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading.Thread(target=receive_message_from_server, args=(client, "m")).start()
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!",
                                message="error" + str(e) + "Cannot connect to host: " + HOST_ADDR + " on port: " + str(
                                    HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(skt, m):
    global my_name, other_player_name, current_round
    global my_choice, other_player_choice, my_score, other_player_score

    while True:
        from_server = skt.recv(4096)

        if not from_server: break

        if from_server.startswith("welcome".encode()):
            if from_server == "welcome1".encode():
                lbl_welcome["text"] = "Welcome {}! \nWaiting for other player".format(my_name)
            elif from_server == "welcome2".encode():
                lbl_welcome["text"] = "Welcome {}! \nGame is starting now!".format(my_name)
            lbl_line_server.pack()

        elif from_server.startswith("other_player_name".encode()):
            other_player_name = from_server.decode().replace("other_player_name", "")
            lbl_other_player_name["text"] = "Player 2: " + other_player_name
            top_frame.pack()
            middle_frame.pack()

            # we know two users are connected so game is ready to start
            threading.Thread(target=count_down, args=(timer, "")).start()
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("other_player_choice".encode()):
            # get the opponent choice from the server
            other_player_choice = from_server.decode().replace("other_player_choice", "")

            # figure out who wins in this round
            who_wins = game_rules(my_choice, other_player_choice)
            round_result = " "
            if who_wins == "you":
                my_score = my_score + 1
                round_result = "WIN"
            elif who_wins == "opponent":
                other_player_score = other_player_score + 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            # Update GUI
            lbl_other_player_choice["text"] = "Opponent choice: " + other_player_choice
            lbl_result["text"] = "Result: " + round_result

            # is this the last round e.g. Round 5?
            if current_round == total_rounds_count:
                # compute final result
                final_result = ""
                color = ""

                if my_score > other_player_score:
                    final_result = "(You Won!!!)"
                    color = "green"
                elif my_score < other_player_score:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "black"

                lbl_final_result["text"] = "FINAL RESULT: " + str(my_score) + " - " + str(
                    other_player_score) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                current_round = 0

            # Start the timer
            threading.Thread(target=count_down, args=(timer, "")).start()

    skt.close()


root.mainloop()
