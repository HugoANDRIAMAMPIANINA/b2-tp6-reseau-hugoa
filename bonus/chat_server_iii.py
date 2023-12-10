import asyncio
from random import choice
from termcolor import colored
from datetime import datetime
from os.path import isfile, exists
from json import load, dump
from argparse import ArgumentParser
from encoding import encode_message, read_header, read_message, write_message


global CLIENTS
CLIENTS = {}


import json

def store_message(message, number):
    room = str(number)
    history = []
    try:
        with open('history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        pass
    exists = False
    for item in history:
        if item['key'] == room:
            item['value'].append(message)
            exists = True
            break
    if not exists:
        history.append({'key': room, 'value': [message]})
    with open('history.json', 'w') as file:
        json.dump(history, file)

def get_history(number):
    room = str(number)
    try:
        with open('history.json', 'r') as file:
            history = json.load(file)
            for item in history:
                if item['key'] == room:
                    return item['value']
            print('room not found.')
            return None
    except FileNotFoundError:
        print('File not found.')
        return None

async def handle_client_msg(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    header = await read_header(reader)
    data = await read_message(reader, header)
    
    pseudo = ""
    room_number = 0
    if data.decode()[:5] == "Hello":
        room_number = int(data.decode()[6])
        pseudo = data.decode()[8:]
    
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
        CLIENTS[id]["room"] = room_number
        
        colored_pseudo = colored(pseudo, CLIENTS[id]["color"], attrs=['bold'])
            
        print(f"Un nouvel utilisateur {colored_pseudo} ({client_host}:{client_port}) s'est connecté à la chatroom {room_number}")
            
        for client_id in CLIENTS:
            if client_id != id and CLIENTS[client_id]["connected"] and CLIENTS[client_id]["room"] == room_number:
                encoded_message = encode_message(f"Annonce : {colored_pseudo} a rejoint la chatroom {room_number}")
                client_writer = CLIENTS[client_id]["w"]
                await write_message(client_writer, encoded_message)
        
    else:
        # Met à jour le port du client s'il s'est déjà connecté une fois (ip est la même grâce au hash)
        if CLIENTS[id]["addr"] != addr:
            CLIENTS[id]["addr"] = addr
        
        CLIENTS[id]["room"] = room_number
        CLIENTS[id]["w"] = writer
        CLIENTS[id]["r"] = reader
        CLIENTS[id]["connected"] = True
        
        colored_pseudo = colored(pseudo, CLIENTS[id]["color"], attrs=['bold'])
        
        encoded_message = encode_message(f"Welcome back {colored_pseudo} !")
        await write_message(writer, encoded_message)
        
        print(f"L'utilisateur {colored_pseudo} ({client_host}:{client_port}) s'est connecté à la chatroom {room_number}")
            
        for client_id in CLIENTS:
            if client_id != id and CLIENTS[client_id]["connected"] and CLIENTS[client_id]["room"] == room_number:
                encoded_message = encode_message(f"Annonce : {colored_pseudo} est de retour !")
                client_writer = CLIENTS[client_id]["w"]
                await write_message(client_writer, encoded_message)
                
    room_history = get_history(room_number)
    if room_history is not None:
        encoded_history = encode_message(room_history)
        await write_message(writer, encoded_history)
        
    while True:
        header = await read_header(reader)
        
        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime('[%H:%M]')
        if header == b'':
            CLIENTS[id]["connected"] = False
            print(f"L'utilisateur {colored_pseudo} ({client_host}:{client_port}) s'est déconnecté de la chatroom {room_number}")
            for client_id in CLIENTS:
                if CLIENTS[client_id]["connected"] and CLIENTS[client_id]["room"] == room_number:
                    print("nb room : ",room_number)
                    encoded_message = encode_message(f"{formatted_time} Annonce : {colored_pseudo} a quitté la chatroom {room_number}")
                    client_writer = CLIENTS[client_id]["w"]
                    await write_message(client_writer, encoded_message)
            writer.close()
            await writer.wait_closed()
            break
        
        data = await read_message(reader, header)

        message = data.decode()
        print(f"{formatted_time} Chatroom {room_number} Message reçu de {colored_pseudo} ({client_host}:{client_port})  : {message}")
        
        store_message(f"{formatted_time} {colored_pseudo} a dit : {message}", room_number)
        
        for client_id in CLIENTS:
            if client_id != id and CLIENTS[client_id]["connected"] and CLIENTS[client_id]["room"] == room_number:
                encoded_message = encode_message(f"{formatted_time} {colored_pseudo} a dit : {message}")
                client_writer = CLIENTS[client_id]["w"]
                await write_message(client_writer, encoded_message)


async def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", action="store")
    parser.add_argument("-a", "--address", action="store")
    
    args = parser.parse_args()
    
    host, port = args.address, args.port
    
    if (host is None) and (port is None) and exists("config.json") and isfile("config.json"):
        with open('config.json', 'r') as openfile:
            json_object = load(openfile)
        host, port = json_object["host"], json_object["port"]
    
    server = await asyncio.start_server(handle_client_msg, host, port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())