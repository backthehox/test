import csv
import requests
import json
import pandas
from io import StringIO

# Initialisation des variables
data = []
nom_csv = "0man_alerte_sekoia.csv"
asset_csv=  "0man_assets_sekoia.csv"
token = "token"
base = "https://api.sekoia.io/v1/sic/alerts?sort=created_at&direction=desc&offset="
baseA = "https://api.sekoia.io/v1/asset-management/assets/"
headers = {
    'Authorization': 'Bearer ' + token
}
nbl = 103  # nombre d'alerte à extraire

#initialisation
alertes= []
count = 0
count2 = 0
dictass = {}
countass = 0

# Boucle pour sortir 100 alertes à chaque fois
for i in range(0, nbl, 100):
    limit = min(100, nbl - i)
    offset = i
    str_url = base + str(offset) + "&limit=" + str(limit)
    print(str_url)
    response = requests.get(str_url, headers=headers)
    print(response)
    data = response.json()
    alertes=  alertes + data['items']

#transformation CSV
csvfile= open(nom_csv, 'w', newline='')
csv_writer = csv.writer(csvfile, delimiter='|')
#csv_writer.writerow(alertes[0].keys())
#csv_writer.writerow('\n')
for alerte in alertes:
    # retrait des valeurs inutiles
    alerte.pop('details', None)
    alerte.pop('ttps', None)
    alerte.pop('entity', None)
    alerte.pop('kill_chain_short_id', None)
    alerte.pop('number_of_total_comments', None)
    test=str(alerte['urgency'])
    #Impression dans le CSV
    if count ==0:
        #impression du titre la première fois
        csv_writer.writerow(alerte.keys())
    csv_writer.writerow(str(x) for x in alerte.values())
    #csv_writer.writerow('\n')
    count+=1
    #ajout des actifs dans un dictionnaire
    for ass in alerte['assets']:
        if ass not in dictass.values():
            countass+=1
            dictass[countass]=ass
csvfile.close()

# imprime CSV assets
csvfile = open(asset_csv, 'w', newline='')
csv_writer = csv.writer(csvfile, delimiter='|')
#extraction des actifs
for i in range(1,3):
    str_url = baseA + dictass[i]
    response = requests.get(str_url, headers=headers)
    assets= response.json()
    # Impression dans le CSV
    if count2 == 0:
    # impression du titre la première fois
        csv_writer.writerow(assets.keys())
    csv_writer.writerow(str(x) for x in assets.values())
    # csv_writer.writerow('\n')
    count2 += 1
csvfile.close()
