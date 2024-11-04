from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from django.conf import settings
from .models import Transaction

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'your-webhook-signing-secret'  # Remplacez avec votre clé de signature

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Payload invalide
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Signature invalide
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        stripe_charge_id = intent['id']

        # Mettre à jour le statut de la transaction
        try:
            transaction = Transaction.objects.get(stripe_charge_id=stripe_charge_id)
            transaction.statut = 'réussie'
            transaction.message_confirmation = f"Paiement de {transaction.montant} FCFA réussi."
            transaction.save()
        except Transaction.DoesNotExist:
            return JsonResponse({'status': 'transaction not found'}, status=404)

    return JsonResponse({'status': 'success'}, status=200)



      
