from asyncore import read
from rest_framework import serializers
from core.models import Recipe

#the ModelSerializer is going to represent a specific model in the system => recipe model
class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipe"""

    class Meta:
        model = Recipe
        fields = ['id','title','time_minutes','price','link']
        read_only_field = ['id']