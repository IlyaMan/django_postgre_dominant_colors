# Generated by Django 2.2.3 on 2019-07-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='path',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]
