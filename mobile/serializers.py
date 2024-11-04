from rest_framework import serializers
from .models import Assure, Employeur, Cotisation

class AssureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assure
        fields = '__all__'

class EmployeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employeur
        fields = '__all__'

class CotisationSerializer(serializers.ModelSerializer):
    assure = AssureSerializer()
    employeur = EmployeurSerializer()

    class Meta:
        model = Cotisation
        fields = '__all__'
###########

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Utilisateur

# Sérialiseur d'enregistrement d'un nouvel utilisateur
class UtilisateurSerializer(serializers.ModelSerializer):
    mot_de_passe = serializers.CharField(write_only=True)
    
    class Meta:
        model = Utilisateur
        fields = ['email', 'nom_utilisateur', 'mot_de_passe', 'role', 'status']
        extra_kwargs = {
            'mot_de_passe': {'write_only': True}
        }

    def create(self, validated_data):
        user = Utilisateur(
            email=validated_data['email'],
            nom_utilisateur=validated_data['nom_utilisateur'],
            role=validated_data['role'],
            status=validated_data['status']
        )
        user.set_password(validated_data['mot_de_passe'])  # Hash du mot de passe
        user.save()
        return user

# Sérialiseur personnalisé pour la connexion JWT
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Ajouter des informations utilisateur au token (nom, rôle, etc.)
        data.update({'nom_utilisateur': self.user.nom_utilisateur})
        data.update({'role': self.user.role})

        return data

from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')
        return data



##### deuxieme partie ########


from rest_framework import serializers
from .models import DemandePrestation, Declaration, Document, TypePrestation

# Sérialiseur pour le type de prestation
class TypePrestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePrestation
        fields = '__all__'

# Sérialiseur pour les demandes de prestation
class DemandePrestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandePrestation
        fields = ['assure', 'type_prestation', 'commentaire']

# Sérialiseur pour les déclarations
class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = ['assure', 'type_declaration', 'commentaire']

# Sérialiseur pour les documents
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


############ troisième Partie #############


from rest_framework import serializers
from .models import DroitsAssure, SimulationPension

# Sérialiseur pour les droits de l'assuré
class DroitsAssureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroitsAssure
        fields = '__all__'

# Sérialiseur pour les simulations de pension
class SimulationPensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationPension
        fields = ['assure', 'age_depart_retraite', 'salaire_moyen', 'nombre_annees_contribution', 'montant_pension_simulee']
        read_only_fields = ['assure', 'montant_pension_simulee']
        
        
############################################ Quatrième Partie #######################################################

from rest_framework import serializers
from .models import SuiviDossier, Notification

# Sérialiseur pour le suivi des dossiers
class SuiviDossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviDossier
        fields = '__all__'

# Sérialiseur pour les notifications
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


######################################### Cinquième partie ###########################################################


from rest_framework import serializers
from .models import Rappel, NotificationLegislative

# Sérialiseur pour les rappels automatiques
class RappelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rappel
        fields = '__all__'

# Sérialiseur pour les notifications législatives
class NotificationLegislativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLegislative
        fields = '__all__'



############################################ Sixième Partie ########################################################

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        