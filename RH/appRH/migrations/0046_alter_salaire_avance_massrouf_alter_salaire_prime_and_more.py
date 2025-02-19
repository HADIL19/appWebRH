# Generated by Django 5.1.3 on 2025-01-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0045_alter_salaire_avance_massrouf_alter_salaire_prime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salaire',
            name='avance_massrouf',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='salaire',
            name='prime',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='salaire',
            name='retenue_absence',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='salaire',
            name='salaire_de_base',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
