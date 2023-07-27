from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class entreprises(models.Model):
    nom = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    site_web = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    idnat = models.CharField(max_length=100)
    rccm = models.CharField(max_length=100)
    taux = models.IntegerField()

    def __str__(self):
        return self.nom

class CustomUser(AbstractUser):
    # Ajoutez tous les champs supplémentaires que vous souhaitez pour le modèle User
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
    # Ajoutez tous les champs supplémentaires que vous souhaitez pour le modèle User
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username



class compteur(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=245)
    numero = models.IntegerField()
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')

    class Meta:
        db_table = 'compteur'
        
class classes(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=245)
    libelle2 = models.CharField(max_length=245)
    numero = models.IntegerField()
    etat = models.CharField(max_length=245)

    class Meta:
        db_table = 'classes'

class categories(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=245)
    numero = models.IntegerField()
    psedo = models.IntegerField(default=0)
    classe= models.ForeignKey(classes, on_delete=models.CASCADE, db_column='classe_id')


    class Meta:
        db_table = 'categories'

class comptes(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=245)
    numero = models.CharField(max_length=50)
    statut = models.CharField(max_length=50, null=True)
    categorie = models.ForeignKey('categories', on_delete=models.CASCADE, db_column='categorie_id')
    psedo = models.IntegerField(default=0)

    class Meta:
        db_table = 'comptes'


class compteEntreprise(models.Model):
    id = models.AutoField(primary_key=True)
    compte = models.ForeignKey('comptes', on_delete=models.CASCADE, db_column='compte_id')
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')

    class Meta:
        db_table = 'compteEntreprise'
        
class souscomptes(models.Model):
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=245)
    numero = models.CharField(max_length=50)
    compte = models.ForeignKey('comptes', on_delete=models.CASCADE, db_column='compte_id', null=True, default=None)
    psedo = models.IntegerField(default=0)
    modif = models.IntegerField(default=0)
    suffixe = models.CharField(max_length=100, null=True, default=None)
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')

    class Meta:
        db_table = 'souscomptes'


