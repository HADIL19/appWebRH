# Generated by Django 5.1.3 on 2024-12-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0016_remove_employe_solde_annuel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaire',
            name='absences',
            field=models.IntegerField(default=0),
        ),
    ]
