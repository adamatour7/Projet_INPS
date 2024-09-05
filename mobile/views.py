from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Employe, Employeur, Cotisation
from .serializers import CotisationSerializer, EmployeSerializer, EmployeurSerializer

class CotisationListAPIView(generics.ListAPIView):
    serializer_class = CotisationSerializer

    def get_queryset(self):
        employe_id = self.kwargs['employe_id']
        return Cotisation.objects.filter(employe__id=employe_id).order_by('-periode_debut')

class EmployeurCotisationsAPIView(generics.ListAPIView):
    serializer_class = CotisationSerializer

    def get_queryset(self):
        employeur_id = self.kwargs['employeur_id']
        return Cotisation.objects.filter(employe__employeur__id=employeur_id).order_by('-periode_debut')

###########################################################
#Création de compte
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

## Connexion
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass

## Desactiver le compte
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class DeactivateAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"detail": "Compte désactivé"}, status=status.HTTP_204_NO_CONTENT)

####Gestion des demandes et déclarations

# from rest_framework import generics
# from .models import Demande, Declaration, TypeDemande
# from .serializers import DemandeSerializer, DeclarationSerializer, TypeDemandeSerializer

# class DemandeCreateAPIView(generics.CreateAPIView):
#     serializer_class = DemandeSerializer

# class DeclarationCreateAPIView(generics.CreateAPIView):
#     serializer_class = DeclarationSerializer

# class TypeDemandeListAPIView(generics.ListAPIView):
#     queryset = TypeDemande.objects.all()
#     serializer_class = TypeDemandeSerializer


# ##Consultation des droits et prestations

# from rest_framework import generics
# from .models import Droit, SimulationPension
# from .serializers import DroitSerializer, SimulationPensionSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView

# class DroitListAPIView(generics.ListAPIView):
#     serializer_class = DroitSerializer

#     def get_queryset(self):
#         employe_id = self.kwargs['employe_id']
#         return Droit.objects.filter(employe__id=employe_id)

# class SimulationPensionCreateAPIView(APIView):
#     serializer_class = SimulationPensionSerializer

#     def post(self, request, *args, **kwargs):
#         employe_id = request.data.get('employe')
#         age_retraite = int(request.data.get('age_retraite'))

#         # Logique de calcul simplifiée
#         employe = Employe.objects.get(id=employe_id)
#         droits = Droit.objects.filter(employe=employe, type_droit='Pension')
#         montant_estime = sum(droit.montant_estime for droit in droits) * (age_retraite / 65)  # Par exemple

#         simulation = SimulationPension.objects.create(
#             employe=employe,
#             age_retraite=age_retraite,
#             montant_estime=montant_estime
#         )

#         serializer = SimulationPensionSerializer(simulation)
#         return Response(serializer.data)


# ###Suivi des dossiers

# from rest_framework import generics
# from .models import Demande
# from .serializers import DemandeSerializer

# class SuiviDemandeAPIView(generics.RetrieveAPIView):
#     queryset = Demande.objects.all()
#     serializer_class = DemandeSerializer

#     def get_object(self):
#         employe_id = self.kwargs['employe_id']
#         demande_id = self.kwargs['demande_id']
#         return Demande.objects.get(id=demande_id, employe__id=employe_id)


# from .models import Declaration
# from .serializers import DeclarationSerializer

# class SuiviDeclarationAPIView(generics.RetrieveAPIView):
#     queryset = Declaration.objects.all()
#     serializer_class = DeclarationSerializer

#     def get_object(self):
#         employe_id = self.kwargs['employe_id']
#         declaration_id = self.kwargs['declaration_id']
#         return Declaration.objects.get(id=declaration_id, employe__id=employe_id)

# ####Relever cotisation

# from rest_framework import generics
# from .models import ReleveCotisation
# from .serializers import ReleveCotisationSerializer
# from rest_framework.permissions import IsAuthenticated

# class ListeRelevesAPIView(generics.ListAPIView):
#     serializer_class = ReleveCotisationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         employeur = self.request.user.employeur
#         return ReleveCotisation.objects.filter(employeur=employeur)


# from .models import Declaration
# from .serializers import DeclarationSerializer
# from rest_framework.permissions import IsAuthenticated

# class SoumissionDeclarationAPIView(generics.CreateAPIView):
#     serializer_class = DeclarationSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         employeur = self.request.user.employeur
#         serializer.save(employeur=employeur)

# from django.http import HttpResponse
# import csv

# def telecharger_releve(request, releve_id):
#     releve = ReleveCotisation.objects.get(id=releve_id, employeur=request.user.employeur)

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="releve_{releve_id}.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Employé', 'Date Période', 'Montant', 'Date Paiement', 'Statut'])
#     writer.writerow([releve.employe.nom, releve.date_periode, releve.montant, releve.date_paiement, releve.statut])

#     return response
