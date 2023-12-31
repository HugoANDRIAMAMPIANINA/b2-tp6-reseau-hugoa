from sys import argv
from time import perf_counter
import requests

def get_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode()
        return content
    else:
        print(f"Le contenu de cette url n'a pas pu être récupéré : {response.status_code}")
        return None

def write_content(content, file_path):
    try:
        with open(file_path, "w") as web_page_file:
            web_page_file.write(content)
    except Exception as e:
        print(e)
        
def get_urls_from_file(url_file_path):
    try:
        with open(url_file_path, "r") as url_file:
            urls = []
            for line in url_file:
                urls.append(line.strip())
            return urls
        
    except Exception as e:
        print(e)
        return None

def main():
    if len(argv) != 2:
        print("Veuillez entrer le chemin d'un fichier contenant un ou plusieurs urls en argument")
        exit(0)
        
    url_file_path = argv[1]
    
    urls: list[str] = get_urls_from_file(url_file_path)
    
    for url in urls:
        content = get_content(url)
        if content is not None:
            if "http://" in url:
                url = url.replace('http://', '')
            elif "https://" in url:
                url = url.replace('https://', '')
            file_path = f"/tmp/web_{url}"
            write_content(content, file_path)

if __name__ == "__main__":
    time_start = perf_counter()
    main()
    time_stop = perf_counter()
    print(f"Temps d'execution du script en secondes : {time_stop-time_start}")