import asyncio
from aioconsole import ainput

global HOST 
HOST = "10.1.1.11"
global PORT
PORT = 8888

async def async_input(writer):
    while True:
        user_message = await ainput()
        if user_message == "":
            continue
        
        writer.write(user_message.encode())
        await writer.drain()
        
async def async_receive(reader):
    while True:
        server_response = await reader.read(1024)
        if server_response == b'':
            continue
        
        print(f"{server_response.decode()}\n")
    
        
async def main():
    pseudo = input("Entrez votre pseudo : ")
    
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    
    writer.write(f"Hello|{pseudo}".encode())
    writer.drain()
    
    tasks = [ async_input(writer), async_receive(reader) ]
    
    await asyncio.gather(*tasks)
    
    
if __name__ == "__main__":
    asyncio.run(main())