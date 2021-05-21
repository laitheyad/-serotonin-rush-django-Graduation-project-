from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'SerotoninRush'
router = routers.DefaultRouter()
router.register('register_user', RegisterUser, basename='register_user')
router.register('login', Login, basename='login')
router.register('update_info', UpdateInfo, basename='update_info')
router.register('all_meals', AllMeals, basename='all_meals')
router.register('add_reaction', AddReaction, basename='add_reaction')
router.register('news', NewsAPI, basename='news')
router.register('user_info', GetUserInfoViaToken, basename='user_info')
router.register('user_reactions_info', GetUserMealsViaToken, basename='user_reactions_info')

urlpatterns = [
    path('API/', include(router.urls)),
    path(r'change_meal_status/', ChangeMealStatus.as_view(), name='change_meal_status'),
    path(r'pending_meals/', PendingMeals.as_view(), name='pending_meals'),
    path(r'approved_meals/', ApprovedMeals.as_view(), name='approved_meals'),
    path(r'create_meal/', createMeal.as_view(), name='create_meal'),
    path(r'correlation/', correlation.as_view(), name='correlation')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
