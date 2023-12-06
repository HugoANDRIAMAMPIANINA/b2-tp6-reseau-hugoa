from sys import argv
from time import perf_counter
import asyncio
import aiohttp
import aiofiles

async def get_content(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                return content
            else:
                print(f"Une erreur est survenue : {response.status}")
                return None

async def write_content(content, file_path):
    try:
        async with aiofiles.open(file_path, "wb") as web_page_file:
            await web_page_file.write(content)
    except Exception as e:
        print(e)
        exit(1)
        
async def get_urls_from_file(url_file_path) -> list[str] :
    try:
        async with aiofiles.open(url_file_path, "r") as url_file:
            urls = []
            async for line in url_file:
                urls.append(line.strip())
            return urls
        
    except Exception as e:
        print(e)
        return None

async def main():
    if len(argv) != 2:
        print("Veuillez entrer le chemin d'un fichier contenant un ou plusieurs urls en argument")
        exit(0)
        
    url_file_path = argv[1]
    
    urls: list[str] = await get_urls_from_file(url_file_path)
    
    for url in urls:
        content = await get_content(url)
        if content is not None:
            if "http://" in url:
                url = url.replace('http://', '')
            elif "https://" in url:
                url = url.replace('https://', '')
            file_path = f"/tmp/web_{url}"
            await write_content(content, file_path)

if __name__ == "__main__":
    time_start = perf_counter()
    asyncio.run(main())
    time_stop = perf_counter()
    print(f"Temps d'execution du script en secondes : {time_stop-time_start}")