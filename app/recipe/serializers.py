from asyncore import read
from rest_framework import serializers
from core.models import Recipe, Tag

# tagSerializer must be before recipe due to next serializer
class TagSerializer(serializers.ModelSerializer):
    "Serializers for tags"
    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']



#the ModelSerializer is going to represent a specific model in the system => recipe model
class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipe"""
    #many= this could be a list of tags
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id','title','time_minutes','price','link','tags']
        read_only_fields = ['id']


# using RecipeSerializer as the base class since it's just an extension of the that
# with some few extra fields only
class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']



