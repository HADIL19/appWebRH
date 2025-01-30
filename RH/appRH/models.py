from datetime import date, datetime, timedelta, timezone
from django.db import models
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.timezone import now
from django.utils import timezone



# Create your models here.

class Employe(models.Model):
    # Champs principaux
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relier chaque employé à un utilisateur
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True) 
    tel = models.CharField(max_length=10)  # Ajout d'une validation
    adresse = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')])
    lieu_naissance = models.CharField(max_length=50)
    date_naissance = models.DateField(null=True, blank=True)
    date_recrutement = models.DateField(auto_now_add=True)
    situation_fam = models.CharField(max_length=50)
    fonction = models.CharField(max_length=50)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    
    def jours_absence_par_mois(self, mois, annee):
        absences = self.pointage_set.filter(
            statut='Absent',
            date__year=annee,
            date__month=mois
        ).count()
        return absences

    def clean(self):
        if not self.tel.isdigit():
            return False

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Conge(models.Model):
    TYPE_CONGE = [
        ('Annuel', 'Congé Annuel'),
        ('Maladie', 'Congé Maladie'),
        ('Maternité', 'Congé Maternité'),
        ('Paternité', 'Congé Paternité'),
        ('SansSolde', 'Congé Sans Solde'),
        ('Autre', 'Autre'),
    ]

    STATUTS_DEMANDE = [
        ('En attente', 'En attente'),
        ('Approuvé', 'Approuvé'),
        ('Rejeté', 'Rejeté'),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')
    type_conge = models.CharField(max_length=50, choices=TYPE_CONGE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    solde_annuel = models.IntegerField(default=30)  
    solde_maladie = models.IntegerField(default=10)
    statut = models.CharField(max_length=20, choices=STATUTS_DEMANDE, default='En attente')

    def jours_utilises(self):
        return (self.date_fin - self.date_debut).days + 1

    def clean(self):
        if self.date_debut > self.date_fin:
            return False

    def save(self, *args, **kwargs):
        if self.statut == 'Approuvé':
            jours = self.jours_utilises()
            if self.type_conge == 'Annuel' and self.solde_annuel < jours:
                return False
            elif self.type_conge == 'Maladie' and self.solde_maladie < jours:
                return False
            # Mise à jour des soldes
            if self.type_conge == 'Annuel':
                self.solde_annuel -= jours
            elif self.type_conge == 'Maladie':
                self.solde_maladie -= jours
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_conge} ({self.employe.nom})"

    
class Service(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.nom}"

class Formation(models.Model):
    titre = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    formateure = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    employe = models.ManyToManyField('Employe', related_name="formations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_debut']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def clean(self):
        if self.date_fin <= self.date_debut:
            raise ValidationError("La date de fin doit être après la date de début.")

    def nombre_employe(self):
        return self.employe.count()

    def __str__(self):
        return self.titre

class Evaluation(models.Model):
    date = models.DateField()
    score = models.IntegerField()
    commentaire = models.TextField()
    type_evaluation = models.CharField(max_length=50)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)

class Contrat(models.Model):
    TYPE_CONTRAT = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('STAGE', ' STAGE'),
        ('Autre', 'Autre'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')
    type_contrat = models.CharField(max_length=50,choices=TYPE_CONTRAT)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    periode_essai = models.CharField(max_length=50, null=True, blank=True)
    preavis = models.CharField(max_length=50, null=True, blank=True)
    actif = models.BooleanField(default=True)  # Actif ou archivé
    renouvellements = models.PositiveIntegerField(default=0)
    
    def fin_periode_essai(self):
        # Gérer différentes unités de période d'essai
        if "mois" in self.periode_essai.lower():
            nb_mois = int(self.periode_essai.split()[0])
            return self.date_debut + relativedelta(months=nb_mois)
        elif "jours" in self.periode_essai.lower():
            nb_jours = int(self.periode_essai.split()[0])
            return self.date_debut + timedelta(days=nb_jours)
        else:
            return self.date_debut  # Pas de période d'essai valide

    def est_en_periode_essai(self):
        return now().date() <= self.fin_periode_essai() # type: ignore

    def __str__(self):
        return f"{self.employe.nom} "


class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    salaire_de_base = models.DecimalField(max_digits=10, decimal_places=2)
    annee = models.IntegerField()
    mois = models.IntegerField()
    prime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    retenue_absence = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avance_massrouf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    demandes_massrouf = models.IntegerField(default=0)  
    justification_massrouf = models.TextField(null=True, blank=True)
    absences = models.IntegerField(default=0)  
    mois_demande = models.CharField(max_length=2, null=True, blank=True)
    annee_demande = models.IntegerField(null=True, blank=True)

    def get_demandes_annuelles(self):
        return Salaire.objects.filter(
            employe=self.employe,
            annee_demande=self.annee,
            demandes_massrouf__gt=0
        ).count()
    
    def verifier_massrouf(self, montant, justification):
        # Vérifier le nombre de demandes annuelles
        demandes_annuelles = self.get_demandes_annuelles()
        
        if demandes_annuelles >= 2:
            return False
        if not justification:
            return False
        if montant > self.salaire_de_base / 2:
            return False
        return True

    def reset_massrouf_requests(self):
        now = timezone.now()
        salaires_annee_precedente = Salaire.objects.filter(
            employe=self.employe,
            annee=now.year - 1
        )
        for salaire in salaires_annee_precedente:
            salaire.demandes_massrouf = 0
            salaire.save()

    def calculer_retenue_absence(self):
        salaire_jour = self.salaire_de_base / 30
        self.retenue_absence = self.absences * salaire_jour
        self.save()

    def calculer_salaire(self):
        self.calculer_retenue_absence()
        salaire_net = (
            self.salaire_de_base
            + (self.prime or 0)
            - self.retenue_absence
            - self.avance_massrouf
        )
        return round(salaire_net, 2)

    def save(self, *args, **kwargs):
        if not self.pk or self._state.adding:
            now = timezone.now()
            if not self.mois_demande:
                self.mois_demande = str(now.month).zfill(2)
            if not self.annee_demande:
                self.annee_demande = now.year
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Salaire de {self.employe.nom} {self.employe.prenom} ({self.mois}/{self.annee})"

class OffreEmploi(models.Model):
    poste = models.CharField(max_length=50)
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.poste}"

class Candidat(models.Model):
    STATUTS_DEMANDE = [
        ('En attente', 'En attente'),
        ('Accepter', 'Accepté'),
        ('Refuser', 'Resusé'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nomC = models.CharField(max_length=50)
    emailC = models.EmailField()
    telC = models.CharField(max_length=10)
    cv_path = models.FileField(upload_to="cvs/")
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE, null=True, blank=True )
    statut = models.CharField(max_length=20, choices=STATUTS_DEMANDE, default='En attente')

    def __str__(self):
        return f"{self.nomC}"
   
class Entretien(models.Model):
    STATUTS_DECISION = [
        ('En attente', 'En attente'),
        ('Accepter', 'Accepté'),
        ('Refuser', 'Resusé'),
    ]
    type_entretien = models.CharField(max_length=50, choices=[('En ligne', 'En ligne'), ('Présentiel', 'Présentiel')])
    recruteur = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="entretiens")
    date_entretien = models.DateField()
    heure = models.TimeField()
    decision = models.CharField(max_length=20, choices=STATUTS_DECISION, default='En attente')
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entretien pour {self.candidat.nomC} le {self.date_entretien} à {self.heure}"
    

class Pointage(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='pointage_set')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Agent qui saisit
    date = models.DateField()
    heure_entree = models.TimeField(null=True, blank=True)
    heure_sortie = models.TimeField(null=True, blank=True)
    statut = models.CharField(
        max_length=50,
        choices=[('Présent', 'Présent'), ('Absent', 'Absent')],
        default='Présent'
    )

    def verifier_absence(self):
        if not self.heure_entree:
            self.statut = 'Absent'
            self.save()

class Inscription(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='En attente')

    class Meta:
        # Assure qu'un candidat ne peut s'inscrire qu'une fois à une offre
        unique_together = ('candidat', 'offre')

    def __str__(self):
        return f"{self.candidat.nomC} "

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favoris")  # L'utilisateur (agent RH)
    nom = models.CharField(max_length=100)  # Nom de la fonctionnalité favorite
    url = models.CharField(max_length=255)  # URL de la fonctionnalité

    def __str__(self):
        return f"{self.nom} (par {self.user.username})"
    
class Team(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(Employe, related_name="teams")

    def str(self):
        return f"Équipe: {self.name} (Manager: {self.manager.username})"