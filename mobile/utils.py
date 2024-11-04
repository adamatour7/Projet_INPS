from django.core.mail import send_mail

def envoyer_notification(email, message):
    send_mail(
        'Confirmation de paiement - INPS',
        message,
        'noreply@inps.com',
        [email],
        fail_silently=False,
    )
