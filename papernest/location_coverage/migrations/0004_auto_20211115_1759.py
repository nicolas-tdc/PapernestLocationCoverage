# Generated by Django 3.2.9 on 2021-11-15 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location_coverage', '0003_auto_20211115_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coveragesite',
            name='lat',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coveragesite',
            name='long',
            field=models.CharField(max_length=100),
        ),
    ]
