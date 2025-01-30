from datetime import date, timedelta, timezone
from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidat, Contrat, Employe, Conge, Entretien, Evaluation, Favori, Formation, OffreEmploi, Pointage, Salaire ,Inscription, Service, Team
from .forms import ContratForm, EmployeForm , CongeForm, EntretienForm, EvaluationForm, FavoriForm, FormationForm, InscriptionForm, MassroufForm, OffreEmploiForm, ServiceForm, inscrireoffreForm,SalaireForm
from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user=form.save()
            group = Group.objects.get(name='Candidat')
            user.groups.add(group)
            return redirect('login')  # Rediriger l'utilisateur vers la page de connexion
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

def home(request):
    # Check if the user belongs to a specific group
    if request.user.groups.filter(name='Candidat').exists():
        return render(request, 'home.html',{'is_candidat':True})  # Use the name of the route
    elif request.user.groups.filter(name='Employe').exists():
        return redirect('coordonnees_employe')  # Use the name defined in your URL pattern
    elif request.user.groups.filter(name='Agent Rh').exists():
        return redirect('dashboardAgent')  # Use the name defined in your URL pattern
    elif request.user.groups.filter(name='Manager').exists():
        return redirect('my_team')  # Use the name defined in your URL pattern
    elif request.user.groups.filter(name='Responsable RH').exists():
        return redirect('liste_contrats')  # Use the name defined in your URL pattern
    else:
        return render(request, 'home.html')

def aboutus(request):
    is_candidat=request.user.groups.filter(name='Candidat').exists()
    return render(request, 'aboutus.html',{'is_candidat':is_candidat})  
  
@login_required
def liste_employes(request):
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()

    # Si l'utilisateur est un employé, afficher uniquement ses informations
    if is_employe:
        mois = date.today().month
        annee = date.today().year
        employes = Employe.objects.filter(user=request.user).select_related('service')
    else:
        # Pour les autres rôles, afficher tous les employés et permettre une recherche
        query = request.GET.get('q', '')
        mois = date.today().month
        annee = date.today().year
        employes = Employe.objects.select_related('service')
        if query:
            employes = employes.filter(Q(nom__icontains=query) | Q(prenom__icontains=query))

    return render(request, "listeemploye.html", {
        "employes": employes, 
        "is_employe": is_employe,
        "is_agent_rh": is_agent_rh,
        'mois': mois,
        'annee': annee,
    })

def detail_employe(request, id):
    try:
        employe = Employe.objects.get(id=id)
    except Employe.DoesNotExist:
        employe = None
    return render(request, "detailemploye.html", {"employe": employe})

def ajouter_employe(request):

    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('liste_employes')  
    else:
        form = EmployeForm()
    return render(request, "ajouteremploye.html", {"form": form})

def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)  
    if request.method == "POST":
        employe.delete()  
        return redirect('liste_employes')  
    return render(request, "supprimeremploye.html", {"employe": employe})

def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)  
    if request.method == "POST":
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()  
            return redirect('liste_employes')  
    else:
        form = EmployeForm(instance=employe)  
    return render(request, "modifieremploye.html", {"form": form, "employe": employe})

def rechercher_employe(request):
    query=request.GET.get('q','')
    if query:
        employes = Employe.objects.filter(
            Q(nom__icontains=query)|Q(prenom__icontains=query)
        )
    else:
        employes = Employe.objects.none()

    return render(request,"rechercheremploye.html",{"employes": employes,"query": query})

@login_required
def liste_conges(request):
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()
    is_responsable_rh = request.user.groups.filter(name='Responsable RH').exists()

    if is_employe:
        # L'employé ne voit que ses propres congés
        try:
            employe = Employe.objects.get(user=request.user)
            conges = Conge.objects.filter(employe=employe)
        except Employe.DoesNotExist:
            conges = []
    else:
        # Les autres rôles voient tous les congés
        conges = Conge.objects.all()
    
    return render(request, 'listconges.html', {
        'conges': conges,
        "is_employe": is_employe,
        "is_agent_rh": is_agent_rh,
        "is_responsable_rh":is_responsable_rh,
    })