class journaux(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    libelle = models.CharField(max_length=245)
    psedo = models.IntegerField(default=0)
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')

    class Meta:
        db_table = 'journaux'

class journalcompte(models.Model):
    id = models.AutoField(primary_key=True)
    compte_num = models.IntegerField(null=True, default=None)
    journal = models.ForeignKey('journaux', on_delete=models.CASCADE, db_column='journal_id')
    long_compte = models.IntegerField(null=True, default=None)

    class Meta:
        db_table = 'journalcompte'
        unique_together = (('compte_num', 'journal'),)


class exercices(models.Model):
    id = models.AutoField(primary_key=True)
    lib = models.CharField(max_length=50, null=True, default=None)
    debut = models.DateField()
    fin = models.DateField()
    annee = models.IntegerField(null=True, default=None)
    etat = models.IntegerField(default=0)
    psedo = models.IntegerField(default=0)
    preseance = models.IntegerField(default=3)
    resultat = models.IntegerField(default=0)
    existe = models.IntegerField(default=0)
    ecriture = models.IntegerField(default=0)
    cloture = models.IntegerField(default=0)
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')
    
    class Meta:
        db_table = 'exercices'


class ecritures(models.Model):
    id = models.AutoField(primary_key=True)
    dte = models.DateField()
    dteaff = models.DateField(null=True, default=None)
    dtetime = models.DateTimeField()
    libelle = models.CharField(max_length=245)
    reference = models.CharField(max_length=50, null=True, default=None)
    beneficiaire = models.CharField(max_length=100, null=True, default=None)
    journal = models.ForeignKey('journaux', on_delete=models.CASCADE, db_column='journal_id')
    psedo = models.IntegerField(default=0)
    exercice = models.ForeignKey('exercices', on_delete=models.CASCADE, db_column='exercice_id', null=True, default=None)
    devise = models.CharField(max_length=10, null=True, default=None)
    lettrer = models.IntegerField(default=0)
    dteupdt = models.DateTimeField(null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')
    class Meta:
        db_table = 'cptecritures'


class detailsecritures(models.Model):
    id = models.AutoField(primary_key=True)
    compte = models.ForeignKey('comptes', on_delete=models.CASCADE, db_column='compte_id', null=True, default=None)
    debit = models.DecimalField(max_digits=65, decimal_places=10, default=0)
    credit = models.DecimalField(max_digits=65, decimal_places=10, default=0)
    libelle = models.CharField(max_length=245, null=True, default=None)
    numdoc = models.CharField(max_length=245, null=True, default=None)
    devise = models.CharField(max_length=10, null=True, default=None)
    taux = models.IntegerField(null=True, default=None)
    ecriture = models.ForeignKey('ecritures', on_delete=models.CASCADE, db_column='ecriture_id', null=True, default=None)
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')
    categorie = models.ForeignKey('categories', on_delete=models.CASCADE, db_column='categorie_id', null=True, default=None)
    souscompte = models.ForeignKey('souscomptes', on_delete=models.CASCADE, db_column='souscompte_id', null=True, default=None)
    compte_ecriture = models.CharField(max_length=200, null=True, default=None)
    long_compte = models.IntegerField(default=0)

    class Meta:
        db_table = 'detailsecritures'



class rapportjournal(models.Model):
    id = models.AutoField(primary_key=True)
    dte = models.DateField(null=True, default=None)
    ref = models.CharField(max_length=50, null=True, default=None)
    compte = models.CharField(max_length=200, null=True, default=None)
    description = models.TextField(null=True, default=None)
    debit = models.DecimalField(max_digits=65, decimal_places=10, default=0)
    credit = models.DecimalField(max_digits=65, decimal_places=10, default=0)
    devise = models.CharField(max_length=20, null=True, default=None)
    journal = models.ForeignKey('journaux', on_delete=models.CASCADE, db_column='journal_id', null=True, default=None)
    exercice = models.ForeignKey('exercices', on_delete=models.CASCADE, db_column='exercice_id', null=True, default=None)
    psedo = models.IntegerField(default=0)
    benprov = models.CharField(max_length=254, null=True, default=None)
    ecriture = models.ForeignKey('ecritures', on_delete=models.CASCADE, db_column='ecriture_id', null=True, default=None)
    entreprise = models.ForeignKey('entreprises', on_delete=models.CASCADE, db_column='entreprise_id')

    class Meta:
        db_table = 'rapportjournal'


class modelesRapportsCompta(models.Model):
    id = models.AutoField(primary_key=True)
    compte_id = models.CharField(max_length=200, default='0')
    saufbrut = models.CharField(max_length=200, default='0')
    partielbrut = models.CharField(max_length=200, null=True, default=None)
    rubrique = models.CharField(max_length=200, null=True, default=None)
    solde = models.IntegerField(default=0, help_text="0 peu importe 1 debiteur 2 crediteur")
    signevar = models.CharField(max_length=10, null=True, default=None)
    code = models.CharField(max_length=10)
    amortprov = models.CharField(max_length=200, default='0')
    saufamort = models.CharField(max_length=200, null=True, default=None)
    partielamort = models.CharField(max_length=200, null=True, default=None)
    format = models.IntegerField(default=3)
    ref = models.CharField(max_length=10, null=True, default=None)
    note = models.CharField(max_length=10, null=True, default=None)
    signe = models.IntegerField(null=True, default=None, help_text="-1=-;1=+;0=-/+")
    typeligne = models.IntegerField(default=0, help_text="-1=souscompte;0=compte;1=categorie;2=total")
    ba = models.IntegerField(default=0)
    bp = models.IntegerField(default=0)
    r = models.IntegerField(default=0, help_text="0=pas un compte resultat, 1=charge ,2 =produit")

    class Meta:
        db_table = 'modelesRapportsCompta'


