# Generated by Django 5.0.6 on 2024-05-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meep',
            name='photo',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images/'),
        ),
    ]