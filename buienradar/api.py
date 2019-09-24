import asyncio
from typing import Dict, List, Union

import aiohttp
import requests

from .models import (ActualWeather, Forecast, ForecastDay, ForecastMessage,
                     RainData, WeatherReport)


class BuienradarBase():
    base_url = 'https://data.buienradar.nl/2.0/feed/json'
    gps_url = 'https://gpsgadget.buienradar.nl/data/raintext'

    @staticmethod
    def _convert(payload: Union[List, Dict], model: type):
        if isinstance(payload, list):
            items = []
            for data in payload:
                item = model.from_dict(data)
                items.append(item)
            return items
        return model.from_dict(payload)

    @staticmethod
    def _convert_rain_data(payload: str) -> List[RainData]:
        lines = payload.splitlines()
        return [RainData(int(line.split('|')[0]), line.split('|')[1]) for line in lines]


class BuienradarApi(BuienradarBase):
    """
    Buienradar API.
    """

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json'
        }

    def _request(self, url: str, params: dict = None) -> object:
        with self.session.get(url, headers=self.headers, params=params) as request:
            request.raise_for_status()

            if request.headers['Content-Type'] == 'text/plain':
                return request.text

            return request.json()

    def get_shortterm_forecast(self) -> ForecastMessage:
        """ Get forecast message for the upcoming 5 days """
        response = self._request(self.base_url)
        return self._convert(response['forecast']['shortterm'], model = ForecastMessage)

    def get_longterm_forecast(self) -> ForecastMessage:
        """ Get forecast message for the upcoming 10 days """
        response = self._request(self.base_url)
        return self._convert(response['forecast']['longterm'], model = ForecastMessage)

    def get_forecast(self) -> List[ForecastDay]:
        """ Get forecast data for the upcoming 5 days """
        response = self._request(self.base_url)
        return self._convert(response['forecast']['fivedayforecast'], model = ForecastDay)

    def get_weather_report(self) -> WeatherReport:
        """ Get weather report """
        response = self._request(self.base_url)
        return self._convert(response['forecast']['weatherreport'], model = WeatherReport)
    
    def get_actual_weather(self) -> ActualWeather:
        """ Get actual weather measurements """
        response = self._request(self.base_url)
        return self._convert(response['actual'], model = ActualWeather)

    def get_rain(self, latitude: int, longitude: int) -> List[RainData]:
        """ Get the expected rainfall for the next 2 hours per 5 minutes """
        response = self._request(self.gps_url, { 'lat': latitude, 'lon': longitude })
        return self._convert_rain_data(response)


class AsyncBuienradarApi(BuienradarBase):
    """
    Async Buienradar API.
    """

    def __init__(self):
        self.headers = {
            'Accept': 'application/json'
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def _request(self, url: str, params: dict = None) -> object:
        async with self.session.get(url, headers=self.headers, params=params) as request:
            response = await request.json()
            request.raise_for_status()
            return response

    async def get_shortterm_forecast(self) -> ForecastMessage:
        """ Get forecast message for the upcoming 5 days """
        response = await self._request(self.base_url)
        return self._convert(response['forecast']['shortterm'], model = ForecastMessage)

    async def get_longterm_forecast(self) -> ForecastMessage:
        """ Get forecast message for the upcoming 10 days """
        response = await self._request(self.base_url)
        return self._convert(response['forecast']['longterm'], model = ForecastMessage)

    async def get_forecast(self) -> List[ForecastDay]:
        """ Get forecast data for the upcoming 5 days """
        response = await self._request(self.base_url)
        return self._convert(response['forecast']['fivedayforecast'], model = ForecastDay)

    async def get_weather_report(self) -> WeatherReport:
        """ Get weather report """
        response = await self._request(self.base_url)
        return self._convert(response['forecast']['weatherreport'], model = WeatherReport)

    async def get_actual_weather(self) -> ActualWeather:
        """ Get actual weather measurements """
        response = await self._request(self.base_url)
        return self._convert(response['actual'], model = ActualWeather)

    async def get_rain(self, latitude: int, longitude: int) -> List[RainData]:
        """ Get the expected rainfall for the next 2 hours per 5 minutes """
        response = await self._request(self.gps_url, { 'lat': latitude, 'lon': longitude })
        return self._convert_rain_data(response)