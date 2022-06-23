"""
View for recipe api
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
# for the use of the permission we check from user before they use
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

#Tag
#mixin is just things that we can add into view
from rest_framework import mixins
from core.models import Tag

#Ingredients
from core.models import Ingredient

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

    def perform_create(self, serializer): #we override the create method of django
        "create a new recipe"
        #when we create a new recipe through the create feature of the view,
        #it's going to call this function
        serializer.save(user=self.request.user)


#tag => using viewset; viewset can provide simple CRUD
#GenericViewSet must be the last inheritance
#mixins.UpdateModelMixin => we can update the tags
#mixins.DestroyModelMixin => we can delete the tags
class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    'Manage tags in the database'
    serializer_class=serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        "Filter queryset to authenticated user"
        return self.queryset.filter(user=self.request.user).order_by('-name')

#mixins.UpdateModelMixin will au
class IngredientViewSet(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    'manage ingredients in the database'
    serializer_class=serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        "Filter queryset to authenticated user"
        return self.queryset.filter(user=self.request.user).order_by('-name')