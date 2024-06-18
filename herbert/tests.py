from django.test import TestCase

# Create your tests here.
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Category

class RecipeBookTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
    def test_user_registration(self):
        # Test user registration functionality
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/success.html')
        
    def test_user_authentication(self):
        # Test user authentication functionality
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        
    def test_recipe_creation(self):
        # Test recipe creation functionality
        category = Category.objects.create(name='Breakfast')
        response = self.client.post('/recipes/create/', {
            'title': 'Pancakes',
            'description': 'Delicious breakfast pancakes',
            'ingredients': 'Flour, milk, eggs',
            'instructions': 'Mix ingredients and cook on a pan',
            'category': category.id,
        })
        self.assertEqual(response.status_code, 302)
        
        recipe = Recipe.objects.get(title='Pancakes')
        self.assertEqual(recipe.description, 'Delicious breakfast pancakes')
        
    def test_recipe_update(self):
        # Test recipe update functionality
        recipe = Recipe.objects.create(
            title='Pizza',
            description='Homemade pizza recipe',
            ingredients='Dough, cheese, tomato sauce',
            instructions='Roll out dough, add toppings, bake',
            category=Category.objects.create(name='Dinner'),
            user=self.user
        )
        
        response = self.client.post(f'/recipes/{recipe.id}/update/', {
            'title': 'Margherita Pizza',
            'description': 'Classic Margherita pizza recipe',
            'ingredients': 'Dough, mozzarella, tomato sauce',
            'instructions': 'Roll out dough, add toppings, bake',
            'category': recipe.category.id,
        })
        self.assertEqual(response.status_code, 302)
        
        updated_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(updated_recipe.title, 'Margherita Pizza')
        
    def test_recipe_deletion(self):
        # Test recipe deletion functionality
        recipe = Recipe.objects.create(
            title='Salad',
            description='Healthy salad recipe',
            ingredients='Lettuce, tomatoes, cucumbers',
            instructions='Chop vegetables, toss with dressing',
            category=Category.objects.create(name='Lunch'),
            user=self.user
        )
        
        response = self.client.post(f'/recipes/{recipe.id}/delete/')
        self.assertEqual(response.status_code, 302)
        
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe.id)
            
    def test_category_assignment(self):
        # Test category assignment functionality
        category = Category.objects.create(name='Dessert')
        recipe = Recipe.objects.create(
            title='Cake',
            description='Delicious cake recipe',
            ingredients='Flour, sugar, eggs',
            instructions='Mix ingredients, bake, decorate',
            category=category,
            user=self.user
        )
        
        self.assertEqual(recipe.category.name, 'Dessert')