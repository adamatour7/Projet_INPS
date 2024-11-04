from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom User Manager
class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom_utilisateur, mot_de_passe=None, role='assure'):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse e-mail")
        
        user = self.model(
            email=self.normalize_email(email),
            nom_utilisateur=nom_utilisateur,
            role=role  # Ajout du rôle ici
        )
        
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom_utilisateur, mot_de_passe):
        user = self.create_user(
            email=self.normalize_email(email),
            nom_utilisateur=nom_utilisateur,
            mot_de_passe=mot_de_passe,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Modèle Utilisateur personnalisé
class Utilisateur(AbstractBaseUser):
    ROLES = (
        ('assure', 'Assuré'),
        ('employeur', 'Employeur'),
        ('admin', 'Administrateur'),
    )

    email = models.EmailField(unique=True)
    nom_utilisateur = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLES)
    status = models.BooleanField(default=True)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_utilisateur', 'role']

    def __str__(self):
        return self.nom_utilisateur

# Modèle de log des actions utilisateur
class Log(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    action = models.TextField()
    date_action = models.DateTimeField(auto_now_add=True)
    ip_adresse = models.GenericIPAddressField()

# Modèle Assuré
class Assure(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='assure')
    numero_assure = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    etat_civil = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)
    date_affiliation = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nom} {self.prenom}'

# Modèle Employeur
class Employeur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    nom_entreprise = models.CharField(max_length=255)
    numero_identification = models.CharField(max_length=20, unique=True)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    secteur_activite = models.CharField(max_length=100)
    date_inscription = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nom_entreprise

# Modèle Cotisation
class Cotisation(models.Model):
    assure = models.ForeignKey(Assure, on_delete=models.CASCADE)
    employeur = models.ForeignKey(Employeur, on_delete=models.CASCADE)
    mois_annee = models.CharField(max_length=7)  # Format MM-YYYY
    salaire_brut = models.DecimalField(max_digits=10, decimal_places=2)
    montant_cotisation_salariale = models.DecimalField(max_digits=10, decimal_places=2)
    montant_cotisation_patronale = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.mois_annee} - {self.assure.nom}'


### deuxieme partie ##


from django.db import models
from django.conf import settings
from .models import Assure

# Modèle pour les types de prestations
class TypePrestation(models.Model):
    nom = models.CharField(max_length=255)  # Nom de la prestation, ex: 'Pension de retraite'
    description = models.TextField()

    def __str__(self):
        return self.nom

class DemandePrestation(models.Model):
    assure = models.ForeignKey('Assure', on_delete=models.CASCADE)
    type_prestation = models.ForeignKey(TypePrestation, on_delete=models.CASCADE)  # ForeignKey vers TypePrestation
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default='En attente')
    commentaire = models.TextField(null=True, blank=True)  # Commentaires sur la demande (facultatif)
    def __str__(self):
        return f'{self.assure} - {self.type_prestation}'
  # Ex: En attente, Approuvée, Rejetée
   

    

# Modèle pour les déclarations de l'assuré (revenus, changement de situation, etc.)
class Declaration(models.Model):
    TYPE_DECLARATION_CHOICES = [
        ('Revenus', 'Déclaration de revenus'),
        ('Mariage', 'Déclaration de mariage'),
        ('Naissance', 'Déclaration de naissance'),
        ('Résidence', 'Changement de résidence'),
    ]

    assure = models.ForeignKey(Assure, on_delete=models.CASCADE)
    type_declaration = models.CharField(max_length=50, choices=TYPE_DECLARATION_CHOICES)
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default='En attente')
    commentaire = models.TextField(null=True, blank=True)  # Commentaires ou remarques

    def __str__(self):
        return f"{self.assure.nom} - {self.type_declaration}"


# Modèle pour les documents soumis avec une demande ou déclaration
class Document(models.Model):
    FILE_TYPE_CHOICES = [
        ('Prestation', 'Document pour prestation'),
        ('Declaration', 'Document pour déclaration'),
    ]

    fichier = models.FileField(upload_to='documents/')
    type_document = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    demande_prestation = models.ForeignKey(DemandePrestation, on_delete=models.CASCADE, null=True, blank=True)
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, null=True, blank=True)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} - {self.type_document}"

############################################# Troisième Partie ##########################################################

from django.db import models
from .models import Assure

# Modèle pour les droits de l'assuré
class DroitsAssure(models.Model):
    assure = models.OneToOneField(Assure, on_delete=models.CASCADE)  # Un seul droit par assuré
    montant_pension_estimee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Montant estimé de la pension
    age_retraite_estime = models.IntegerField(default=60)  # Âge de départ à la retraite estimé
    allocations_familiales = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Montant des allocations familiales
    autres_droits = models.TextField(null=True, blank=True)  # Description d'autres droits éventuels

    def __str__(self):
        return f"Droits de {self.assure.nom} {self.assure.prenom}"

