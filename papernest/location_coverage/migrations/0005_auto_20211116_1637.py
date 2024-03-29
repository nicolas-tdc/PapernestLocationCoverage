# Generated by Django 3.2.9 on 2021-11-16 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location_coverage', '0004_auto_20211115_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coveragesite',
            name='coverage_types',
            field=models.ManyToManyField(related_name='coverage_types', to='location_coverage.CoverageType'),
        ),
        migrations.AlterField(
            model_name='coveragesite',
            name='lat',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='coveragesite',
            name='long',
            field=models.CharField(max_length=20),
        ),
    ]
