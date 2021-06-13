import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import urllib.request
import json

class coord_scraper:

    def __init__(self, city, state):
        self.image = ""
        self.city = city
        self.state = state
        self.api_key = "03428aa539f939d0a417e761df5f639d"
        self.query = city.replace(" ", "_")
        # self.query = city.replace(" ", "_") + ",_" + state.replace(" ","_")
        self.url = "https://www.wikipedia.org/wiki/%s" % self.query
        self.coords = None

    def get_coords(self):

        # GET HTML response
        response = requests.get(self.url)

        # if response status code is 200
        if response:
            try:
                # Parse HTML response
                soup = BeautifulSoup(response.text, 'html.parser')
                # Locate and extract longitudinal coordinates
                latlon = soup.find("span", class_="geo-dec").text
                # Convert coordinates digits to floats, using list comprehension
                latlon_dd = [float(i) for i in re.findall("\\d+[.]\\d+", latlon)]
                if re.findall("\\w$", latlon)[0] == "S":
                    latlon_dd[0] = -1 * latlon_dd[0]  # negative sign if in the Southern hemisphere
                if re.findall("\\w$", latlon)[0] == "W":
                    latlon_dd[1] = -1 * latlon_dd[1]  # negative sign if in the Western hemisphere
                self.lat, self.lon = latlon_dd
            except AttributeError:
                print(
                    "WARNING: Webpage did not contain coordinate locations (e.g., search yielded a disambiguation page.)")
                self.lat, self.lon = np.nan, np.nan
        else:
            print("WARNING: Response status code was not 200 (STATUS: %d)" % response.status_code)
            self.lat, self.lon = np.nan, np.nan
        self.coords = {"longitude": self.lon, "latitude": self.lat}

    def get_image(self):
        content = requests.get(self.url).content
        soup = BeautifulSoup(content, 'lxml')  # choose lxml parser
        # find the tag : <img ... >
        image_tags = soup.findAll('img')
        i = 1
        for image_tag in image_tags:
            link = image_tag.get('src')
            filename = self.query + ".jpg"
            if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
                if i == 1:
                    i += 1
                    image_link = "https:" + link
                    #print(image_link)
                    self.image = image_link
                    #urllib.request.urlretrieve(image_link, filename)

    def get_weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = self.city
        complete_url = base_url + "appid=" + self.api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        print(x)
        print(response)
        if x["cod"] != "404":
            # store the value of "main"
            # key in variable y
            y = x["main"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]

            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidiy = y["humidity"]

            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]

            # print following values
            print(" Temperature (in kelvin unit) = " +
                  str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(current_pressure) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))
            return {
                "temperature": current_temperature-273.15,
                "current_pressure": current_pressure,
                "current_humidiy" : current_humidiy,
                "description": weather_description
            }

        else:
            return "City not found"



#paris = coord_scraper("Berlin", "Germany")
#paris.get_coords()
#print(paris.coords)

#skopje = coord_scraper("skopje", "macedonia")
#skopje.get_coords()
#print(skopje.coords)

#print(skopje.lat)
#print(skopje.lon)

#skopje.get_image()
#paris.get_image()

#ljubljana = coord_scraper("ljubljana", "slovenia")
#ljubljana.get_image()


skopje = coord_scraper("Ljubjana", "Slovenia")
skopje.get_coords()
print(skopje.coords)

#print(ljubljana.image)

