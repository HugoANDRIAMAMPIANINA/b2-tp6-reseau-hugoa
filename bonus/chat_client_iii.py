import asyncio
from aioconsole import ainput
# from termcolor import colored

global HOST 
HOST = "10.1.1.11"
global PORT
PORT = 8888

async def async_input(writer):
    while True:
        user_message = await ainput("Entrez votre message :\n")
        if user_message == "":
            continue
        
        print(f"Vous avez dit : {user_message}")
        writer.write(user_message.encode())
        await writer.drain()
        
async def async_receive(reader):
    while True:
        server_response = await reader.read(1024)
        if server_response == b'':
            raise Exception("Le serveur s'est déconnecté. Aurevoir")
        
        message = server_response.decode()
        print(f"{message}")
    
        
async def main():
    pseudo = input("Entrez votre pseudo : ")
    
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    
    writer.write(f"Hello|{pseudo}".encode())
    
    tasks = [ async_input(writer), async_receive(reader) ]
    
    await asyncio.gather(*tasks)
    
    
if __name__ == "__main__":
    asyncio.run(main())