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

#image
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


#filter
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


# ModelViewSet is use the direct interact with a model
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe api"""
    #the variable names below are not to be modified
    serializer_class = serializers.RecipeDetailSerializer
    # the objects that are avaible for this view set
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #recieving filter arguments as a list of ids, comma seperated
    def _params_to_ints(self, qs):
        'convert a list of string to intergers'
        return [int(str_id) for str_id in qs.split(',')]


    # override the orignal function to filter the queryset thats related to the user
    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        #user that is assigned with the request
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()


    def get_serializer_class(self):
        "Return the serializer class for the request"
        #the minor defference of RecipeSerializer vs RecipeDetailSerializer
        #is when the action are requesting the list of recipes that are without detail
        #so we use RecipeSerializer .
        #where as if with detail than we use RecipeDetailSerializer
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer): #we override the create method of django
        "create a new recipe"
        #when we create a new recipe through the create feature of the view,
        #it's going to call this function
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#tag => using viewset; viewset can provide simple CRUD
#GenericViewSet must be the last inheritance
#mixins.UpdateModelMixin => we can update the tags
#mixins.DestroyModelMixin => we can delete the tags
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        "Filter queryset to authenticated user"
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    'Manage tags in the database'
    serializer_class=serializers.TagSerializer
    queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
    'manage ingredients in the database'
    serializer_class=serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
