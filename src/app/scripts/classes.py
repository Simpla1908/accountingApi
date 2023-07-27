# importer.py
import json
import os

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votre_projet.settings")
import django

django.setup()

from app.models import classes

def importer_donnees_json():
    with open('json/classes.json') as fichier:
        donnees = json.load(fichier)
        for element in donnees[1]["data"]:
            obj = classes(
                id=int(element['id']),
                libelle=element['libelle'],
                libelle2=element['libelle2'],
                numero=int(element['numero']),
                etat=element['etat'],
            )
            obj.save()

if __name__ == '__main__':
    importer_donnees_json()
