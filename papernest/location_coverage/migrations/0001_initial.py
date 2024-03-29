# Generated by Django 3.2.9 on 2021-11-11 01:40

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoverageSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_coordinates', models.FloatField()),
                ('y_coordinates', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ref_code', models.IntegerField()),
                ('countries', django_countries.fields.CountryField(max_length=746, multiple=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoverageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
                ('coverage_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location_coverage.coveragesite')),
            ],
        ),
        migrations.AddField(
            model_name='coveragesite',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location_coverage.provider'),
        ),
    ]
