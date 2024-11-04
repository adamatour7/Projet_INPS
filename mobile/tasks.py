from celery import shared_task
from django.utils import timezone
from .models import Rappel, Assure
from django.core.mail import send_mail

@shared_task
def envoyer_rappels_cotisations():
    today = timezone.now().date()
    jour = today.day

    # Vérifier si nous sommes le 10, 11, ou 12 du mois
    if jour in [10, 11, 12]:
        # Récupérer tous les assurés
        assures = Assure.objects.all()

        # Parcourir les assurés et envoyer des rappels pour les cotisations du 15
        for assure in assures:
            # Vérifier s'il existe déjà un rappel non envoyé pour cet assuré pour le 15 du mois en cours
            if not Rappel.objects.filter(assure=assure, type_rappel='cotisation', date_echeance__month=today.month, date_echeance__year=today.year, est_envoye=False).exists():
                # Créer un rappel pour l'assuré
                rappel_message = f"Rappel: Vous devez payer vos cotisations avant le 15 {today.strftime('%B')}. Veuillez procéder au paiement pour éviter les pénalités."
                Rappel.objects.create(
                    assure=assure,
                    type_rappel='cotisation',
                    date_echeance=today.replace(day=15),
                    message=rappel_message
                )
                # Envoyer la notification
                envoyer_notification(assure.email, rappel_message)

def envoyer_notification(email, message):
    # Exemple d'envoi d'un email pour un rappel de cotisation
    send_mail(
        'Rappel de paiement de cotisation',
        message,
        'noreply@inps.com',  # Adresse email de l'expéditeur
        [email],  # Destinataire
        fail_silently=False,
    )
