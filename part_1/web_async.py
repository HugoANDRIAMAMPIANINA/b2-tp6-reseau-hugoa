from sys import argv
import asyncio
import aiohttp
import aiofiles

async def get_content(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content = await resp.read()
                return content

    except Exception as e:
        print(e)
        return None
    
async def write_content(content, file_path):
    try:
        async with aiofiles.open(file_path, "w") as web_page_file:
            await web_page_file.write(content)
    except Exception as e:
        print("Problem here")
        print(e)
    
async def main():   
     
    if len(argv) < 2:
        print("Veuillez entrer un url en argument")
        exit(0)

    url = argv[1]
    file_path = "/tmp/web_page"
    
    content_task = get_content(url)

    write_task = write_content(content_task, file_path)
    
    tasks = [ content_task, write_task ]
    await asyncio.gather(*tasks)
    
    
if __name__ == "__main__":
    asyncio.run(main())
