# tournam8

 ![](pics/tournam8-logo.png) 

#### Read more about how this idea saves $21,504 per year in manual processing [here](https://www.slixites.com/blog/we-built-a-discord-bot-that-saves-usd21-504-per-year).





# Short Version

> A discord bot that is equipped with an OCR, custom functions and uses an API to send and retrieve data!


# Long Version

Tournam8 is a [Discord](https://en.wikipedia.org/wiki/Discord_(software)) bot that was built specific for Element, a tournament organization which hosts tournaments for video game called Spellbreak.

During a tournament, players are instructed to take a screenshot of their scores after a game and post them in a Discord text channel. Staff members then record all of the player statistics to a spreadsheet. 

To give you more perspective on whats that like. There are about 40 players in a game and there are 6 games played per tournament. That's 240 screenshots per tournament and at an average of 6 characters per screenshots, that around 1440 characters that need to be transferred to an excel sheet.



![](pics/logo-element.png)
***Element Logo***

Here is an example of the OCR. The system extracts the data from a screenshot and sends the information to a database through an my API.


![](pics/ocr-example-1.gif)


# API

The API used for the data transfer can be found [Here](https://github.com/adavila0703/elements-API)

### Request Example
```cpp
{
    "data":
    {
        "type": "record",
        "attributes": {
            "kills": 15,
            "damage": 1500,
            "place": 1,
            "assists": 3,
            "username": "marley-ee",
            "game": "Game 1",
            "discord_id": 256486795486897624,
            "scrimy_name": null,
            "tourny_name": "Element 1",
            "qualy_name": null

        }
    }
}
```


# Technologies

| Language | VPS            | API                                | Platform | OCR                         | Imaging |
|----------|----------------|------------------------------------|----------|-----------------------------|---------|
| Python   | Vultr (Ubuntu) | Flask / SQLAlchemy / Rest JSON API | Discord  | Tesseract OCR / Pytesseract | OpenCV  |

