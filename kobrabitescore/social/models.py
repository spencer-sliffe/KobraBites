from django.db import models

from client.models import Client
from mealplanning.models import Recipe, RecipeCategory, Meal, MealCategory


class SharedRecipe(models.Model):
    shared_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='shared_recipes')
    shared_at = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shared_variants')
    number_of_saves = models.PositiveIntegerField(default=0)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    comments = models.TextField(null=True, blank=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='shared_recipes')
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Shared Recipe: {self.recipe.name} by {self.shared_by.user.email}"


class SharedMeal(models.Model):
    shared_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='shared_meals')
    shared_at = models.DateTimeField(auto_now_add=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='shared_variants')
    number_of_saves = models.PositiveIntegerField(default=0)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    comments = models.TextField(null=True, blank=True)
    category = models.ForeignKey(MealCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='shared_meals')
    video = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Shared Meal: {self.meal.name} by {self.shared_by.user.email}"

