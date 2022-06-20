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
    #the variable names below are not to be modified
    serializer_class = serializers.RecipeDetailSerializer
    # the objects that are avaible for this view set
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # override the orignal function to filter the queryset thats related to the user
    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        #user that is assigned with the request
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        "Return the serializer class for the request"
        #the minor defference of RecipeSerializer vs RecipeDetailSerializer
        #is when the action are requesting the list of recipes that are without detail
        #so we use RecipeSerializer .
        #where as if with detail than we use RecipeDetailSerializer
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class