# [Buienradar API](https://www.buienradar.nl/)

[![PyPI](https://img.shields.io/pypi/v/buienradar-api.svg)](https://pypi.org/project/buienradar-api/)

Unofficial wrapper for the buienradar [API](https://www.buienradar.nl/overbuienradar/gratis-weerdata) (dutch weather forecast). The Buienradar API currently features the following services:

- 2 hour GPS forecast based on longitude and latitude.
- Actual measurements per station
- 5 day forecast
- weather report

```python
from buienradar import BuienradarApi

api = BuienradarApi()
api.get_actual_weather()
```

```python
from buienradar import AsyncBuienradarApi

async def test():
    async with AsyncBuienradarApi() as api:
        forecast = await api.get_forecast()
        print(forecast)
```

## License

Licensed under the [MIT License](LICENSE).