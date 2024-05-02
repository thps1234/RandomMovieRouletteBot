# RandomMovieRouletteBot
 
Telegram bot [@RandomMovieRouletteBot](https://t.me/RandomMovieRouletteBot) randomly chooses a movie from a letterboxd list - pre-defined or chosen by a user.

Letterboxd doesn't have API, so we have to analyse content on a web page. 

> [!IMPORTANT]
> In order to make things simple, I don't store letterboxd data locally, so it takes a few seconds to fetch data.
> As a simple demo it runs locally on my PC, so 100% availability is not guaranteed.

## Used libraries

- **random** for picking a random movie from a list
- **requests** and **bs4** for webscrapping
- **re** for regular expression (checking validity of URL)
- **json** for transforming .json configs to dictionaries
- and last, but not least **telebot** as a telegram bot engine

## Files

- **randomMovieRouletteBot.py** - implementation
- **headers.json** - headers for requests
- **lists.json** - pre-defined lists
- **requirements.txt** and **Dockerfile** - Docker configs
- **token.txt** - telegram bot token. For obvious security reasons this file is not presented here. 