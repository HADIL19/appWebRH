# Generated by Django 5.1.3 on 2024-12-28 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0006_remove_candidat_offre_alter_candidat_tel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemandeConge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_demande', models.DateField(auto_now_add=True)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('type_conge', models.CharField(max_length=50)),
                ('statut', models.CharField(default='En attente', max_length=20)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes_conge', to='appRH.employe')),
            ],
        ),
    ]
