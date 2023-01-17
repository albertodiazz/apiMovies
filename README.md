# Descripcion

It is an Application Command Line Interface (CLI) for searching movies on the OK.ru servers, made with the help of Gnula [click gnula](gnula.nu). The CLI was designed to avoid the advertisements by web-scraping to directly obtain the working links.


## Installation
Docker version 20.10.18
```docker
# This was developed in WSL2, so I create a volume dbmovies which is located in the path /var/lib/docker/volumes/dbmovies 
docker volume create dbmovies
```
``` docker
docker compose up -d
```
Python version 3.8.10
``` python 
pip install -r requirements.txt
```

## Usage
+ -s = is the name of the movie, when we have a long name we must put it between quotes 'men in black'
+ -n = is the amount of searches to be carried out, we must remember that when we set large numbers we take longer to check the functioning of the links
``` python 
python -s <name movie> -n <number of results> 
```
![alt text](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d90fff4a-1890-49e7-a935-fdbc4c2648e1/photo_2023-01-16_14-24-46.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230116T230957Z&X-Amz-Expires=86400&X-Amz-Signature=4912fa1ddb194eb3519253851b20b3b5d906b4b17bf59bc0832ce6aca21ddf32&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22photo_2023-01-16_14-24-46.jpg%22&x-id=GetObject)

It is important to remember that the results appear based on the arrangement of the Russian links. If nothing appears, it means that it does not exist on the Gnula page.

## Motivation
This is a tool developed with the purpose of exploring a microservices architecture with Docker. Its functioning and design is an Overengineer to explore the communications between an API and parallel tasks. To do this, Django, Celery (task queue) and Redis were used to consume the results in the CLI. The CLI generates an HTTP request, the server verifies that the Gnula API KEY works or exists in the database, otherwise it generates a new KEY. Once this verification is done, it responds with the task ID and thus avoids timeout by NGINX, when the task is finished, Redis serves the response in our CLI.

![alt text](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/fc2219a4-3e82-464c-9716-7899d330a9d4/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230117%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230117T001019Z&X-Amz-Expires=86400&X-Amz-Signature=7ac842018dcd6e6987f518cb20ee51dfcda8a3d747843470d1ac5e46e64792a8&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)
