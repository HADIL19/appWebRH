# Generated by Django 5.1.3 on 2024-12-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0011_conge_agent_traitant_conge_statut_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conge',
            name='agent_traitant',
        ),
        migrations.AlterField(
            model_name='employe',
            name='date_recrutement',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='employe',
            name='sexe',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=10),
        ),
    ]
