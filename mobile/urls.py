# urls.py de l'application (ex: mobile/urls.py)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CotisationViewSet, EmployeurViewSet, AssureViewSet,
    RegisterView, MyTokenObtainPairView, LogoutView,
    DemandePrestationViewSet, DeclarationViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView
from .views import DroitsAssureViewSet, SimulationPensionViewSet
from .views import SuiviDossierViewSet, NotificationViewSet
from .views import RappelViewSet, NotificationLegislativeViewSet
from .views import TransactionViewSet
from .stripe_webhook import stripe_webhook


# Création du routeur pour les vues standard
router = DefaultRouter()
router.register(r'cotisations', CotisationViewSet, basename='cotisation')
router.register(r'employeurs', EmployeurViewSet, basename='employeur')
router.register(r'assures', AssureViewSet, basename='assure')

router.register(r'droits-assure', DroitsAssureViewSet)
router.register(r'simulations-pension', SimulationPensionViewSet, basename='simulationpension')

router.register(r'suivi-dossiers', SuiviDossierViewSet, basename='suividossier')
router.register(r'notifications', NotificationViewSet, basename='notification')

router.register(r'rappels', RappelViewSet, basename='rappels')  # Rappels de cotisations
router.register(r'notifications-legislatives', NotificationLegislativeViewSet, basename='notifications-legislatives')  # Notifications législatives

router.register(r'transactions', TransactionViewSet, basename='transactions')
# Inclusion des URLs gérées par le routeur et des vues personnalisées
urlpatterns = [
    # URLs standard générées par le routeur
    path('', include(router.urls)),  # Préfixe commun pour toutes les routes générées par le routeur

    # Authentification et gestion des utilisateurs (sans le préfixe 'api/')
    path('register/', RegisterView.as_view(), name='register'),  # Enregistrement d'un nouvel utilisateur
    path('login/', MyTokenObtainPairView.as_view(), name='login'),  # Connexion et obtention d'un token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rafraîchir le token JWT
    path('logout/', LogoutView.as_view(), name='logout'),  # Déconnexion

    # Gestion des demandes de prestations et des déclarations (sans 'api/')
    path('demandes-prestation/', DemandePrestationViewSet.as_view({'post': 'create'}), name='demande_prestation'),
    path('declarations/', DeclarationViewSet.as_view({'post': 'create'}), name='declaration'),
    
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),  # Webhook Stripe pour les paiements
]
