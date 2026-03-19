import requests
import time
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("METEO_API_KEY")

STATIONS = [
    "33042005",
    "33281001",
    "33540001",
    "40046001",
    "40192001",
    "40246003"
]

date_fin = datetime.utcnow() - timedelta(days=1)
date_deb = date_fin - timedelta(days=7)

date_fin_str = date_fin.strftime("%Y-%m-%d")
date_deb_str = date_deb.strftime("%Y-%m-%d")

all_data = ""

headers = {"apikey": API_KEY}

for station in STATIONS:
    print(f"Station {station}")

    try:
        # 1. Commande
        url_cmd = f"https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/quotidienne?id-station={station}&date-deb-periode={date_deb_str}T00:00:00Z&date-fin-periode={date_fin_str}T23:59:59Z"
        
        r = requests.get(url_cmd, headers=headers)
        r.raise_for_status()

        id_cmd = r.json()["elaboreProduitAvecDemandeResponse"]["return"]

        time.sleep(10)

        # 2. Téléchargement
        url_file = f"https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier?id-cmde={id_cmd}"
        r2 = requests.get(url_file, headers=headers)
        r2.raise_for_status()

        content = r2.text

        if all_data == "":
            all_data = content
        else:
            all_data += "\n".join(content.split("\n")[1:])

    except Exception as e:
        print(f"Erreur station {station}: {e}")

# 3. Sauvegarde
with open("meteo.csv", "w", encoding="utf-8") as f:
    f.write(all_data)

print("Fichier généré")
