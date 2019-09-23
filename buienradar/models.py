from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import LetterCase, config, dataclass_json


@dataclass_json
@dataclass
class Forecast:
    weather_report: str
    short_term: str
    long_term: str
    five_day_forecast: str


@dataclass_json
@dataclass
class ForecastMessage:
    startdate: str
    enddate: str
    forecast: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ForecastDay:
    day: str
    mintemperature: str
    maxtemperature: str
    mintemperature_max: int
    mintemperature_min: int
    maxtemperature_max: int
    maxtemperature_min: int
    rain_chance: int
    sun_chance: int
    wind_direction: str
    wind: int
    mm_rain_min: int
    mm_rain_max: int
    weatherdescription: str
    iconurl: str


@dataclass_json
@dataclass
class WeatherReport:
    published: str
    title: str
    summary: str
    text: str
    author: str
    authorbio: str


@dataclass_json
@dataclass
class StationMeasurement:
    stationid: int
    stationname: str
    lat: int
    lon: int
    regio: str
    timestamp: str
    weatherdescription: str
    iconurl: str
    graphUrl: str
    temperature: Optional[float] = None
    groundtemperature: Optional[float] = None
    feeltemperature: Optional[float] = None
    humidity: Optional[int] = None
    winddirection: Optional[str] = None
    windgusts: Optional[float] = None
    windspeed: Optional[float] = None
    windspeedBft: Optional[int] = None
    precipitation: Optional[int] = None
    sunpower: Optional[int] = None
    rainFallLast24Hour: Optional[int] = None
    rainFallLastHour: Optional[int] = None
    winddirectiondegrees: Optional[int] = None
    airpressure: Optional[float] = None


@dataclass_json
@dataclass
class ActualWeather:
    actualradarurl: str
    sunset: str
    sunrise: str
    stationmeasurements: List[StationMeasurement]
