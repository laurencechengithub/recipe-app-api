"""
URL mappings for the recipe app.
"""

from django.urls import (
    path,
    include,
)
# default router provided by the django
from rest_framework.routers import DefaultRouter

from recipe import views

#Create a default router
router = DefaultRouter()
#register our viewset to the router with the name 'recipes'
router.register('recipes', views.RecipeViewSet)
#now this creates endpoint as "/recipes" from viewset to this end point
#and since we are using modelViewSet it's going to create CRUD create,read,update,delete

#register our viewset to the router with the name 'tads'
router.register('tags', views.TagViewSet)
#register our viewset to the router with the name 'ingredients'
router.register('ingredients', views.IngredientViewSet)


#define the name when we do reverse lookup  of url's
app_name = 'recipe'


# the urlpatterns are here to include the functions generated automatically by the router
urlpatterns = [
    path('',include(router.urls)),
]