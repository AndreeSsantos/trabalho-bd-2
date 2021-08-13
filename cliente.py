from tkinter import *
from tkinter import ttk
import socket
import json

HEADER = 32 # Toda msg do cliente pro servidor tem um header de 32 bytes dizendo o tamanho da msg enviada
PORT = 5000
FORMAT = 'utf-8'
NOME = ''
CONECTADO = False
REGISTRADO = False

root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))
text = Text(content, borderwidth=5, relief="ridge", width=50, height=25)
text.insert('1.0', socket.gethostbyname(socket.gethostname())+'\n')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Método pra lidar com as respostas do servidor
def handle_server_response(msg, res_msg):
    global REGISTRADO
    global CONECTADO
    global NOME

    if res_msg == "Este usuário já existe, tente outro.":
        None
    if res_msg == "Usuario registrado com sucesso":
        msg = json.loads(msg)
        NOME = msg['name']
        REGISTRADO = True
    if res_msg == "Desconectado":
        client.close()
        REGISTRADO = False
        CONECTADO = False
        NOME = ''

# método pra enviar as msg ao servidor de registros
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    response_msg = client.recv(1024).decode(FORMAT)
    text.insert('1.0', f"Msg recebida: {response_msg}\n")
    handle_server_response(msg, response_msg)

# Esse método é executado ao apertar o botão (conectar)
def conectar():
    global CONECTADO
    global REGISTRADO
    global client
    #Conecta ao servidor de registros
    if CONECTADO == False:
        text.insert('1.0', f"Conectando ao host ({server_entry.get()})\n")
        ADDR = (server_entry.get(), PORT)
        x = 0
        while x < 2 :
            try:
                client.connect(ADDR)
                CONECTADO = True
                x = 2
            except ConnectionRefusedError:
                text.insert('1.0', f"Conexão ao host ({server_entry.get()}) foi recusada\n")
                x = 2
            except OSError:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                x +=1
    # Registra o nome de usuário
    if REGISTRADO == False and CONECTADO == True:
        text.insert('1.0', f"Registrando usuário ({name_entry.get()})\n")
        mensagem = {'type': 'new_user', 'name': name_entry.get()}
        send(json.dumps(mensagem))

# Esse método é executado ao apertar o botão (consultar)
def consultar():
    global CONECTADO
    if CONECTADO:
        text.insert('1.0', f"Consultando ({consulta_entry.get()})\n")
        mensagem = {'type': 'consulta_user', 'name': consulta_entry.get()}
        send(json.dumps(mensagem))

# Esse método é executado ao apertar o botão (desconectar)
def desconectar():
    global NOME
    if NOME != '':
        text.insert('1.0', f"Desconectando\n")
        mensagem = {'type': 'disconnect', 'name': NOME}
        send(json.dumps(mensagem))


##### Interface Gráfica
server_lbl = ttk.Label(content, text="Server")
server_entry = ttk.Entry(content)
name_lbl = ttk.Label(content, text="Name", )
name_entry = ttk.Entry(content)
con_btn = Button(content, text="Conectar", command=conectar)

consulta_lbl = ttk.Label(content, text="Name", )
consulta_entry = ttk.Entry(content)
consulta_btn = Button(content, text="Consultar", command=consultar)

ok = Button(content, text="Okay")
desc_btn = Button(content, text="Desconectar", command=desconectar)

content.grid(column=0, row=0, sticky=(N, S, E, W))
text.grid(column=0, row=0, columnspan=3, rowspan=30, sticky=(N, S, E, W))

name_lbl.grid(column=3, row=0, sticky=(N))
name_entry.grid(column=3, row=1, sticky=(N,E,W), pady=5, padx=5)
server_lbl.grid(column=4, row=0, sticky=(N))
server_entry.grid(column=4, row=1, sticky=(N,E,W), pady=5, padx=5)
con_btn.grid(column=3, row=2, columnspan=2, sticky=(N, E, W), pady=5, padx=5)

consulta_lbl.grid(column=3, row=3, columnspan=2, sticky=(N))
consulta_entry.grid(column=3, row=4, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
consulta_btn.grid(column=3, row=5, columnspan=2, sticky=(N, E, W), pady=5, padx=5)

ok.grid(column=3, row=6, sticky=(N, E, W), pady=5, padx=5)
desc_btn.grid(column=4, row=6, sticky=(N, E, W), pady=5, padx=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(5, weight=1)

root.mainloop()