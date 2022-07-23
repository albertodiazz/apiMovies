# Descripcion

Esta sera mi primer aplicacion en go y lo que buscare sera el hacer una API apartir de hacer WebScraping con BurpSuite en una pagina de peliculas repleta de publicidad y que no tiene una API oficial [GNULA](https://gnula.nu/). 

## Objetivos

+ Poder buscar las peliculas desde un script.
+ Manejar las respuesta de peliculas encontradas o no.
+ Obetener los links de las peliculas con sus atributos de si tiene subtitulos o no, etc. 
+ Crear una base de datos que busque los links y si ya existe no es necesario interactuar con la api y si el link ya caduco o no existe lo debe de buscar en el internet.


### Plus

+ Buscar desde Telegram y que devuelva el catalogo de peliculas.
+ Poder seleccionar, darle play y stop desde Telegram.
+ Tener una pagina local que sirva como reproductor de las peliculas.
+ Extender este principio de buscar los links en todo el internet o al menos en multiples paginas de forma concurrente.

## Domain Driven Desing 

**Context**: HTTP API for search movies

**Language**: search, movies, genero, imbd, remoteControl

**Entities**: HTTP server 

**Service**: serchMovies, classification, addFavorites, listFavorites, controlPlayStop, visualization 

**Value Object**: [?] 

**Possible events**: MovieNotFound, MovieFound, ClassificationNotFound, alreadyExistFavorites, handlerHTTP, remoteControlHandler 

**Repository**: [?]

**Aggregates**: [?]

```**Nota** las partes que tienen ? es por que aun no entiendo los conceptos.```