@login_required
def demander_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)  # Ne sauvegarde pas encore dans la base de données
            employe = get_object_or_404(Employe, user=request.user)  # Récupère l'employé lié à l'utilisateur
            conge.employe = employe  # Associe l'employé au congé
            conge.save()  # Sauvegarde le congé
            return redirect('voir_coordonnees_conges')  # Redirige vers la page des congés
    else:
        form = CongeForm()
    return render(request, 'demanderconge.html', {'form': form})

def liste_demandes(request):
    demandes = Conge.objects.filter(statut="En attente")
    return render(request, "listedemandes.html", {"demandes": demandes})

def traiter_demande(request, conge_id, action):
    conge = get_object_or_404(Conge, id=conge_id)
    if action == "approuver":
        conge.statut = "Approuvé"
    elif action == "rejeter":
        conge.statut = "Rejeté"
    conge.save()
    return redirect('liste_demandes')


def ajouter_offre(request):
    if request.method == 'POST':
        form = OffreEmploiForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde l'offre d'emploi dans la base de données
            return redirect('liste_offre')  # Redirige vers la liste des offres après ajout
    else:
        form = OffreEmploiForm()  # Affiche un formulaire vide pour un ajout
    return render(request, "ajouteroffre.html", {"form": form})

def supprimer_offre(request, id):
    offre = get_object_or_404(OffreEmploi, id=id)  
    if request.method == "POST":
        offre.delete()  
        return redirect('liste_offre')  
    return render(request, "supprimeroffre.html", {"offre": offre})


def liste_offre(request):
    query = request.GET.get('q', '')
    offre = OffreEmploi.objects.select_related('service')
    
    if query:
        offre = offre.filter(Q(poste__icontains=query) | Q(service__nom__icontains=query))
    
    # Vérifier le rôle de l'utilisateur
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()
    is_candidat = request.user.groups.filter(name='Candidat').exists()
    is_responsable = request.user.groups.filter(name='Responsable RH').exists()


    return render(
        request, 
        "listeoffre.html", 
        {
            "offre": offre, 
            "query": query, 
            "is_agent_rh": is_agent_rh, 
            "is_candidat": is_candidat,
            "is_responsable":is_responsable,
        }
    )


def liste_candidature(request):
    candidature = Candidat.objects.select_related('offre').all()  # Récupère tous les candidats
    return render(request, 'listcandidature.html', {'candidature': candidature})

def liste_demandes_recrutement(request):
    candidature = Candidat.objects.select_related('offre').filter(statut="En attente")
    return render(request, "listedemandesrecrutement.html", {"candidature": candidature})

def traiter_demande_recrutement(request, candidature_id, action):
    candidatur = get_object_or_404(Candidat, id=candidature_id)
    if action == "accepter":
        if request.method == "POST":
            form = EntretienForm(request.POST)
            if form.is_valid():
                entretien = form.save(commit=False)
                recruteur = form.cleaned_data['recruteur']  # Le recruteur sélectionné
                entretien.recruteur = recruteur  # Assigner le recruteur sélectionné
                entretien.candidat = candidatur
                entretien.save()
                candidatur.statut = "accepté"
                candidatur.save()
                return redirect('liste_demandes_recrutement')
        else:
            form = EntretienForm()
        return render(request, 'entretien_form.html', {'form': form, 'candidat': candidatur})
        
    elif action == "refuser":
        candidatur.statut = "Refusé"
        candidatur.save()
    return redirect('liste_demandes_recrutement')

       
def liste_entretiens(request):
    entretiens = Entretien.objects.all()
    return render(request, 'liste_entretiens.html', {'entretiens': entretiens})

