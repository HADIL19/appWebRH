# Generated by Django 5.1.3 on 2024-12-31 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0020_contrat_actif_contrat_fichier_contrat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrat',
            name='fichier_contrat',
        ),
    ]
