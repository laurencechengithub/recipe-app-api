"""
Tests for recipe APIs.
"""
from decimal import Decimal
import email

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)

#test working with tags
from core.models import Tag

RECIPES_URL = reverse('recipe:recipe-list')

# RecipeDetail Test
def recipe_detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


#Recipe test functions
def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests. 沒有登入 所以401"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        #test the recipe are retuned in order of id, order by reverse order
        recipes = Recipe.objects.all().order_by('-id')
        #pass all the recipe into the recipe serializer, (many=true, tells that we pass throught a list of items)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #the response data must be equal to the serializer data
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)



    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = recipe_detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)


    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        res = self.client.post(RECIPES_URL, payload) #post the payload recipe to url: /api/recipes/recipe

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #after sucessful created, than we retrieve a recipe with the id
        recipe = Recipe.objects.get(id=res.data['id'])
        print("@@"+str(recipe))

        for k, v in payload.items():
            print("kkk"+str(k))
            print('vvv'+str(v))
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
            """Test partial update of a recipe."""
            original_link = 'https://example.com/recipe.pdf'
            recipe = create_recipe(
                user=self.user,
                title='Sample recipe title',
                link=original_link,
            )

            payload = {'title': 'New recipe title'}
            url = recipe_detail_url(recipe.id)
            res = self.client.patch(url, payload)

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            recipe.refresh_from_db()
            self.assertEqual(recipe.title, payload['title'])
            self.assertEqual(recipe.link, original_link)
            self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test full update of recipe."""
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title',
            link='https://exmaple.com/recipe.pdf',
            description='Sample recipe description.',
        )

        payload = {
            'title': 'New recipe title',
            'link': 'https://example.com/new-recipe.pdf',
            'description': 'New recipe description',
            'time_minutes': 10,
            'price': Decimal('2.50'),
        }
        url = recipe_detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        url = recipe_detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe successful."""
        recipe = create_recipe(user=self.user)

        url = recipe_detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_recipe_other_users_recipe_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        recipe = create_recipe(user=new_user)

        url = recipe_detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())


#Test create tags from recipes

    def test_create_recipe_with_new_tags(self):
            """Test creating a recipe with new tags."""
            #create one recipe with tags
            payload = {
                'title': 'Thai Prawn Curry',
                'time_minutes': 30,
                'price': Decimal('2.50'),
                'tags': [{'name': 'Thai'}, {'name': 'Dinner'}],
            }
            #request payload as json
            res = self.client.post(RECIPES_URL, payload, format='json')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

            #get the authrnticated user's recipe from all recipes
            recipes = Recipe.objects.filter(user=self.user)
            #make sure it's recipe.count = 1 so recipes[0] wont return nil
            self.assertEqual(recipes.count(), 1)
            the_first_recipe = recipes[0]
            self.assertEqual(the_first_recipe.tags.count(), 2)
            for tag in payload['tags']:
                exists = the_first_recipe.tags.filter(
                    name=tag['name'],
                    user=self.user,
                ).exists()
                self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        """Test creating a recipe with existing tag."""
        tag_indian = Tag.objects.create(user=self.user, name='Indian')
        payload = {
            'title': 'Pongal',
            'time_minutes': 60,
            'price': Decimal('4.50'),
            'tags': [{'name': 'Indian'}, {'name': 'Breakfast'}],
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_indian, recipe.tags.all())
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)