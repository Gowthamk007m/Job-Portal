from django.urls import include, path
from .views import *
from jobs.views import JobProfileSelectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'api/register', RegisterAPIView)

app_name = 'accounts' 


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('details/create/<id>', DetailsCreateView.as_view(), name='create_details'),    
    path('activities/create/', ActivitiesCreateView.as_view(), name='create_activities'),    
    path('qualifications/create/', QualificationsCreateView.as_view(), name='create_qualifications'),   
    path('role/', JobProfileSelectView.as_view(), name='role'),    

    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/login/',LoginAPIView.as_view(), name="api-login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    # path('', include(router.urls)),

]