@login_required
def voir_coordonnees(request):
    # Vérifier si l'utilisateur est un candidat
    if not request.user.groups.filter(name='Candidat').exists():
        return redirect('home')
    
    try:
        # Essayer de récupérer le candidat
        candidat = Candidat.objects.get(user=request.user)
    except Candidat.DoesNotExist:
        # Si le candidat n'existe pas, le créer
        candidat = Candidat(
            user=request.user,
            nomC=f"{request.user.first_name} {request.user.last_name}",
            emailC=request.user.email
        )
        candidat.save()
    
    # Récupérer toutes les inscriptions du candidat
    inscriptions = Inscription.objects.filter(candidat=candidat).select_related('offre')
    
    context = {
        'candidat': candidat,
        'inscriptions': inscriptions
    }
    
    return render(request, 'voircoordonnees.html', context)


def inscrire_offre(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)

    # Vérifier si le candidat est déjà inscrit à cette offre
    existing_inscription = Inscription.objects.filter(
        candidat__user=request.user,
        offre=offre
    ).exists()

    if existing_inscription:
        messages.error(request, "Vous êtes déjà inscrit à cette offre.")
        return redirect('voir_coordonnees')

    try:
        # Essayer de récupérer le candidat existant
        candidat = Candidat.objects.get(user=request.user)
    except Candidat.DoesNotExist:
        # Créer un nouveau candidat avec les champs requis
        candidat = Candidat(
            user=request.user,
            nomC=f"{request.user.first_name} {request.user.last_name}",
            emailC=request.user.email,
            offre=offre
        )

    if request.method == 'POST':
        form = inscrireoffreForm(request.POST, request.FILES, instance=candidat)
        if form.is_valid():
            try:
                # Sauvegarder le candidat
                candidat = form.save(commit=False)
                candidat.offre = offre

                # Gérer l'upload du CV
                if 'cv_path' in request.FILES:
                    candidat.cv_path = request.FILES['cv_path']
                candidat.save()

                # Créer l'inscription si elle n'existe pas déjà
                inscription, created = Inscription.objects.get_or_create(
                    candidat=candidat,
                    offre=offre,
                    defaults={'status': 'En attente'}  # Vous pouvez ajouter un statut par défaut
                )

                if created:
                    messages.success(request, "Votre inscription a été enregistrée avec succès!")
                else:
                    messages.info(request, "Vous étiez déjà inscrit à cette offre.")
                
                return redirect('voir_coordonnees')

            except IntegrityError:
                messages.error(request, "Une erreur s'est produite lors de l'inscription.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = inscrireoffreForm(instance=candidat)

    return render(request, 'inscrireoffre.html', {
        'form': form,
        'offre': offre
    })

def dashboardAgent(request):
    # Exemple de récupération des données
    total_offres = OffreEmploi.objects.count()  # Nombre d'offres d'emploi
    total_candidats = Candidat.objects.count()  # Nombre de candidats inscrits
    total_employes = Employe.objects.count()  # Nombre d'employés

    context = {
        'total_offres': total_offres,
        'total_candidats': total_candidats,
        'total_employes': total_employes,
    }
    
    return render(request, 'dashboardAgant.html', context)

def detail_entretien(request, candidat_id):
    candidat = get_object_or_404(Candidat, id=candidat_id)
    # Vérifier qu'il existe un entretien pour ce candidat
    try:
        entretien = Entretien.objects.get(candidat=candidat)
    except Entretien.DoesNotExist:
        entretien = None    
    # Passer 'entretien' et 'candidat' dans le contexte
    return render(request, 'entretien_details.html', {'entretien': entretien, 'candidat': candidat})

@login_required
def fiche_paie(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()
    
    # Vérifier si l'utilisateur est l'employé concerné par la fiche de paie
    if request.user.groups.filter(name='Employe').exists():
        try:
            employe = Employe.objects.get(user=request.user)
            if salaire.employe != employe:
                return redirect('home')  # Rediriger si ce n'est pas sa fiche de paie
        except Employe.DoesNotExist:
            return redirect('home')
            
    salaire_net = salaire.calculer_salaire()
    return render(request, 'fichepaie.html', {
        'salaire': salaire, 
        'salaire_net': salaire_net,        
        "is_employe": is_employe,
        "is_agent_rh": is_agent_rh,
    })
@login_required
def liste_salaires(request):
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()
    
    if is_employe:
        # L'employé ne voit que ses propres salaires
        try:
            employe = Employe.objects.get(user=request.user)
            salaires = Salaire.objects.filter(employe=employe)
        except Employe.DoesNotExist:
            salaires = []
    else:
        # Les autres rôles voient tous les salaires
        salaires = Salaire.objects.select_related('employe').all()
    
    return render(request, 'listesalaires.html', {
        'salaires': salaires,
        "is_employe": is_employe,
        "is_agent_rh": is_agent_rh,
    })
def ajouter_salaire(request):
    if request.method == "POST":
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('liste_salaires')  
    else:
        form = SalaireForm()
    return render(request, "ajoutersalaire.html", {"form": form})

def demander_massrouf(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    
    if request.method == 'POST':
        form = MassroufForm(request.POST, instance=salaire)
        justification = request.POST.get('justification_massrouf', '')
        
        if form.is_valid():
            montant = form.cleaned_data['avance_massrouf']
            
            # Vérifier le nombre de demandes annuelles
            demandes_annuelles = salaire.get_demandes_annuelles()
            if demandes_annuelles >= 2:
                messages.error(request, "Vous avez déjà atteint la limite de deux demandes de massrouf pour cette année.")
                return redirect('voir_coordonnees_salaires')
            
            try:
                # Vérification des règles de montant et justification
                if not salaire.verifier_massrouf(montant, justification):
                    messages.error(request, "Montant non valide ou justification manquante. Le montant ne doit pas dépasser la moitié du salaire de base.")
                    return redirect('demander_massrouf', salaire_id=salaire_id)
                
                # Enregistrer le mois et l'année de la demande
                now = timezone.now()
                salaire.mois_demande = str(now.month).zfill(2)
                salaire.annee_demande = now.year
                salaire.avance_massrouf = montant
                salaire.demandes_massrouf = 1  # Marquer qu'une demande a été faite
                salaire.justification_massrouf = justification
                salaire.salaire_de_base -= montant
                salaire.save()

                messages.success(request, "Votre demande de massrouf a été enregistrée avec succès.")
                return redirect('voir_coordonnees_salaires')
                
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('demander_massrouf', salaire_id=salaire_id)
    else:
        form = MassroufForm(instance=salaire)
    
    # Ajouter le nombre de demandes restantes au contexte
    demandes_annuelles = salaire.get_demandes_annuelles()
    demandes_restantes = 2 - demandes_annuelles
    
    return render(request, 'demandermassrouf.html', {
        'form': form, 
        'salaire': salaire,
        'demandes_restantes': demandes_restantes
    })

def mettre_a_jour_absences():
    employes = Employe.objects.all()  # Récupérer tous les employés
    for employe in employes:
        # Compter les absences mensuelles
        absences_mensuelles = Pointage.objects.filter(
            employe=employe,
            statut='Absent',
            date__month=date.today().month  # Filtrer par le mois actuel
        ).count()
        # Vérifier si l'objet Salaire existe pour l'employé, l'année et le mois
        salaire, created = Salaire.objects.get_or_create(
            employe=employe,
            annee=date.today().year,
            mois=date.today().month,)
        # Debugging: Vérification des données
        print(f"Employe: {employe.nom} {employe.prenom}")
        print(f"Absences mensuelles: {absences_mensuelles}")
        print(f"Salaire avant mise à jour: {salaire.absences}")
        # Mise à jour du champ absences dans le salaire
        salaire.absences = absences_mensuelles
        salaire.save()  # Sauvegarder les modifications
        # Debugging: Vérification après sauvegarde
        print(f"Salaire après mise à jour: {salaire.absences}")


@login_required
def liste_contrats(request):
    query = request.GET.get('q', '')
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()
    is_responsable_rh = request.user.groups.filter(name='Responsable RH').exists()

    if is_employe:
        # L'employé ne voit que ses propres contrats actifs
        try:
            employe = Employe.objects.get(user=request.user)
            contrats = Contrat.objects.filter(employe=employe, actif=True)
        except Employe.DoesNotExist:
            contrats = []
    else:
        # Les autres rôles voient tous les contrats actifs
        contrats = Contrat.objects.filter(actif=True)
        if query:
            contrats = contrats.filter(
                Q(employe__nom__icontains=query) |
                Q(type_contrat__icontains=query) |
                Q(date_debut__icontains=query) |
                Q(date_fin__icontains=query)
            )
    
    return render(request, 'listcontrats.html', {
        'contrats': contrats, 
        'query': query,
        "is_employe": is_employe,
        "is_agent_rh": is_agent_rh,
        "is_responsable_rh": is_responsable_rh,
    })

def ajouter_contrat(request):
    if request.method == "POST":
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')
    else:
        form = ContratForm()
    return render(request, 'ajoutercontrat.html', {'form': form})

def modifier_contrat(request, id):
    contrat = Contrat.objects.get(id=id)
    if request.method == "POST":
        form = ContratForm(request.POST, request.FILES, instance=contrat)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')
    else:
        form = ContratForm(instance=contrat)
    return render(request, 'modifiercontrat.html', {'form': form})

@login_required
def afficher_contrat(request, id):
    is_employe = request.user.groups.filter(name='Employe').exists()
    contrat = get_object_or_404(Contrat, id=id)
    
    # Vérifier si l'utilisateur est l'employé concerné par le contrat
    if is_employe:
        try:
            employe = Employe.objects.get(user=request.user)
            if contrat.employe != employe:
                return redirect('home')  # Rediriger si ce n'est pas son contrat
        except Employe.DoesNotExist:
            return redirect('home')
            
    return render(request, 'affichercontrat.html', {
        "contrat": contrat,
        "is_employe": is_employe,  # Ajout de la virgule manquante
    })


def archiver_contrat(request, id):
    contrat = get_object_or_404(Contrat, id=id)
    if request.method == "POST":
        contrat.actif = False  # Marquer le contrat comme inactif
        contrat.save()  # Sauvegarder la modification
        return redirect('liste_contrats')
    return render(request, 'supprimercontrat.html', {'contrat': contrat})

def liste_archives(request):
    query = request.GET.get('q', '')
    archives = Contrat.objects.filter(actif=False)  # Contrats archivés
    if query:
        archives = archives.filter(
            Q(employe__nom__icontains=query) |
            Q(type_contrat__icontains=query) |
            Q(date_debut__icontains=query) |
            Q(date_fin__icontains=query)
        )
    return render(request, 'listearchives.html', {'archives': archives, 'query': query})

def restaurer_contrat(request, id):
    contrat = Contrat.objects.get(id=id)
    contrat.actif = True  # Marquer comme actif
    contrat.save()
    return redirect('liste_archives')

def rechercher_contrat(request):
    query = request.GET.get('q', '')  # Recherche globale (nom de l'employé ou type de contrat)
    type_contrat = request.GET.get('type_contrat', '')  # Filtrer par type de contrat
    date_debut = request.GET.get('date_debut', '')  # Filtrer par date de début
    date_fin = request.GET.get('date_fin', '')  # Filtrer par date de fin
    archive = request.GET.get('archive', 'actif')  # Filtrer actifs ou archivés (par défaut : actif)

    # Base : Actifs ou Archivés
    if archive == 'archivés':
        contrats = Contrat.objects.filter(actif=False)
    else:
        contrats = Contrat.objects.filter(actif=True)

    # Appliquer les filtres supplémentaires
    if query:
        contrats = contrats.filter(
            Q(employe__nom__icontains=query) |  # Recherche par prénom de l'employé
            Q(type_contrat__icontains=query)            # Recherche par type de contrat
        )
    if type_contrat:
        contrats = contrats.filter(type_contrat__icontains=type_contrat)
    if date_debut:
        contrats = contrats.filter(date_debut__gte=date_debut)  # Date de début ≥ valeur fournie
    if date_fin:
        contrats = contrats.filter(date_fin__lte=date_fin)  # Date de fin ≤ valeur fournie

    # Rendu de la page avec les résultats
    return render(request, 'recherchercontrat.html', {
        'contrats': contrats,
        'query': query,
        'type_contrat': type_contrat,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'archive': archive
    })

def alertes_contrats(request):
    # Vérifiez si l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return render(request, "alertescontrats.html", {"alertes": [], "message": "Vous devez être connecté pour voir vos alertes."})

    # Récupérer l'employé lié à l'utilisateur connecté
    employe = request.user.employe
    today = now().date()
    alertes = []

    # Récupérer les contrats actifs pour l'employé connecté
    contrats = Contrat.objects.filter(actif=True, employe=employe)

    for contrat in contrats:
        # Vérifier si le contrat approche de sa fin
        if contrat.date_fin and today >= contrat.date_fin - timedelta(days=30):  # Alerte 30 jours avant expiration
            alertes.append({
                'message': "Votre contrat arrive à expiration. Veuillez envisager un renouvellement.",
                'contrat_id': contrat.id,
                'date_fin': contrat.date_fin,
                'days_until_expiration': (contrat.date_fin - today).days  # Calcul du nombre de jours restants
            })

        # Vérifier si la période d'essai est terminée
        elif today > contrat.fin_periode_essai() and contrat.renouvellements < 3:
            alertes.append({
                'message': "La période d'essai est terminée.",
                'contrat_id': contrat.id,
                'date_fin': contrat.date_fin,
                'days_since_trial_end': (today - contrat.fin_periode_essai()).days  # Calcul des jours depuis la fin de la période d'essai
            })

    return render(request, "alertescontrats.html", {"alertes": alertes})

@login_required
def voir_coordonnees_employe(request):
    try:
        employe = Employe.objects.get(user=request.user)
        
        context = {
            'employe': employe,
        }
        return render(request, 'informations_employe.html', context)
    
    except Employe.DoesNotExist:
        return redirect('home')

def voir_coordonnees_contrat(request):
    try:
        employe = Employe.objects.get(user=request.user)
        contrats = Contrat.objects.filter(employe=employe, actif=True)
        if not contrats:
            messages.warning(request, "Aucune donnée associée trouvée.")

        context = {
            'employe': employe,
            'contrats': contrats,
        }
        return render(request, 'contrat_employe.html', context)
    
    except Employe.DoesNotExist:
        return redirect('home')

def voir_coordonnees_conges(request):
    try:
        employe = Employe.objects.get(user=request.user)
        conges = Conge.objects.filter(employe=employe)
        
        context = {
            'employe': employe,
            'conges': conges,
        }
        return render(request, 'conges_employe.html', context)
    
    except Employe.DoesNotExist:
        return redirect('home')

def voir_coordonnees_salaires(request):
    try:
        employe = Employe.objects.get(user=request.user)
        salaires = Salaire.objects.filter(employe=employe)
        if not salaires:
            messages.warning(request, "Aucune donnée associée trouvée.")

        context = {
            'employe': employe,
            'salaires': salaires,
        }
        return render(request, 'salaires_employe.html', context)
    
    except Employe.DoesNotExist:
        return redirect('home')

def liste_formations(request):
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_agent_rh = request.user.groups.filter(name='Agent Rh').exists()

    # Vérification si l'utilisateur est un employé et récupération des formations
    formations = Formation.objects.all()  # Par défaut, récupérer toutes les formations

    try:
        employe = Employe.objects.get(user=request.user)  # Récupérer l'employé actuel
    except Employe.DoesNotExist:
        employe = None

    if is_employe:
        # L'employé ne peut voir que ses propres formations
        formations = Formation.objects.filter(employe=employe)  # Assurez-vous que 'employe' est bien défini dans le modèle Formation
    else:
        # Les autres rôles voient toutes les formations
        formations = Formation.objects.all()

    return render(request, 'liste_formations.html', {
        'formations': formations,
        'employe': employe,
        'is_employe': is_employe,
        'is_agent_rh': is_agent_rh,
    })


def ajouter_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_formations')
    else:
        form = FormationForm()
    return render(request, 'ajouter_formation.html', {'form': form})

def detail_formation(request, id):
    formation = get_object_or_404(Formation, id=id)
    return render(request, 'detail_formation.html', {'formation': formation}) 


@login_required
def inscrire_employe(request, formation_id, employe_id):
    # Récupérer la formation et l'employé
    formation = get_object_or_404(Formation, id=formation_id)
    employe = get_object_or_404(Employe, id=employe_id)

    # Vérification des droits d'accès
    # L'agent RH ou l'employé peuvent inscrire un employé
    if request.user != employe.user and not request.user.groups.filter(name='Agent Rh').exists():
        return HttpResponseForbidden("Vous n'êtes pas autorisé à inscrire cet employé.")

    # Vérification si l'employé est déjà inscrit à la formation
    if employe in formation.employe.all():
        message = "Vous êtes déjà inscrit à cette formation."
    else:
        formation.employe.add(employe)  # Ajouter l'employé à la formation
        formation.save()  # Sauvegarder la modification
        message = "Votre inscription a été prise en compte avec succès !"

    # Afficher un message de confirmation ou d'erreur
    return render(request, 'inscription_confirmation.html', {
        'formation': formation,
        'message': message
    })

def voir_coordonnees_formation(request):
    employe = get_object_or_404(Employe, user=request.user)
    formations = employe.formations.all()  # Assuming a ManyToMany relation between Employe and Formation
    return render(request, 'formation_employe.html', {'formations': formations})



def liste_services(request):
    query = request.GET.get('q', '')
    services = Service.objects.all()
    if query:
        services = services.filter(Q(code__icontains=query) | Q(nom__icontains=query))
    return render(request, "listeservices.html", {"services": services, "query": query})


def ajouter_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_services')
    else:
        form = ServiceForm()
    return render(request, "ajouterservice.html", {"form": form})

def supprimer_service(request, id):
    services = get_object_or_404(Service, id=id)
    if request.method == "POST":
        services.delete()
        return redirect('liste_services')
    return render(request, "supprimerservice.html", {"services": services})

def modifier_service(request, id):
    services = get_object_or_404(Service, id=id)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=services)
        if form.is_valid():
            form.save()
            return redirect('liste_services')
    else:
        form = ServiceForm(instance=services)
    return render(request, "modifierservice.html", {"form": form, "services": services})

def rechercher_service(request):
    query=request.GET.get('q','')
    if query:
        services = Service.objects.filter(
            Q(code__icontains=query)|Q(nom__icontains=query)
        )
    else:
        services = Service.objects.none()

    return render(request,"rechercherservice.html",{"services": services,"query": query})

def rechercher_offre (request):
    query=request.GET.get('q','')
    if query:
        offres = OffreEmploi.objects.filter(
            (Q(poste__icontains=query) | Q(service__nom__icontains=query))
        )
    else:
        offres = OffreEmploi.objects.none()

    return render(request,"rechercheroffre.html",{"offres": offres,"query": query})

def liste_favoris(request):
    favoris = Favori.objects.filter(user=request.user)  # Filtrer par utilisateur
    return render(request, 'listefavoris.html', {'favoris': favoris})
pass

def ajouter_favori(request):
    if request.method == 'POST':
        form = FavoriForm(request.POST)
        if form.is_valid():
            favori = form.save(commit=False)
            favori.user = request.user  # Associe le favori à l'utilisateur connecté
            favori.save()
            return redirect('liste_favoris')
    else:
        form = FavoriForm()
    return render(request, 'ajouterfavori.html', {'form': form})

def supprimer_favori(request, id):
    favori = get_object_or_404(Favori, id=id, user=request.user)
    if request.method == 'POST':
        favori.delete()
        return redirect('liste_favoris')
    return render(request, 'supprimerfavori.html', {'favori': favori})


def rapport_absences(request, employe_id, mois, annee):
    # Récupérer l'employé
    employe = get_object_or_404(Employe, pk=employe_id)
    
    # Filtrer les absences pour l'employé, mois et année donnés
    absences = Pointage.objects.filter(
        employe=employe,
        date__year=annee,
        date__month=mois,
        statut="Absent"
    )
    
    # Renvoyer le contexte au template
    return render(request, 'rapportabsences.html', {
        'employe': employe,
        'absences': absences,
        'mois': mois,
        'annee': annee,
    })

def saisir_pointage(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    if request.method == 'POST':
        date = request.POST.get('date', now().date())
        statut = request.POST.get('statut', 'Absent')
        heure_entree = request.POST.get('heure_entree', None)

        # Vérifier si heure_entree est vide ou invalide
        if not heure_entree:
            heure_entree = None

        # Créer ou mettre à jour le pointage pour cette date
        pointage, created = Pointage.objects.get_or_create(
            employe=employe,
            date=date,
            defaults={
                'statut': statut,
                'heure_entree': heure_entree,
                'agent': request.user,
            }
        )
        if not created:  # Si le pointage existe déjà, mettre à jour
            pointage.statut = statut
            pointage.heure_entree = heure_entree
            pointage.agent = request.user
            pointage.save()

        return redirect('liste_employes')

    return render(request, 'saisirpointage.html', {'employe': employe})

def create_team(request):
    if request.method == "POST":
        name = request.POST.get("name")
        manager_id = request.POST.get("manager")
        members_ids = request.POST.getlist("members")

        manager = User.objects.get(id=manager_id)
        team = Team.objects.create(name=name, manager=manager)

        for member_id in members_ids:
            member = Employe.objects.get(id=member_id)
            team.members.add(member)

        return redirect("team_list")  # Redirection après création

    managers = User.objects.filter(groups__name="Manager")
    employees = Employe.objects.all()
    return render(request, "create_team.html", {"managers": managers, "employees": employees})

def my_team(request):
    team = Team.objects.filter(manager=request.user).first()
    if not team:
        return render(request, "error.html", {"message": "Vous n'avez pas d'équipe associée."})

    return render(request, "my_team.html", {"team": team})


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team_list.html', {'teams': teams})

def evaluate_employee(request, employee_id):
    employee = get_object_or_404(Employe, id=employee_id)

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)  # Crée l'évaluation sans la sauvegarder immédiatement
            evaluation.employe = employee  # On lie l'employé à l'évaluation
            evaluation.save()  # Sauvegarde l'évaluation
            return redirect('my_team')  # Redirige vers la page de l'équipe après l'évaluation
    else:
        form = EvaluationForm()

    return render(request, 'evaluate_employee.html', {'form': form, 'employee': employee})

def view_employee_evaluations(request, employee_id):
    is_employe = request.user.groups.filter(name='Employe').exists()
    is_manager = request.user.groups.filter(name='Manager').exists()
    is_agent = request.user.groups.filter(name='Agent Rh').exists()
    is_responsable = request.user.groups.filter(name='Responsable RH').exists()

    employee = get_object_or_404(Employe, id=employee_id)
    evaluations = Evaluation.objects.filter(employe=employee)

    return render(request, 'view_employee_evaluations.html', {
        'employee': employee,
        'evaluations': evaluations,
        'is_employe':is_employe,
        'is_manager':is_manager,
        'is_agent':is_agent,
        'is_responsable':is_responsable
    })