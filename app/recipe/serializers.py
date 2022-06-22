
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

        #default nested serializer are read only, thus we need to create custom
    #adding a new method in class to override the original create method
    def create(self, validated_data):
        "create a recipe"
        #tags exists, remove it from validated_data and asign it to new varibale
        tags = validated_data.pop('tags',[])
        #and the rest of validated_data (that tags are exculded)
        #we are going to create recipe with those value
        recipe = Recipe.objects().create(**validated_data)
        #get the authenticated user
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, created = Tag.objects().get_or_create(
                user=auth_user,
                **tag, # name=tag['name'],
            )
            recipe.tags.add(tag_obj)

        return recipe

