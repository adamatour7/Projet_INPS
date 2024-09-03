from rest_framework import serializers
from .models import Cotisation, Employe, Employeur

class EmployeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employeur
        fields = '__all__'

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'

class CotisationSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer()

    class Meta:
        model = Cotisation
        fields = '__all__'
        
####Gestion des demandes et déclarations


# from .models import Demande, Declaration, TypeDemande

# class TypeDemandeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TypeDemande
#         fields = '__all__'

# class DemandeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Demande
#         fields = '__all__'

# class DeclarationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Declaration
#         fields = '__all__'


# ##Consultation des droits et prestations

# from rest_framework import serializers
# from .models import Droit, SimulationPension

# class DroitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Droit
#         fields = '__all__'

# class SimulationPensionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SimulationPension
#         fields = '__all__'


# ###Suivi des dossiers


# from .models import Demande

# class DemandeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Demande
#         fields = '__all__'

# from .models import Declaration

# class DeclarationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Declaration
#         fields = '__all__'

# ####Relever cotisation

# from rest_framework import serializers
# from .models import ReleveCotisation

# class ReleveCotisationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ReleveCotisation
#         fields = '__all__'

# from .models import Declaration

# class DeclarationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Declaration
#         fields = '__all__'
