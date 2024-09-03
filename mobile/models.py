from django.db import models
from django.utils import timezone
from django.core.mail import send_mail


class Employeur(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.TextField()
    email = models.EmailField(unique=True)
    numero_identification = models.IntegerField( unique=True)
    date_enregistrement = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.nom

class Employe(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    numero_identification = models.IntegerField(unique=True)
    employeur = models.ForeignKey(Employeur, on_delete=models.CASCADE, related_name='employes')

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Cotisation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='cotisations')
    periode_debut = models.DateField()
    periode_fin = models.DateField()
    montant_verse = models.DecimalField(max_digits=10, decimal_places=2)
    date_versement = models.DateField()

    def __str__(self):
        return f"Cotisation de {self.employe} pour la période {self.periode_debut} - {self.periode_fin}"
    
#Gestion des demandes et déclarations


# class TypeDemande(models.Model):
#     nom = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.nom

# class Demande(models.Model):
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='demandes')
#     type_demande = models.ForeignKey(TypeDemande, on_delete=models.SET_NULL, null=True)
#     date_soumission = models.DateField(auto_now_add=True)
#     statut = models.CharField(max_length=50, default='En cours')
#     historique_statuts = models.JSONField(default=list)  # Nouvel ajout
#     documents = models.FileField(upload_to='documents_demandes/', blank=True, null=True)
#     commentaires = models.TextField(blank=True)

#     def __str__(self):
#         return f"Demande de {self.employe} pour {self.type_demande.nom}"

#     def mise_a_jour_statut(self, nouveau_statut):
#         self.historique_statuts.append({
#             "statut": nouveau_statut,
#             "date": timezone.now()
#         })
#         self.statut = nouveau_statut
#         self.save()
#         send_mail(
#         'Mise à jour de votre demande',
#         f'Votre demande a été mise à jour: {nouveau_statut}',
#         'no-reply@inps.example.com',
#         [self.employe.email],
#         fail_silently=False,
#         )



# class Declaration(models.Model):
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='declarations')
#     type_declaration = models.CharField(max_length=255)
#     date_soumission = models.DateField(auto_now_add=True)
#     statut = models.CharField(max_length=50, default='En cours')
#     historique_statuts = models.JSONField(default=list)  # Nouvel ajout
#     documents = models.FileField(upload_to='documents_declarations/', blank=True, null=True)
#     commentaires = models.TextField(blank=True)

#     def __str__(self):
#         return f"Declaration de {self.employe} pour {self.type_declaration}"

#     def mise_a_jour_statut(self, nouveau_statut):
#         self.historique_statuts.append({
#             "statut": nouveau_statut,
#             "date": timezone.now()
#         })
#         self.statut = nouveau_statut
#         self.save()
#         # Envoyer une notification par email
#         send_mail(
#         'Mise à jour de votre demande',
#         f'Votre demande a été mise à jour: {nouveau_statut}',
#         'no-reply@inps.example.com',
#         [self.employe.email],
#         fail_silently=False,
#         )

    
    
# ##Consultation des droits et prestations


# class Droit(models.Model):
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='droits')
#     type_droit = models.CharField(max_length=255)
#     description = models.TextField()
#     montant_estime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#     def __str__(self):
#         return f"Droit de {self.employe} pour {self.type_droit}"


# class SimulationPension(models.Model):
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='simulations')
#     age_retraite = models.IntegerField()
#     montant_estime = models.DecimalField(max_digits=10, decimal_places=2)
#     date_simulation = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Simulation de pension pour {self.employe} à {self.age_retraite} ans"


# ###

# class ReleveCotisation(models.Model):
#     employeur = models.ForeignKey(Employeur, on_delete=models.CASCADE, related_name='releves')
#     employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='releves')
#     date_periode = models.DateField()
#     montant = models.DecimalField(max_digits=10, decimal_places=2)
#     date_paiement = models.DateField()
#     statut = models.CharField(max_length=50, default='Payé')

#     def __str__(self):
#         return f"Relevé {self.date_periode} - {self.employe.nom}"
