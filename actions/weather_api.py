# importing modules
import requests, json
from deep_translator import GoogleTranslator

# type your API KEY Here.
api_key = "cfa5b537727db559f6e39e8ad9fb481b"
base_url = "https://api.openweathermap.org/data/2.5/weather?"


def city_weather(city):
    # taking input "city name" from user
    city_name_en = GoogleTranslator(source='auto', target='en').translate(city)
    # print(city_name_en)
    # complete_url variable to store the complete_url address
    complete_url = base_url + "q=" + city_name_en + "&appid=" + api_key
    #
    # #get methods of requests module retruns respons object
    response = requests.get(complete_url)
    #
    # #json method of response object convert json format data into python format data
    x = response.json()

    format_add = None
    # Now x contains list of nested dictionaries
    # check the value of "cod" key is equal to "404", means city is found otherwise, city is not found
    if x["cod"] != "404":
        # store the value of "main" key in variable y
        format_add = x["main"]

        # store the value coressponding to the "temp" key of y
        current_temperature = format_add["temp"]

        # store the value coressponding to the "pressure" key of y
        current_pressure = format_add["pressure"]

        # store the value coressponding to the "humidity" key of y
        current_humidity = format_add["humidity"]

        # store the value of "weather" key in variable z
        z = x["weather"]

        # store the value corresponding to the "description" key
        # at the 0th index of z
        weather_description = z[0]["description"]
    else:
        format_add = "City Not Found"
    return format_add
