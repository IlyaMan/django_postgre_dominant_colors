# Generated by Django 2.2.3 on 2019-07-24 12:16

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('image', '0002_auto_20190724_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='colors',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0),
                                                                        django.core.validators.MaxValueValidator(255)]),
                size=3), blank=True, default=None, null=True, size=3),
        ),
    ]
