# Generated by Django 5.1.3 on 2024-12-29 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0012_remove_conge_agent_traitant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaire',
            name='avance_massrouf',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='salaire',
            name='retenue_absence',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
