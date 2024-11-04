from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SuiviDossier, Notification

# Envoyer une notification à l'utilisateur lors d'un changement de statut dans le dossier
@receiver(post_save, sender=SuiviDossier)
def notifier_changement_statut(sender, instance, **kwargs):
    if instance.demande_prestation:
        assure = instance.demande_prestation.assure
        dossier_type = "Demande de prestation"
    elif instance.declaration:
        assure = instance.declaration.assure
        dossier_type = "Déclaration"

    message = f"Votre {dossier_type} a été mis à jour. Nouveau statut : {instance.statut}"

    # Créer une notification
    Notification.objects.create(
        assure=assure,
        message=message
    )
