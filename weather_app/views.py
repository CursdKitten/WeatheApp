from django.shortcuts import render
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import pytz
import requests
import json

from weather_app.utils import api_helper, country_helper
from weather_app.models import Weather

# initialise API helper
api_service = api_helper.APIHelper()
country_service = country_helper.GetCountry()

class HomeView(generic.View):
    
    def get(self, request):
        template = 'base.html'
        today = datetime.now().replace(tzinfo=pytz.utc)

        context = {"date_today": today}
        
        address = request.GET.get('address')
        description = request.GET.get('description')
        temperature = request.GET.get('temperature')
        feels_like = request.GET.get('feels_like')
        symbol = request.GET.get('symbol')
      
        if address:
            Weather.objects.create(address=address, temperature=float(temperature), description=description, 
                feels_like=feels_like, symbol=symbol)
        
        return render(request, template, context)

class MapAPIView(APIView):

    def get_coordinates(self, request, street_address):
        api_key = api_service.get_api_key_by_name('maps api')
        
        request_url = f"https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?address={street_address}&outFields=location&f=json&token={api_key}"

        # Send request
        response = requests.get(request_url)

           # Process response
        if response.status_code == 200:
            json_response = json.loads(response.text)
            return json_response
        else:
            print(f"Request error: {response.content.decode()}")
        
    def get(self, request, street_address):
        response = self.get_coordinates(request, street_address)
        return Response(response)


class WeatherAPIView(APIView):
    def get_weather_forecast(self, request, street_address):
        
        coordinate_service = MapAPIView()

        api_key = api_service.get_api_key_by_name('weather api')
        maps_response = coordinate_service.get_coordinates(request, street_address)
        latitude, longitude = api_service.extract_coordinates(maps_response)

        if latitude and longitude:
            closest_address = api_service.extract_closest_matching_address(maps_response)
            request_url= f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
            response = requests.get(request_url)

            if response.status_code == 200:
                return api_service.return_relevant_weather_data(json.loads(response.text), closest_address)
                
            else:
                return {"error":"invalid"}
        else:
            return {"error":"invalid"}
       

    def get(self, request, street_address):
        response = self.get_weather_forecast(request, street_address)
        return Response(response)

class HistoricalDataView(APIView):

    def get(self, request):
        
        historical_data = api_service.get_historical_data()

        return Response(historical_data)
