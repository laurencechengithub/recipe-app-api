
from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient

# IngredientsSerializer must be before recipe due to nest serializer pattern
class IngredientSerializer(serializers.ModelSerializer):
    "Serializers for ingredients"
    class Meta:
        model = Ingredient
        fields = ['id','name']
        read_only_fields = ['id']


# tagSerializer must be before recipe due to nest serializer
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
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id','title','time_minutes','price','link',
            'tags','ingredients',
        ]
        read_only_fields = ['id']

    # the _getxxx underline means that this method is internal only
    def _get_or_create_tags(self, tags, recipe):
        "Handle get and create tags while needed"
                #get the authenticated user
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, create = Tag.objects.get_or_create(
                user=auth_user,
                **tag, # or can write as name=tag['name'],
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self,ingredents, recipe):
        "Handle get and create ingredient while needed when create recipe"
        auth_user = self.context['request'].user
        for ingredient in ingredents:
            #below will either get the object of already exist or it'll create a new one
            ingredient_obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    #default nested serializer are read only, thus we need to create custom
    #adding a new method in class to override the original create method
    def create(self, validated_data):
        "create a recipe"
        #tags exists, remove it from validated_data and asign it to new varibale
        tags = validated_data.pop('tags',[])
        #if ingredients exists, remove it from validated_data and asign it to new varibale
        ingredients = validated_data.pop('ingredients',[])
        #and the rest of validated_data (that tags are exculded)
        #we are going to create recipe with those value
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)
        return recipe

    #since it's update, instance => the existed instance
    def update(self, instance, validated_data):
        "update recipe"
        #get the tag from valited_data assign it to <tags>,
        #if it's nono than set it to None
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            #clear the tags from instance
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)
        #rest of valitated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

# using RecipeSerializer as the base class since it's just an extension of the that
# with some few extra fields only
class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

