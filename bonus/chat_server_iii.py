import asyncio
from random import choice
from termcolor import colored
from datetime import datetime

global HOST 
HOST = "10.1.1.11"
global PORT
PORT = 8888
global CLIENTS
CLIENTS = {}

async def handle_client_msg(reader, writer):
    data = await reader.read(1024)
    pseudo = ""
    if data.decode()[:5] == "Hello":
        pseudo = data.decode()[6:]
    
    addr = writer.get_extra_info('peername')
    
    client_host, client_port = addr
    id = hash(client_host + pseudo)
    
    colored_pseudo = ""
    
    if id not in CLIENTS.keys():
        colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
        
        CLIENTS[id] = {}
        CLIENTS[id]["r"] = reader
        CLIENTS[id]["w"] = writer
        CLIENTS[id]["addr"] = addr
        CLIENTS[id]["pseudo"] = pseudo
        CLIENTS[id]["color"] = choice(colors)
        CLIENTS[id]["connected"] = True
        
        colored_pseudo = colored(pseudo, CLIENTS[id]["color"], attrs=['bold'])
            
        print(f"Un nouvel utilisateur {colored_pseudo} ({client_host}:{client_port}) s'est connecté à la chatroom")
            
        for client_id in CLIENTS:
            if client_id != id and CLIENTS[client_id]["connected"]:
                CLIENTS[client_id]["w"].write(f"Annonce : {colored_pseudo} a rejoint la chatroom".encode())
                await CLIENTS[client_id]["w"].drain()
    else:
        # Met à jour le port du client s'il s'est déjà connecté une fois (ip est la même grâce au hash)
        if CLIENTS[id]["addr"] != addr:
            CLIENTS[id]["addr"] = addr
        
        CLIENTS[id]["w"] = writer
        CLIENTS[id]["r"] = reader
        CLIENTS[id]["connected"] = True
        colored_pseudo = colored(pseudo, CLIENTS[id]["color"], attrs=['bold'])    
        
        writer.write(f"Welcome back {colored_pseudo} !".encode())
        await writer.drain()
        
        print(f"L'utilisateur {colored_pseudo} ({client_host}:{client_port}) s'est connecté à la chatroom")
            
        for client_id in CLIENTS:
            if client_id != id and CLIENTS[client_id]["connected"]:
                CLIENTS[client_id]["w"].write(f"Annonce : {colored_pseudo} est de retour !".encode())
                await CLIENTS[client_id]["w"].drain()
        
    while True:
        data = await reader.read(1024)
        
        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime('[%H:%M]')

        if data == b'':
            CLIENTS[id]["connected"] = False
            for client_id in CLIENTS:
                if CLIENTS[client_id]["connected"]:
                    CLIENTS[client_id]["w"].write(f"{formatted_time} Annonce : {colored_pseudo} a quitté la chatroom".encode())
                    await CLIENTS[client_id]["w"].drain()
            writer.close()
            await writer.wait_closed()
            continue

        message = data.decode()
        print(f"{formatted_time} Message reçu de {colored_pseudo} ({client_host}:{client_port}) : {message}")
        
        for client_id in CLIENTS:
            if client_id != id and CLIENTS[client_id]["connected"]:
                CLIENTS[client_id]["w"].write(f"{formatted_time} {colored_pseudo} a dit : {message}".encode())
                await CLIENTS[client_id]["w"].drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())