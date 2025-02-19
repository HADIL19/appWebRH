# Generated by Django 5.1.3 on 2024-12-24 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRH', '0004_rename_name_employe_nom_alter_employe_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=15)),
                ('cv_path', models.FileField(upload_to='cvs/')),
            ],
        ),
        migrations.CreateModel(
            name='OffreEmploi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poste', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_publication', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Conge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('type_conge', models.CharField(max_length=50)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conges', to='appRH.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_contrat', models.CharField(max_length=50)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('periode_essai', models.CharField(blank=True, max_length=50, null=True)),
                ('preavis', models.CharField(blank=True, max_length=50, null=True)),
                ('employe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appRH.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Entretien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_entretien', models.CharField(max_length=50)),
                ('date_entretien', models.DateField()),
                ('heure', models.TimeField()),
                ('decision', models.CharField(max_length=50)),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entretiens', to='appRH.candidat')),
                ('recruteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entretiens', to='appRH.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('commentaire', models.TextField()),
                ('type_evaluation', models.CharField(max_length=50)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='appRH.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('theme', models.CharField(max_length=100)),
                ('formulaire', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('employes', models.ManyToManyField(related_name='formations', to='appRH.employe')),
            ],
        ),
        migrations.AddField(
            model_name='candidat',
            name='offre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidats', to='appRH.offreemploi'),
        ),
        migrations.CreateModel(
            name='Pointage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('heure_entree', models.TimeField()),
                ('heure_sortie', models.TimeField(blank=True, null=True)),
                ('statut', models.CharField(max_length=50)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pointages', to='appRH.employe')),
            ],
        ),
        migrations.CreateModel(
            name='Salaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salaire_de_base', models.DecimalField(decimal_places=2, max_digits=10)),
                ('annee', models.IntegerField()),
                ('mois', models.IntegerField()),
                ('prime', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('employe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appRH.employe')),
            ],
        ),
        migrations.AddField(
            model_name='offreemploi',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offres', to='appRH.service'),
        ),
        migrations.AddField(
            model_name='employe',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appRH.service'),
        ),
    ]
