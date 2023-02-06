# WeatherApp

## Description

A simple website that makes use of the OpenWeatherMap current weather API in conjunction with the Arcgis location API in order to retrieve weather 
information of a certain location and save this information to the DB.

### Dependencies

Pip install requirements:
* django==2.2.28
* djangorestframework
* requests
* django-static-jquery==2.1.4

### Executing program

The main endpoint where all the magic happens is /home/.

The user enters an address/area and the program calls:
* Firstly, the Arcgis address API in order to get latitude and longitude. Depending on how vague the entry is, Arcgis may return multiple potential candidates.
The get_highest_score_index method in api_helper will retrieve the position of the candidate with the highest score to choose the closest coordinates.
* Once the coordinates are retrieved, they are sent to the OpenWeatherMap API where a current weather response is retrieved.
* The closest matching address, weather description, temperature and temperature that it feels like are displayed on the website.
* The user may choose to save this weather object or view historical data which pulls all the weather objects from the database.

## Authors

* Kirsten Forrester

## Contributors names and contact info

Tel: 071 872 0132

Email: forrestermkirsten@gmail.com