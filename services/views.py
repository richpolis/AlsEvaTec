# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import xmltodict
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
import requests

import xml.etree.ElementTree as ET

# Create your views here.
from services.models import RandomText
from services.utils import convert_xml_to_json


def random_text(request):
    response = requests.get('https://gturnquist-quoters.cfapps.io/api/random')
    data = response.json()
    repeat = False
    print(data)
    if 'value' in data and 'id' in data['value']:
        number = data['value']['id']
        text = data['value']['quote']

        if not RandomText.objects.filter(number=data['value']['id']).exists():
            RandomText.objects.create(number=number, text=text)
        else:
            print('Numero repetido: %s' % number)
            print('Texto: %s' % text)
            repeat = True
    else:
        number = 0
        text = 'Falla en el servicio'

    format = request.GET.get('format', 'html')
    if format == 'html':
        return render(request, 'services/random_text.html', {
            'number': number,
            'text': text,
            'repeat': repeat
        })
    elif format == 'json':
       return JsonResponse({'number': number, 'text': text, 'repeat': repeat})


def service_soap(request):
    response = requests.get('http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL')
    if response.status_code == 200:
        data = json.loads(json.dumps(xmltodict.parse(response.content)))
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Error en el servicio SOAP'})