# Modèle pour stocker les simulations de pension
class SimulationPension(models.Model):
    assure = models.ForeignKey(Assure, on_delete=models.CASCADE)
    age_depart_retraite = models.IntegerField()  # Âge simulé pour la retraite
    salaire_moyen = models.DecimalField(max_digits=10, decimal_places=2)  # Salaire moyen des dernières années
    nombre_annees_contribution = models.IntegerField()  # Nombre d'années de cotisation
    montant_pension_simulee = models.DecimalField(max_digits=10, decimal_places=2)  # Résultat de la simulation

    date_simulation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulation pour {self.assure.nom} - {self.age_depart_retraite} ans"


############################################ Quatrième Partie #######################################################

from django.db import models
from .models import DemandePrestation, Declaration, Assure

# Modèle pour suivre l'évolution d'un dossier
class SuiviDossier(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('approuve', 'Approuvé'),
        ('rejeté', 'Rejeté'),
        ('documents_manquants', 'Documents manquants'),
    ]

    dossier_type = models.CharField(max_length=20, choices=[('prestation', 'Prestation'), ('declaration', 'Déclaration')])
    demande_prestation = models.ForeignKey(DemandePrestation, on_delete=models.CASCADE, null=True, blank=True)
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    commentaire = models.TextField(null=True, blank=True)  # Commentaires sur l'évolution du dossier

    def __str__(self):
        if self.demande_prestation:
            return f"Suivi pour la demande de prestation {self.demande_prestation}"
        if self.declaration:
            return f"Suivi pour la déclaration {self.declaration}"
        return "Suivi inconnu"

# Modèle pour les notifications envoyées aux utilisateurs
class Notification(models.Model):
    assure = models.ForeignKey(Assure, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date_envoyee = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)  # Marquer si l'utilisateur a lu la notification

    def __str__(self):
        return f"Notification pour {self.assure.nom} {self.assure.prenom}"

######################################### Cinquième partie ###########################################################


from django.db import models
from django.utils import timezone
from .models import Assure
from datetime import date

# Modèle pour gérer les rappels automatiques
class Rappel(models.Model):
    TYPE_RAPPEL_CHOICES = [
        ('cotisation', 'Rappel de paiement de cotisation'),
        ('document', 'Rappel de soumission de document'),
    ]

    assure = models.ForeignKey(Assure, on_delete=models.CASCADE)
    type_rappel = models.CharField(max_length=50, choices=TYPE_RAPPEL_CHOICES)
    date_echeance = models.DateField(null=True, blank=True)  # Date limite pour le paiement ou la soumission
    message = models.CharField(max_length=255)
    est_envoye = models.BooleanField(default=False)  # Marquer si le rappel a été 
    
    def save(self, *args, **kwargs):
        if self.date_echeance is None:  # Si pas de date d'échéance fournie
            self.date_echeance = self.get_date_echeance()  # Définir la date d'échéance
        super().save(*args, **kwargs)  # Appeler la méthode save parente

    def get_date_echeance(self):
        today = date.today()
        # Si aujourd'hui est après le 30, on prend le 30 du mois suivant
        if today.day > 30:
            next_month = today.month + 1 if today.month < 12 else 1
            year = today.year if next_month > 1 else today.year + 1
            return date(year, next_month, 30)
        # Sinon, on prend le 30 du mois courant

    def __str__(self):
        return f"{self.type_rappel} pour {self.assure.nom} - échéance {self.date_echeance}"

# Modèle pour gérer les notifications législatives
class NotificationLegislative(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_annonce = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)  # Permet de désactiver une notification après un certain temps

    def __str__(self):
        return self.titre


############################################ Sixième Partie ########################################################


from django.db import models
from django.utils import timezone
from .models import Assure

class Transaction(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('réussie', 'Réussie'),
        ('échouée', 'Échouée'),
    ]

    assure = models.ForeignKey(Assure, on_delete=models.CASCADE)  # Assuré qui effectue le paiement
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Montant payé
    date_transaction = models.DateTimeField(default=timezone.now)  # Date de la transaction
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')  # Statut du paiement
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)  # ID unique de la transaction Stripe
    message_confirmation = models.TextField(null=True, blank=True)  # Message de confirmation reçu après le paiement

    def __str__(self):
        return f"Transaction {self.reference} - {self.montant} FCFA - {self.statut}"
