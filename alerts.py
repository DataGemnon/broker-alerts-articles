# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 21:55:07 2025

@author: haasm
"""

# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen
import certifi
from datetime import datetime

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def filter_data_by_date(data, target_date):
    return [
        item for item in data
        if datetime.strptime(item['publishedDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date() == target_date
    ]

def find_latest_date_with_articles(data):
    dates = set()
    for item in data:
        dates.add(datetime.strptime(item['publishedDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date())
    sorted_dates = sorted(dates, reverse=True)
    for date in sorted_dates:
        filtered_data = filter_data_by_date(data, date)
        if filtered_data:
            return filtered_data
    return []

def display_latest_recommendations(data):
    print("Voici les dernières recommandations des brokers :\n")
    for item in data:
        published_datetime = datetime.strptime(item['publishedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        formatted_date = published_datetime.strftime('%Y-%m-%d %H:%M')
        print(f"Symbole : {item['symbol']}")
        print(f"Date : {formatted_date}")
        print(f"Titre : {item['newsTitle']}")
        print(f"Objectif de prix : {item['priceTarget']}")
        print(f"Société de l'analyste : {item['analystCompany']}")
        print(f"Lien : {item['newsURL']}\n")

# Récupération des données
url = "https://financialmodelingprep.com/api/v4/price-target-rss-feed?page=0&apikey=ENTER-YOUR-API-KEY-HERE"
data = get_jsonparsed_data(url)

# Filtrage et affichage
latest_data = find_latest_date_with_articles(data)
display_latest_recommendations(latest_data)
