# Generated by Django 5.1.3 on 2025-01-01 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0023_rename_email_candidat_emailc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidat',
            name='offre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appRH.offreemploi'),
        ),
    ]
