# Generated by Django 5.1.3 on 2025-01-21 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0039_alter_formation_formateure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidat',
            name='offre',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='appRH.offreemploi'),
        ),
    ]
