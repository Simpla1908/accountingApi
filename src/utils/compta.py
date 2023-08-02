# compta
from app.models import categories, comptes,souscomptes

def get_account_number(compte_num, long):
    data = {'id': None, 'lib': None}

    if long == 2:
        try:
            category = categories.objects.get(numero=compte_num)
            data['id'] = category.id
            data['lib'] = category.libelle
        except categories.DoesNotExist:
            pass
    elif long == 3:
        try:
            compte = comptes.objects.get(numero=compte_num)
            data['id'] = compte.id
            data['lib'] = compte.libelle
        except comptes.DoesNotExist:
            pass
    elif long >= 4:
        try:
            souscompte = souscomptes.objects.get(numero=compte_num)
            data['id'] = souscompte.id
            data['lib'] = souscompte.libelle
        except souscomptes.DoesNotExist:
            pass

    return data
