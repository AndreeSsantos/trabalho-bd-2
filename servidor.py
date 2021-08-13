import socket 
import threading
import json

HEADER = 32 # Toda msg do cliente pro servidor tem um header de 32 bytes dizendo o tamanho da msg enviada
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname()) # 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
USERS = [] # Registro de usuários, [nome, server, porta]

def handle_client(conn, addr):
    print(f"[Nova Conexão] {addr} conectado.")

    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)            
            msg = json.loads(msg)
            print(f"Msg recebida de [{addr}],  {msg}")
            
            ## Disconecta o usuário e remove o registro.
            if msg['type'] == 'disconnect':
                for user in USERS:
                    if user[0] == msg['name']:
                        USERS.remove(user)
                conn.send("Desconectado".encode(FORMAT))
                conn.close()
                break

            ## Adiciona novo usuário
            if msg['type'] == 'new_user':
                teste = True
                for user in USERS:
                    #Usuário já existe
                    if user[0] == msg['name']:
                        conn.send("Este usuário já existe, tente outro.".encode(FORMAT))
                        teste = False
                        break
                # Usuário criado com sucesso.
                if teste:
                    USERS.append([msg['name'], addr[0], addr[1]])
                    conn.send("Usuario registrado com sucesso".encode(FORMAT))
                print(USERS)

            ## Consulta se o usuário está cadastrado
            if msg['type'] == 'consulta_user':
                teste = True
                for user in USERS:
                    if user[0] == msg['name']:
                        conn.send(f"{msg['name']} --> [{user[1]}] {user[2]}".encode(FORMAT))
                        teste = False
                        break
                if teste:
                    conn.send("Usuario nao cadastrado".encode(FORMAT))         

#Inicializa o servidor, cria uma thread pra cada cliente.
def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Servidor escutando em {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # cria uma thread pra cada cliente
        thread.start()

start()