from django.shortcuts import render,HttpResponse
import requests
import json
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    total_info = None
    if 'info' in request.POST:
        total_info = dict()
        total_info = {
            'error': 0,
        }
        API_ENDPOINT = 'https://www.regcheck.org.uk/api/reg.asmx/CheckIndia'
        rtoNo = request.POST.get('info')
        # userName = 'random1123'
        userName = 'geekys'
        data = {'RegistrationNumber': rtoNo,
                'username': userName}
        v_info = requests.post(url=API_ENDPOINT, data=data).text

        soup = BeautifulSoup(v_info, "xml")
        try:
            vehicleJson = json.loads(soup.find('vehicleJson').text)
        except Exception as e:
            total_info = {
                'error': 1,
            }
        if total_info['error'] != 1:
            total_info['desc'] = vehicleJson.get('Description')
            total_info['year'] = vehicleJson.get('RegistrationYear')
            total_info['make'] = vehicleJson.get('CarMake').get('CurrentTextValue')
            total_info['model'] = vehicleJson.get('CarModel').get('CurrentTextValue')
            total_info['engine'] = vehicleJson.get('EngineNumber')
            total_info['ID_NO'] = vehicleJson.get('VechileIdentificationNumber')
            total_info['Owner'] = vehicleJson.get('Owner')
            total_info['Insurance'] = vehicleJson.get('Insurance')
            total_info['fuel'] = vehicleJson.get('FuelType').get('CurrentTextValue')
            total_info['date'] = vehicleJson.get('RegistrationDate')
            total_info['location'] = vehicleJson.get('Location')

    return render(request, 'core/home.html', {'details': total_info})