# Generated by Django 5.1.3 on 2024-12-28 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0009_conge_jours_utilises_conge_solde_restant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conge',
            name='jours_utilises',
        ),
        migrations.RemoveField(
            model_name='conge',
            name='solde_restant',
        ),
        migrations.RemoveField(
            model_name='conge',
            name='statut',
        ),
        migrations.AddField(
            model_name='employe',
            name='solde_annuel',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='employe',
            name='solde_maladie',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='conge',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conges', to='appRH.employe'),
        ),
        migrations.AlterField(
            model_name='conge',
            name='type_conge',
            field=models.CharField(choices=[('Annuel', 'Congé Annuel'), ('Maladie', 'Congé Maladie'), ('Maternité', 'Congé Maternité'), ('Paternité', 'Congé Paternité'), ('SansSolde', 'Congé Sans Solde'), ('Autre', 'Autre')], max_length=50),
        ),
    ]
