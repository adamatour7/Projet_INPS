from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Assure, Employeur, Cotisation
from .serializers import AssureSerializer, EmployeurSerializer, CotisationSerializer

# Vue pour gérer les assurés
class AssureViewSet(viewsets.ModelViewSet):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    permission_classes = [IsAuthenticated]

    # Filtrer les cotisations pour l'assuré connecté
    def list(self, request, *args, **kwargs):
        # Vérifier si l'utilisateur est un assuré
        if request.user.role == 'assure':
            # Filtrer uniquement les cotisations liées à cet assuré
            cotisations = Cotisation.objects.filter(assure__email=request.user.email)
        else:
            return Response({"error": "Vous n'êtes pas un assuré."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(cotisations, many=True)
        return Response(serializer.data)


# Vue pour gérer les employeurs
class EmployeurViewSet(viewsets.ModelViewSet):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    permission_classes = [IsAuthenticated]

    # Filtrer les cotisations pour les assurés d'un employeur
    def list(self, request, *args, **kwargs):
        # Si l'utilisateur est un employeur
        if request.user.role == 'employeur':
            # Filtrer les cotisations des assurés pour cet employeur
            employeur = Employeur.objects.get(email=request.user.email)
            cotisations = Cotisation.objects.filter(employeur=employeur)
        else:
            return Response({"error": "Vous n'êtes pas un employeur."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(cotisations, many=True)
        return Response(serializer.data)


# Vue pour gérer les cotisations
class CotisationViewSet(viewsets.ModelViewSet):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer
    permission_classes = [IsAuthenticated]

    # Consulter la cotisation pour un employé ou un mois spécifique
    def retrieve(self, request, *args, **kwargs):
        cotisation_id = kwargs.get('pk')  # Par exemple, via l'ID de la cotisation
        cotisation = Cotisation.objects.filter(id=cotisation_id).first()

        if not cotisation:
            return Response({"error": "Cotisation non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        # Vérification des permissions basées sur le rôle
        if request.user.role == 'assure':
            if cotisation.assure.email != request.user.email:
                return Response({"error": "Vous n'avez pas accès à cette cotisation."}, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'employeur':
            employeur = Employeur.objects.get(email=request.user.email)
            if cotisation.employeur != employeur:
                return Response({"error": "Cette cotisation ne concerne pas un de vos employés."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(cotisation)
        return Response(serializer.data)

###########


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import Utilisateur
from .serializers import UtilisateurSerializer, MyTokenObtainPairSerializer

# Vue d'enregistrement
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        role = data.get('role', None)

        # On vérifie que le rôle est valide (employé ou employeur)
        if role not in ['assure', 'employeur']:
            return Response({"error": "Rôle invalide. Choisissez 'assure' ou 'employeur'."}, status=status.HTTP_400_BAD_REQUEST)

        # Sérialiseur pour créer l'utilisateur
        serializer = UtilisateurSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur enregistré avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue personnalisée de connexion avec SimpleJWT
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        print("Données reçues pour la connexion : ", request.data)  # Débogage
        return super().post(request, *args, **kwargs)

# Vue de déconnexion (Invalidation du token en l'effaçant côté client)
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalide le token
            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Impossible de se déconnecter."}, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


########################################### deuxieme partie #################################################




from .models import DemandePrestation, Declaration, Document, TypePrestation
from .serializers import DemandePrestationSerializer, DeclarationSerializer, DocumentSerializer, TypePrestationSerializer

# Vue pour gérer les types de prestations
class TypePrestationViewSet(viewsets.ModelViewSet):
    queryset = TypePrestation.objects.all()
    serializer_class = TypePrestationSerializer
    permission_classes = [IsAuthenticated]

# Vue pour gérer les demandes de prestations
class DemandePrestationViewSet(viewsets.ModelViewSet):
    queryset = DemandePrestation.objects.all()
    serializer_class = DemandePrestationSerializer
    permission_classes = [IsAuthenticated]


# Vue pour gérer les déclarations
# Vue pour soumettre une déclaration
class DeclarationViewSet(viewsets.ModelViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    permission_classes = [IsAuthenticated]

# Vue pour gérer les documents associés aux demandes et déclarations
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]



######################################## Troisième Partie ######################################################


from .models import DroitsAssure, SimulationPension
from .serializers import DroitsAssureSerializer, SimulationPensionSerializer
from django.db.models import Sum
from datetime import datetime
from .models import SimulationPension, Cotisation

# Vue pour les droits de l'assuré
class DroitsAssureViewSet(viewsets.ModelViewSet):
    queryset = DroitsAssure.objects.all()
    serializer_class = DroitsAssureSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Récupérer les droits de l'assuré connecté
        droits = DroitsAssure.objects.filter(assure=request.user.assure)
        serializer = self.get_serializer(droits, many=True)
        return Response(serializer.data)

# Vue pour gérer la simulation de pension
class SimulationPensionViewSet(viewsets.ModelViewSet):
    queryset = SimulationPension.objects.all()
    serializer_class = SimulationPensionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Extraire les données nécessaires pour la simulation
        salaire_moyen = request.data.get('salaire_moyen')
        nombre_annees_contribution = int(request.data.get('nombre_annees_contribution'))

        # Calcul de la date correspondant à 8 ans avant aujourd'hui
        today = datetime.today()
        date_huit_ans_avant = today.replace(year=today.year - 8).strftime('%Y-%m')

        # Récupérer les cotisations des 8 dernières années
        cotisations = Cotisation.objects.filter(
            assure=request.user.assure,
            mois_annee__gte=date_huit_ans_avant  # Filtrer les cotisations sur 8 ans
        ).aggregate(total_salaire=Sum('salaire_brut'))

        if cotisations['total_salaire'] is None:
            return Response({"error": "Pas assez de données pour calculer la RMM."}, status=status.HTTP_400_BAD_REQUEST)

        total_salaire_8_dernieres_annees = cotisations['total_salaire']
        RMM = total_salaire_8_dernieres_annees * 8 / 96  # Calcul de la RMM sur les 8 dernières années

        # Calcul de la pension
        TAUX_REMPLACEMENT = 0.02  # 2 % par année de cotisation
        montant_pension_simulee = RMM * TAUX_REMPLACEMENT * nombre_annees_contribution

        # Sauvegarder la simulation dans la base de données
        simulation = SimulationPension.objects.create(
            assure=request.user.assure,
            age_depart_retraite=request.data.get('age_depart_retraite'),
            salaire_moyen=salaire_moyen,
            nombre_annees_contribution=nombre_annees_contribution,
            montant_pension_simulee=montant_pension_simulee
        )

        serializer = self.get_serializer(simulation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
############################################ Quatrième Partie #######################################################

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SuiviDossier, Notification
from .serializers import SuiviDossierSerializer, NotificationSerializer

# Vue pour le suivi des dossiers
class SuiviDossierViewSet(viewsets.ModelViewSet):
    queryset = SuiviDossier.objects.all()
    serializer_class = SuiviDossierSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Filtrer par l'assuré connecté et par type de dossier
        dossier_type = request.query_params.get('dossier_type')
        if dossier_type == 'prestation':
            suivi = SuiviDossier.objects.filter(dossier_type='prestation', demande_prestation__assure=request.user.assure)
        elif dossier_type == 'declaration':
            suivi = SuiviDossier.objects.filter(dossier_type='declaration', declaration__assure=request.user.assure)
        else:
            return Response({"error": "Type de dossier non spécifié."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(suivi, many=True)
        return Response(serializer.data)

# Vue pour les notifications
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Récupérer les notifications pour l'utilisateur connecté
        notifications = Notification.objects.filter(assure=request.user.assure)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Marquer une notification comme lue
        notification = self.get_object()
        notification.lu = True
        notification.save()
        return Response(self.get_serializer(notification).data)


######################################### Cinquième partie ###########################################################


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rappel, NotificationLegislative
from .serializers import RappelSerializer, NotificationLegislativeSerializer
from django.utils import timezone

# Vue pour gérer les rappels
class RappelViewSet(viewsets.ModelViewSet):
    queryset = Rappel.objects.all()
    serializer_class = RappelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Récupérer les rappels de l'utilisateur connecté
        rappels = Rappel.objects.filter(assure=request.user.assure, est_envoye=False)
        serializer = self.get_serializer(rappels, many=True)
        return Response(serializer.data)

# Vue pour gérer les notifications législatives
class NotificationLegislativeViewSet(viewsets.ModelViewSet):
    queryset = NotificationLegislative.objects.filter(est_active=True)  # Affiche uniquement les notifications actives
    serializer_class = NotificationLegislativeSerializer
    permission_classes = [IsAuthenticated]


############################################ Sixième Partie ########################################################


import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Transaction
from .serializers import TransactionSerializer

# Configurer Stripe avec la clé secrète
stripe.api_key = settings.STRIPE_SECRET_KEY

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        # Récupérer les informations nécessaires à la transaction
        assure_id = request.data.get('assure')
        montant = request.data.get('montant')
        
        # Convertir le montant en centimes car Stripe utilise les centimes
        montant_cents = int(float(montant) * 100)

        try:
            # Créer un PaymentIntent avec Stripe
            intent = stripe.PaymentIntent.create(
                amount=montant_cents,
                currency='xof',  # Changez la devise si nécessaire
                payment_method_types=['card'],
                description="Paiement de cotisation",
            )

            # Enregistrer la transaction dans la base de données
            transaction = Transaction.objects.create(
                assure_id=assure_id,
                montant=montant,
                statut='en_attente',
                stripe_charge_id=intent['id'],
            )

            # Retourner le client_secret à envoyer au frontend
            return Response({
                'client_secret': intent['client_secret'],
                'transaction': self.get_serializer(transaction).data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
