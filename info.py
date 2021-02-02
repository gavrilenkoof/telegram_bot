import requests


class _OpenWeatherMap():

    WEATHER_ID = '1b4fc164a1fa07df0699ca7a77bb2def'

    def get(self, city):
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={
                               'q': city,
                               'type': 'like',
                               'units': 'metric',
                               'lang': 'ru',
                               'APPID': _OpenWeatherMap.WEATHER_ID,
                           })
        data = res.json()
        return {
            'city': data['list'][0]['name'],
            'conditions': data['list'][0]['weather'][0]['description'],
            'temp': data['list'][0]['main']['temp'],
            'temp_max': data['list'][0]['main']['temp_max'],
            'temp_min': data['list'][0]['main']['temp_min'],
        }


class _NationalBankBelarus():
    

    def get(self, currency):
        res = requests.get(f'https://www.nbrb.by/api/exrates/rates/{currency}?parammode=2')
        data = res.json()
        return {
            'Currency' : data["Cur_Abbreviation"],
            'Quantity' : str(data["Cur_Scale"]) + ' ' + data["Cur_Abbreviation"] ,
            'Value to BYN' : str(data["Cur_OfficialRate"]) + ' ' + 'BYN',
        }




class CityInfo():

    def __init__(self, weather_forecast=None, bank=None):
        self._weather_forecast = weather_forecast or _OpenWeatherMap()
        self._bank = bank or _NationalBankBelarus()

    def weather_forecast(self, city):
        return self._weather_forecast.get(city)

    def get_exchange(self, currency):
        return self._bank.get(currency)
