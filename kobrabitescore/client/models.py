from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from mealplanning.models import WeekPlan, GroceryItem, Meal, Recipe, Allergen
from user.models import CustomUser

User = get_user_model()


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])


class PersonFields(models.Model):
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    birthdate = models.DateField(auto_now=False, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    pronouns = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        abstract = True


class Client(PersonFields, SoftDeleteModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile')
    email_opt_in = models.BooleanField(default=False)
    phone_opt_in = models.BooleanField(default=False)
    client_since = models.DateField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='client_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client<{self.first_name} {self.last_name} ({self.id})>"

    def get_name(self):
        try:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        except AttributeError:
            return None


class ClientMealSchedule(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='meal_schedule')
    plans = models.ManyToManyField(WeekPlan, related_name='client_schedules', blank=True)

    def __str__(self):
        return f"Meal Schedule for {self.client.user.email}"


class ClientGroceryList(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='grocery_lists')
    name = models.CharField(max_length=255, default="My Grocery List")
    items = models.ManyToManyField(GroceryItem, related_name='grocery_lists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.client.user.email}"


class ClientRecipe(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by_clients')
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.email} saved {self.recipe.name}"


class ClientMeal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='saved_meals')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='saved_by_clients')
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.user.email} saved {self.meal.name}"


class ClientDiet(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='diet_restrictions')
    calories_per_day = models.PositiveIntegerField(null=True, blank=True)
    allergies = models.ManyToManyField(Allergen, related_name='clients', blank=True)

    def __str__(self):
        return f"Diet for {self.client.user.email}"
