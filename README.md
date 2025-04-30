# Rock Paper Scissors - Distributed Systems Game 🎮🌐

This is a two-player Rock Paper Scissors game built using Python sockets and Tkinter. It demonstrates the core concepts of distributed systems including client-server architecture, concurrency with threading, and message passing over TCP.

## 🧠 Features

- Two-player real-time gameplay
- TCP-based client-server communication
- Multithreaded handling of client connections
- GUI for both server and players using Tkinter
- Round-based gameplay with score tracking

## 🧱 Technologies Used

- Python 3
- Sockets (TCP)
- Tkinter (GUI)
- Threading

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/ramishamunir/rock_paper_scissors_ds_game.git
cd rock_paper_scissors_ds_game
```


### 2. Run the server
```
python game_server.py
```

### 3. Run each client (on same or different machine within LAN)
```
python game_client.py
```

🔗 Note:
Make sure the HOST_ADDR in both files is set to the server machine’s IP.

Also ensure the image files (rock.png, paper.png, scissor.png) are present in the same folder.

📚 Course Context:

This project was developed as part of a Distributed Systems course to demonstrate basic concepts through a practical, interactive multiplayer game in September, 2022


