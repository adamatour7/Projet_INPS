from django.urls import path
from .views import CotisationListAPIView, EmployeurCotisationsAPIView
# from .views import DemandeCreateAPIView, DeclarationCreateAPIView, TypeDemandeListAPIView
# from .views import DroitListAPIView, SimulationPensionCreateAPIView
# from .views import SuiviDemandeAPIView, SuiviDeclarationAPIView
# from .views import ListeRelevesAPIView, SoumissionDeclarationAPIView, telecharger_releve


urlpatterns = [
    path('employes/<int:employe_id>/cotisations/', CotisationListAPIView.as_view(), name='employe-cotisations'),
    path('employeurs/<int:employeur_id>/cotisations/', EmployeurCotisationsAPIView.as_view(), name='employeur-cotisations'),
    
    # path('types-demandes/', TypeDemandeListAPIView.as_view(), name='types-demandes'),
    # path('demandes/', DemandeCreateAPIView.as_view(), name='soumettre-demande'),
    # path('declarations/', DeclarationCreateAPIView.as_view(), name='soumettre-declaration'),
    
    # path('employes/<int:employe_id>/droits/', DroitListAPIView.as_view(), name='employe-droits'),
    # path('simulations/', SimulationPensionCreateAPIView.as_view(), name='simulation-pension'),
    
    # path('employes/<int:employe_id>/demandes/<int:demande_id>/', SuiviDemandeAPIView.as_view(), name='suivi-demande'),
    # path('employes/<int:employe_id>/declarations/<int:declaration_id>/', SuiviDeclarationAPIView.as_view(), name='suivi-declaration'),
    
    
    # path('employeur/releves/', ListeRelevesAPIView.as_view(), name='liste-releves'),
    # path('employeur/declaration/', SoumissionDeclarationAPIView.as_view(), name='soumission-declaration'),
    # path('employeur/releve/<int:releve_id>/telecharger/', telecharger_releve, name='telecharger-releve'),
 
 

    
    
]
