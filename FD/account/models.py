# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllergyInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    ingredient = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'allergy_info'
        unique_together = (('id', 'user'),)


class Food(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    food_name = models.CharField(max_length=100)
    serving_size = models.DecimalField(max_digits=5, decimal_places=2)
    serving_size_unit = models.CharField(max_length=5)
    calorie = models.DecimalField(max_digits=8, decimal_places=2)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    sugar = models.DecimalField(max_digits=5, decimal_places=2)
    salt = models.DecimalField(max_digits=7, decimal_places=2)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'food'


class Include(models.Model):
    meal = models.OneToOneField('Meal', models.CASCADE, primary_key=True, related_name = 'include_meal_pk')
    meal_user = models.ForeignKey('Meal', models.CASCADE)
    food = models.ForeignKey(Food, models.CASCADE)
    amount = models.IntegerField()
    amount_unit = models.CharField(max_length=5)
    x = models.DecimalField(max_digits=10, decimal_places=2)
    y = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'include'
        unique_together = (('meal', 'meal_user', 'food'),)


class Likes(models.Model):
    id = models.OneToOneField('User', models.CASCADE, db_column='id', primary_key=True)
    #meal = models.ForeignKey('Meal', models.CASCADE, related_name = 'likes_meal')
    #meal_user = models.ForeignKey('Meal', models.CASCADE, related_name = 'likes_mealUser')

    meal = models.ForeignKey('Meal', models.CASCADE, related_name='meal_id')
    meal_user = models.ForeignKey('Meal', models.CASCADE, related_name='meal_user_id')
    log_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'likes'
        unique_together = (('id', 'meal', 'meal_user'),)



class Meal(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE)
    calories_total = models.DecimalField(max_digits=8, decimal_places=2)
    carbo_total = models.DecimalField(max_digits=5, decimal_places=2)
    protein_total = models.DecimalField(max_digits=5, decimal_places=2)
    fat_total = models.DecimalField(max_digits=5, decimal_places=2)
    sugar_total = models.DecimalField(max_digits=5, decimal_places=2)
    salt_total = models.DecimalField(max_digits=5, decimal_places=2)
    saturated_fat_total = models.DecimalField(max_digits=5, decimal_places=2)
    log_time = models.DateTimeField()
    image_name = models.CharField(max_length=255, blank=True, null=True)
    public_avail = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'meal'
        unique_together = (('id', 'user'),)


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    passwd = models.CharField(max_length=30)
    gender = models.IntegerField()
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    reg_datetime = models.DateTimeField()
    gcode = models.CharField(max_length=10)
    calorie = models.DecimalField(max_digits=8, decimal_places=2)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    sugar = models.DecimalField(max_digits=5, decimal_places=2)
    salt = models.DecimalField(max_digits=5, decimal_places=2)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2)
    intf_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'
