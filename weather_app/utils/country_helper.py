import requests


class GetCountry():

    def get_ip(self):
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]


    def get_location(self):
        ip_address = self.get_ip()
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()

        return  response.get("country_name")


