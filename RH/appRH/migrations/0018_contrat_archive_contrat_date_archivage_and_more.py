# Generated by Django 5.1.3 on 2024-12-31 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0017_salaire_absences'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrat',
            name='archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contrat',
            name='date_archivage',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='type_contrat',
            field=models.CharField(choices=[('CDI', 'Contrat à Durée Indéterminée'), ('CDD', 'Contrat à Durée Déterminée'), ('Stage', 'Stage'), ('Autre', 'Autre')], max_length=50),
        ),
    ]
