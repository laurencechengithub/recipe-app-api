"""
View for recipe api
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
# for the use of the permission we check from user before they use
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

# ModelViewSet is use the direct interact with a model
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe api"""
    serializers_class = serializers.RecipeSerializer
    # the objects that are avaible for this view set
    query_set = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # override the orignal function to filter the queryset thats related to the user
    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        #user that is assigned with the request
        return self.query_set.filter(user=self.request.user).order_by('-id')
