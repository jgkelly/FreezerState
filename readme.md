# FreezerState
Raspberry Pi freezer temperature monitor and notifier. 

This project started after losing one too many freezer's full of food due to either a door not completely closed (it's an upright freezer, and the wife refuses to get a chest freezer), or a power outage. 

The idea is to have a Raspberry Pi Zero sitting on some sort of battery back-up, monitoring the internal temperature within the freezer, and providing the following "services":

* Some sort of notification (probably a text message) if the freezer temperature rises over a certain value
* A web interface that will let me view the current temperature within the freezer.
* _Nice to have_: Blinking LED visually signalling the temperature is too warm.
* _Nice to have_: REST interface allowing external applications to query current temperature values.
* _Nice to have_: Running in a Docker container.


## Requirements

This project was written under Python 3.5 or greater. It was developed under Python 3.8.2. 

## Usage

Currently, you will need to run this in the same folder as freezerstate.py:

```
python freezerstate.py
```

***NOTE:*** Make sure python is set to run Python 3.5 or greater. 