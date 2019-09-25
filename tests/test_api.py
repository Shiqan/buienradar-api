import os
from unittest.mock import Mock, patch

import pytest
import requests

from buienradar import BuienradarApi
from buienradar.models import RainData

response = {
  "$id": "1",
  "buienradar": {
    "$id": "2",
    "copyright": "(C)opyright Buienradar / RTL. Alle rechten voorbehouden",
    "terms": "Deze feed mag vrij worden gebruikt onder voorwaarde van bronvermelding buienradar.nl inclusief een hyperlink naar https://www.buienradar.nl. Aan de feed kunnen door gebruikers of andere personen geen rechten worden ontleend."
  },
  "actual": {
    "$id": "3",
    "actualradarurl": "https://api.buienradar.nl/image/1.0/RadarMapNL?w=500&h=512",
    "sunrise": "2019-09-25T07:30:00",
    "sunset": "2019-09-25T19:32:00",
    "stationmeasurements": [
      {
        "$id": "4",
        "stationid": 6391,
        "stationname": "Meetstation Arcen",
        "lat": 51.5,
        "lon": 6.2,
        "regio": "Venlo",
        "timestamp": "2019-09-25T19:50:00",
        "weatherdescription": "Zwaar bewolkt",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png",
        "graphUrl": "https://www.buienradar.nl/nederland/weerbericht/weergrafieken/cc",
        "winddirection": "Z",
        "temperature": 16.3,
        "groundtemperature": 15.8,
        "feeltemperature": 16.3,
        "windgusts": 3.2,
        "windspeed": 1.6,
        "windspeedBft": 1,
        "humidity": 83,
        "precipitation": 0,
        "sunpower": 0,
        "rainFallLast24Hour": 1.6,
        "rainFallLastHour": 0,
        "winddirectiondegrees": 190
      },
      {
        "$id": "55",
        "stationid": 6252,
        "stationname": "Meetstation Zeeplatform K13",
        "lat": 53.22,
        "lon": 3.22,
        "regio": "Noordzee",
        "timestamp": "2019-09-25T19:50:00",
        "weatherdescription": "Zwaar bewolkt",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png",
        "graphUrl": "https://www.buienradar.nl/nederland/weerbericht/weergrafieken/cc",
        "winddirection": "ZZW",
        "airpressure": 1000.5,
        "windgusts": 9.5,
        "windspeed": 6.7,
        "windspeedBft": 4,
        "winddirectiondegrees": 193
      }
    ]
  },
  "forecast": {
    "$id": "56",
    "weatherreport": {
      "$id": "57",
      "published": "2019-09-25T17:45:00",
      "title": "Kletsnat",
      "summary": "De herfst is in volle gang. Het is een komen en gaan van regengebieden. Tussendoor is het tijdelijk wat droger maar veel ruimte voor de zon is er niet.",
      "text": "Voorlopig houden we het niet droog. De herfst is in volle gang! Met een zuidwestelijke aanvoer komt de een na de andere storing over.&nbsp;Goed voor de natuur maar wat minder leuk als je naar buiten wilt.Vanavond&nbsp;en vannacht wordt het tijdelijk wat droger al blijft in het&nbsp;westen en noorden de kans op een bui wat groter. De temperatuur daalt naar een graad of 14. De matig tot vrij krachtige wind waait uit het zuiden tot zuidwesten.Donderdag&nbsp;is het bewolkt en trekt er vanuit het zuidwesten een regengebied over. Het kan vooral in de noordwestelijke helft van het land flink plenzen. Ook is daar een klap onweer niet uit te sluiten. Het kwik blijft steken op zo&rsquo;n 18 graden. De zuidwestenwind is matig en aan de kust (vrij) krachtig.De dagen daarna&nbsp;blijft het wisselvallig. Van tijd tot tijd trekken er gebieden met regen of buien over Nederland. Op zondag valt er plaatselijk meer dan 15 mm. De middagtemperaturen komen over het algemeen uit op 17 of 18 graden.&nbsp;&nbsp;",
      "author": "Nicolien Kroon",
      "authorbio": "Sinds 2014 actief als meteoroloog en presentatie bij RTL Nieuws en Buienradar."
    },
    "shortterm": {
      "$id": "58",
      "startdate": "2019-09-26T00:00:00",
      "enddate": "2019-09-30T00:00:00",
      "forecast": "Van tijd tot tijd regen(buien) en maximumtemperaturen tussen 16 en 20°C. Vooral zondag vrij veel regen."
    },
    "longterm": {
      "$id": "59",
      "startdate": "2019-10-01T00:00:00",
      "enddate": "2019-10-05T00:00:00",
      "forecast": "De dagelijkse neerslagkans neemt af naar ca. 50%. Vrij grote kans (rond 50%) op maxima rond of iets onder normaal."
    },
    "fivedayforecast": [
      {
        "$id": "60",
        "day": "2019-09-26T00:00:00",
        "mintemperature": "14",
        "maxtemperature": "17",
        "mintemperatureMax": 14,
        "mintemperatureMin": 14,
        "maxtemperatureMax": 17,
        "maxtemperatureMin": 17,
        "rainChance": 90,
        "sunChance": 10,
        "windDirection": "zw",
        "wind": 4,
        "mmRainMin": 2,
        "mmRainMax": 6,
        "weatherdescription": "Zwaar bewolkt en regen",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png"
      },
      {
        "$id": "61",
        "day": "2019-09-27T00:00:00",
        "mintemperature": "13",
        "maxtemperature": "17/18",
        "mintemperatureMax": 13,
        "mintemperatureMin": 13,
        "maxtemperatureMax": 18,
        "maxtemperatureMin": 17,
        "rainChance": 70,
        "sunChance": 30,
        "windDirection": "zw",
        "wind": 4,
        "mmRainMin": 0,
        "mmRainMax": 2,
        "weatherdescription": "Afwisselend bewolkt met (mogelijk) wat lichte regen",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png"
      },
      {
        "$id": "62",
        "day": "2019-09-28T00:00:00",
        "mintemperature": "13",
        "maxtemperature": "16/17",
        "mintemperatureMax": 13,
        "mintemperatureMin": 13,
        "maxtemperatureMax": 17,
        "maxtemperatureMin": 16,
        "rainChance": 90,
        "sunChance": 30,
        "windDirection": "zw",
        "wind": 5,
        "mmRainMin": 3,
        "mmRainMax": 10,
        "weatherdescription": "Afwisselend bewolkt met (mogelijk) wat lichte regen",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png"
      },
      {
        "$id": "63",
        "day": "2019-09-29T00:00:00",
        "mintemperature": "12/13",
        "maxtemperature": "16/17",
        "mintemperatureMax": 13,
        "mintemperatureMin": 12,
        "maxtemperatureMax": 17,
        "maxtemperatureMin": 16,
        "rainChance": 90,
        "sunChance": 20,
        "windDirection": "zw",
        "wind": 4,
        "mmRainMin": 8,
        "mmRainMax": 17,
        "weatherdescription": "Zwaar bewolkt en regen",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png"
      },
      {
        "$id": "64",
        "day": "2019-09-30T00:00:00",
        "mintemperature": "12/14",
        "maxtemperature": "16/17",
        "mintemperatureMax": 14,
        "mintemperatureMin": 12,
        "maxtemperatureMax": 17,
        "maxtemperatureMin": 16,
        "rainChance": 90,
        "sunChance": 20,
        "windDirection": "w",
        "wind": 4,
        "mmRainMin": 1,
        "mmRainMax": 6,
        "weatherdescription": "Zwaar bewolkt en regen",
        "iconurl": "https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png"
      }
    ]
  }
}

@pytest.fixture()
def buienradar():
    return BuienradarApi()

@patch('buienradar.BuienradarApi._request')
def test_actual_weather(mock_response, buienradar):
    mock_response.return_value = response
    weather = buienradar.get_actual_weather()
    assert len(weather.stationmeasurements) == 2


@patch('buienradar.BuienradarApi._request')
def test_fivedayforecast(mock_response, buienradar):
    mock_response.return_value = response
    forecast = buienradar.get_forecast()
    assert len(forecast) == 5


def test_rain_intensity():
    assert RainData(77, 'notrelevent').rain_intensity == 0.1