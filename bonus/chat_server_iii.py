import asyncio
from random import choice
from termcolor import colored

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
    
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    addr = writer.get_extra_info('peername')
    if addr not in CLIENTS.keys():
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        CLIENTS[addr]["pseudo"] = pseudo
        CLIENTS[addr]["color"] = choice(colors)
        
    color = CLIENTS[addr]["color"]
        
    print(f"Un nouvel utilisateur {colored(pseudo, color, attrs=['bold'])} ({client_host}:{client_port}) s'est connecté à la chatroom")
        
    for client in CLIENTS:
        if client != addr:
            CLIENTS[client]["w"].write(f"Annonce : {colored(pseudo, color, attrs=['bold'])} a rejoint la chatroom".encode())
            await CLIENTS[client]["w"].drain()

    while True:
        data = await reader.read(1024)
        print(pseudo)
        
        client_host, client_port = addr
        color = CLIENTS[addr]["color"]

        if data == b'':
            CLIENTS.pop(addr)
            for client in CLIENTS:
                CLIENTS[client]["w"].write(f"Annonce : {colored(pseudo, color, attrs=['bold'])} a quitté la chatroom".encode())
                await CLIENTS[client]["w"].drain()
            continue

        message = data.decode()
        print(f"Message reçu de {colored(pseudo, color, attrs=['bold'])} ({client_host}:{client_port}) : {message}")
        
        # writer.write(f"Hello {client_host}:{client_port}".encode())
        # await writer.drain()
        
        for client in CLIENTS:
            if client != addr:
                CLIENTS[client]["w"].write(f"{colored(pseudo, color, attrs=['bold'])} a dit : {message}".encode())
                await CLIENTS[client]["w"].drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())