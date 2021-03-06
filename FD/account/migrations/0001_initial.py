# Generated by Django 3.2.8 on 2021-10-10 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllergyInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ingredient', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'allergy_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('food_name', models.CharField(max_length=100)),
                ('serving_size', models.DecimalField(decimal_places=2, max_digits=5)),
                ('serving_size_unit', models.CharField(max_length=5)),
                ('calorie', models.DecimalField(decimal_places=2, max_digits=8)),
                ('carbohydrate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sugar', models.DecimalField(decimal_places=2, max_digits=5)),
                ('salt', models.DecimalField(decimal_places=2, max_digits=5)),
                ('saturated_fat', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'food',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('calories_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('carbo_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('protein_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sugar_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('salt_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('saturated_fat_total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('log_time', models.DateTimeField()),
                ('image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('public_avail', models.IntegerField()),
            ],
            options={
                'db_table': 'meal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=30)),
                ('gender', models.IntegerField()),
                ('age', models.IntegerField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('reg_datetime', models.DateTimeField()),
                ('gcode', models.CharField(max_length=10)),
                ('calorie', models.DecimalField(decimal_places=2, max_digits=8)),
                ('carbohydrate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sugar', models.DecimalField(decimal_places=2, max_digits=5)),
                ('salt', models.DecimalField(decimal_places=2, max_digits=5)),
                ('saturated_fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('intf_type', models.IntegerField()),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Include',
            fields=[
                ('meal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='include_meal_pk', serialize=False, to='account.meal')),
                ('amount', models.IntegerField()),
                ('amount_unit', models.CharField(max_length=5)),
                ('x', models.DecimalField(decimal_places=2, max_digits=10)),
                ('y', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'include',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.user')),
                ('log_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'likes',
                'managed': False,
            },
        ),
    ]
