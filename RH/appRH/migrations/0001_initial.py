# Generated by Django 5.1.3 on 2024-11-26 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('daten', models.DateField(verbose_name='Date de naissance')),
                ('date_embauche', models.DateField(verbose_name="Date d'embauche")),
                ('adresse', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Conge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('type_conge', models.CharField(choices=[('ANNUEL', 'Congé Annuel'), ('MALADIE', 'Congé Maladie'), ('MATERNITE', 'Congé Maternité/Paternité'), ('SANS_SOLDE', 'Congé Sans Solde')], max_length=20)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appRH.employe')),
            ],
        ),
        migrations.AddField(
            model_name='employe',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appRH.service'),
        ),
    ]
