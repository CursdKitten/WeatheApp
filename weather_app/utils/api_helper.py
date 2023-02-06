from weather_app.models import APIKey, Weather
from weather_app.utils import country_helper

country_service = country_helper.GetCountry()

class APIHelper():
    
    def get_api_key_by_name(self, name):
        return APIKey.objects.get(name=name).key

    def convert_units(self, kelvin, country):
        temp = round(kelvin-273.15)
        if country:
            if 'united states' in country:
                temp = round(9/5(kelvin - 273) + 32)
        
        return temp

    def get_symbol(self, country):
        symbol = '°C'
        if country:
            if 'united states' in country:
                symbol = '°F'

        return symbol
    
    def return_relevant_weather_data(self, response, address):

        country = country_service.get_location()

        return {
            'address': address,
            'description': response['weather'][0]['description'],
            'temperature': self.convert_units(float(response['main']['temp']), country),
            'feels_like':  self.convert_units(float(response['main']['feels_like']), country),
            'symbol': self.get_symbol(country),
            'icon': response['weather'][0]['icon']
        }
    
    def get_highest_score_index(self, response):
        
        scores = []
        for candidate in response['candidates']:
            scores.append(float(candidate['score']))
        
        closest_similarity = max(scores)
        return scores.index(closest_similarity)


    def extract_closest_matching_address(self, response):
        index = self.get_highest_score_index(response)

        return response['candidates'][index]['address']

    def extract_coordinates(self, response):
        lat = None
        long = None
        if response['candidates']:
            index = self.get_highest_score_index(response)
            lat = response['candidates'][index]['location']['x']
            long = response['candidates'][index]['location']['y']

        
        return lat, long
    
    def get_historical_data(self):
        response = []
        all_weather_objects = Weather.objects.order_by('date_created_at')

        for object in all_weather_objects:
            response_dict = {}
            response_dict['address'] = object.address
            response_dict['temperature'] = object.temperature
            response_dict['description'] = object.description
            response_dict['feels_like'] = object.feels_like
            response_dict['symbol'] = object.symbol

            response.append(response_dict)
        
        return response
            