from django.apps import apps
from django.db import models


def get_client_model():
    return apps.get_model('client', 'Client')


class GroceryItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField(default=1.0)
    unit_of_measure = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.unit_of_measure} {self.name}"


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    amount = models.FloatField(default=1.0)
    unit_of_measure = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.amount} {self.unit_of_measure} {self.name}"


class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    food_category = models.ManyToManyField(FoodCategory, related_name='recipes', blank=True)

    def __str__(self):
        return self.name


class Allergen(models.Model):
    name = models.CharField(max_length=255, unique=True)
    food_items = models.ManyToManyField(FoodItem, related_name='allergens', blank=True)

    def __str__(self):
        return self.name


class MealCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    time_to_make = models.PositiveIntegerField(help_text="Time in minutes")
    recipe_image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    categories = models.ManyToManyField(RecipeCategory, related_name='recipes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Consider if needed
    updated_at = models.DateTimeField(auto_now=True)  # Consider if needed

    def __str__(self):
        return self.name


class MealItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='meal_items')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='meal_items')

    def __str__(self):
        return self.food_item.name if self.food_item else f"Recipe: {self.recipe.name}"


class Meal(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.SET_NULL, null=True, blank=True, related_name='meals')
    name = models.CharField(max_length=255)
    meal_items = models.ManyToManyField(MealItem, related_name='meals')
    description = models.TextField(null=True, blank=True)
    time_to_make = models.PositiveIntegerField(help_text="Time in minutes", null=True, blank=True)
    meal_image = models.ImageField(upload_to='meals/', null=True, blank=True)
    category = models.ForeignKey(MealCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='meals')

    def __str__(self):
        return self.name


class DayPlan(models.Model):
    breakfast = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True, related_name='dayplan_breakfasts')
    lunch = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True, related_name='dayplan_lunches')
    dinner = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True, related_name='dayplan_dinners')

    def __str__(self):
        return f"DayPlan #{self.id}"


class WeekPlan(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name='week_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()
    sunday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_sunday')
    monday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_monday')
    tuesday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_tuesday')
    wednesday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_wednesday')
    thursday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_thursday')
    friday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_friday')
    saturday = models.OneToOneField(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='weekplan_saturday')

    def __str__(self):
        return f"WeekPlan for {self.client.user.email} ({self.start_date} - {self.end_date})"


