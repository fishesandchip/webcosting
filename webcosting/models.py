# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

from validators import validate_lower_than_100

class Coefficient(models.Model):
    """Représente les coefficients utilisés dans la méthode COCOMO

    La valeur du coefficient dépend du type de projet. Il y a 4 coefficients
    différents.
    """

    def __unicode__(self):
        return self.type_projet + '-' + self.type_coefficient

    TYPE_PROJET_CHOIX = (
        ('organique', 'organique'),
        ('semi-détaché', 'semi-détaché'),
        ('embarqué', 'embarqué'),
    )

    type_projet = models.CharField(
        max_length=10,
        choices=TYPE_PROJET_CHOIX,
        default='organique'
    )

    TYPE_COEFFICIENT_CHOIX = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    type_coefficient = models.CharField(
        max_length=2,
        choices=TYPE_COEFFICIENT_CHOIX,
        default='A',
    )

    valeur_coefficient = models.FloatField(
        default=None,
    )


class LanguageDeProgrammation(models.Model):
    """Classe représentant un language de programmation.

    A chaque language est associé une estimation du nombre de lignes de code
    nécessaires par points de fonctions. Ceci est utilisé dans la méthode
    des points de fonctions.

    TODO: mettre à jour les références
    """

    def __unicode__(self):
        return self.language_de_programmation

    language_de_programmation = models.CharField(
        'language de programmation',
        max_length=100
    )

    ligne_de_code = models.IntegerField(
        'ligne de code par points de fonctions',
    )


class TailleProjet(models.Model):
    """Représente la taille d'un projet.

    Selon la taille du projet, l'estimation de la charge de travail par points
    de fonctions (dans la méthode des points de fonctions) est différente.
    """

    def __unicode__(self):
        return str(self.taille_projet)

    taille_projet = models.CharField(
        'taille du projet',
        max_length=30,
    )

    charge_de_travail = models.PositiveIntegerField(
        'charge de travail en jour homme par points de fonctions'
    )


class TypeFonction(models.Model):
    """Représente un type de fonction.

    Dans la méthode des points de fonctions, chaque fonction peut être de 5
    types différents.
    """

    def __unicode__(self):
        return self.type_fonction

    TYPE_FONCTION_CHOIX = (
        ('données internes', 'données internes'),
        ('données externes', 'données externes'),
        ('entrées', 'entrées'),
        ('sorties', 'sorties'),
        ('interrogation', 'interrogation')
    )

    type_fonction = models.CharField(
        max_length=20,
        choices=TYPE_FONCTION_CHOIX,
        default='données internes'
    )


class CalculPointDeFonction(models.Model):
    """Référence servant à calculer le nombre de points de fonctions.

    Le nombre de points de fonctions dépend du type de fonction, du
    nombre de sous-fonctions et du nombre de données élémentaires.

    TODO: la complexité ne semble pas être utilisée, à vérifier.
    """

    type_fonction = models.ForeignKey(
        TypeFonction,
        on_delete=models.CASCADE,
        default=None
    )

    nombre_sous_fonction_deb = models.PositiveIntegerField(
        default=0
    )

    nombre_sous_fonction_fin = models.PositiveIntegerField(
        default=0
    )

    nombre_donnees_elementaires_deb = models.PositiveIntegerField(
        default=0
    )

    nombre_donnees_elementaires_fin = models.PositiveIntegerField(
        default=0
    )

    COMPLEXITE_CHOIX = (
        ('faible', 'faible'),
        ('moyen', 'moyen'),
        ('élevé', 'élevé')
    )

    complexite = models.CharField(
        max_length=10,
        choices=COMPLEXITE_CHOIX,
        default='moyen'
    )

    nombre_point_de_fonction = models.PositiveIntegerField(
        'nombre de points de fonctions',
        default=0
    )


class Projet(models.Model):
    """Représente un projet."""

    def __unicode__(self):
        return self.nom_projet

    nom_projet = models.CharField(
        'nom du projet',
        max_length=100,
        default=None
    )

    date_dernier_enregistrement = models.DateTimeField(
        'date du dernier enregistrement',
        auto_now=True,
        null=True
    )

    ORGANIQUE = 'OR'
    SEMIDETACHE = 'SD'
    EMBARQUE = 'EM'

    TYPE_PROJET_CHOIX = (
        (ORGANIQUE, 'organique'),
        (SEMIDETACHE, 'semi-détaché'),
        (EMBARQUE, 'embarqué'),
    )

    type_projet = models.CharField(
        'type de projet',
        max_length=2,
        choices=TYPE_PROJET_CHOIX,
        default='organique'
    )

    taille_projet = models.ForeignKey(
        TailleProjet,
        on_delete=models.CASCADE,
        default='moyen'
    )

    language_de_programmation = models.ForeignKey(
        LanguageDeProgrammation,
        on_delete=models.CASCADE,
        default='java'
    )

    facteur_ajustement = models.IntegerField(
        default=1,
    )

    FIAB_CHOIX = (
        (0.75, 'très bas: 0.75'),
        (0.88, 'bas: 0.88'),
        (1.00, 'moyen: 1.00'),
        (1.15, 'élevé: 1.15'),
        (1.40, 'très élevé: 1.40'),
    )

    fiab = models.FloatField(
        'fiabilité requise du logiciel',
        choices=FIAB_CHOIX,
        default=1.00,
    )

    DONN_CHOIX = (
        (0.94, 'bas (0.94)'),
        (1.00, 'moyen (1.00)'),
        (1.08, 'élevé (1.08)'),
        (1.16, 'très élevé (1.16)'),
    )

    donn = models.FloatField(
        'taille de la base de données',
        choices=DONN_CHOIX,
        default=1.00,
    )

    CPLX_CHOIX = (
        (0.70, 'très bas: 0.70'),
        (0.85, 'bas: 0.85'),
        (1.00, 'moyen: 1.00'),
        (1.15, 'élevé: 1.15'),
        (1.30, 'très élevé: 1.30'),
        (1.65, 'très très élevé: 1.65'),
    )

    cplx = models.FloatField(
        'complexité du produit',
        choices=CPLX_CHOIX,
        default=1.00,
    )

    TEMP_CHOIX = (
        (1.00, 'moyen: 1.00'),
        (1.11, 'élevé: 1.11'),
        (1.30, 'très élevé: 1.30'),
        (1.66, 'très très élevé: 1.66'),
    )

    temp = models.FloatField(
        'contrainte sur le temps d\'exécution',
        choices=TEMP_CHOIX,
        default=1.00,
    )

    ESPA_CHOIX = (
        (1.00, 'moyen: 1.00'),
        (1.06, 'élevé: 1.06'),
        (1.21, 'très élevé: 1.21'),
        (1.56, 'très très élevé: 1.56'),
    )

    espa = models.FloatField(
        'contrainte sur l\'espace de stockage',
        choices=ESPA_CHOIX,
        default=1.00,
    )

    VIRT_CHOIX = (
        (0.87, 'bas: 0.87'),
        (1.00, 'moyen: 1.00'),
        (1.15, 'élevé: 1.15'),
        (1.30, 'très élevé: 1.30'),
    )

    virt = models.FloatField(
        'volatilité de la machine virtuelle',
        choices=VIRT_CHOIX,
        default=1.00,
    )

    CSYS_CHOIX = (
        (0.87, 'bas: 0.87'),
        (1.00, 'moyen: 1.00'),
        (1.07, 'élevé: 1.07'),
        (1.15, 'très élevé: 1.15'),
    )

    csys = models.FloatField(
        'contrainte du système de développement',
        choices=CSYS_CHOIX,
        default=1.00,
    )

    APTA_CHOIX = (
        (1.46, 'très bas: 1.46'),
        (1.19, 'bas: 1.19'),
        (1.00, 'moyen: 1.00'),
        (0.86, 'élevé: 0.86'),
        (0.71, 'très élevé: 0.71'),
    )

    apta = models.FloatField(
        'aptitude à l\'analyse',
        choices=APTA_CHOIX,
        default=1.00,
    )

    EXPA_CHOIX = (
        (1.29, 'très bas: 1.29'),
        (1.13, 'bas: 1.13'),
        (1.00, 'moyen: 1.00'),
        (0.91, 'élevé: 0.91'),
        (0.82, 'très élevé: 0.82'),
    )

    expa = models.FloatField(
        'expérience dans le domaine de l\'application',
        choices=EXPA_CHOIX,
        default=1.00,
    )

    APTP_CHOIX = (
        (1.42, 'très bas: 1.42'),
        (1.17, 'bas: 1.17'),
        (1.00, 'moyen: 1.00'),
        (0.86, 'élevé: 0.86'),
        (0.70, 'très élevé: 0.70'),
    )

    aptp = models.FloatField(
        'aptitude à la programmation',
        choices=APTP_CHOIX,
        default=1.00,
    )

    EXPV_CHOIX = (
        (1.21, 'très bas: 1.21'),
        (1.10, 'bas: 1.10'),
        (1.00, 'moyen: 1.00'),
        (0.95, 'élevé: 0.95'),
    )

    expv = models.FloatField(
        'expérience de la machine virtuelle',
        choices=EXPV_CHOIX,
        default=1.00,
    )

    EXPL_CHOIX = (
        (1.14, 'très bas: 1.14'),
        (1.07, 'bas: 1.07'),
        (1.00, 'moyen: 1.00'),
        (0.95, 'élevé: 0.95'),
    )

    expl = models.FloatField(
        'expérience dans le language de programmation',
        choices=EXPL_CHOIX,
        default=1.00,
    )

    PMOD_CHOIX = (
        (1.24, 'très bas: 1.24'),
        (1.10, 'bas: 1.10'),
        (1.00, 'moyen: 1.00'),
        (0.91, 'élevé: 0.91'),
        (0.82, 'très élevé: 0.82'),
    )

    pmod = models.FloatField(
        'méthode de programmation moderne',
        choices=PMOD_CHOIX,
        default=1.00,
    )

    OLOG_CHOIX = (
        (1.24, 'très bas: 1.24'),
        (1.10, 'bas: 1.10'),
        (1.00, 'moyen: 1.00'),
        (0.91, 'élevé: 0.91'),
        (0.83, 'très élevé: 0.83'),
    )

    olog = models.FloatField(
        'disponibilité d\'outils logiciels',
        choices=OLOG_CHOIX,
        default=1.00,
    )

    DREQ_CHOIX = (
        (1.23, 'très bas: 1.23'),
        (1.08, 'bas: 1.08'),
        (1.00, 'moyen: 1.00'),
        (1.04, 'élevé: 1.04'),
        (1.10, 'très élevé: 1.10'),
    )

    dreq = models.FloatField(
        'écart avec le modèle Cocomo simple',
        choices=DREQ_CHOIX,
        default=1.00,
    )

    def get_absolute_url(self):
        """Retourne l'url de l'objet.

        Permet, dans les templates, de construire des liens de type:
        <a href="{{ object.get_absolute_url }}">{{ object.name }}</a>

        Cela évite de hardcoder des urls et rend les modifications
        ultérieures d'urls plus simples.
        """
        return reverse('webcosting:projet', kwargs={'pk': self.pk})

    """L'utilisation des 'property' permet d'inclure des champs calculés dans
    le modèle. Cf cette réponse:
    http://stackoverflow.com/questions/11465293/create-a-field-which-value-is-a-calculation-of-other-fields-values
    """
    @property
    def point_de_fonction_brut(self):
        """Calcule le nombre total de points de fonctions bruts du projet."""
        fonctions = Fonction.objects.filter(projet=self.id)

        point_de_fonction_brut = 0
        for fonction in fonctions:
            point_de_fonction_brut += fonction.point_de_fonction_brut

        return point_de_fonction_brut

    @property
    def point_de_fonction_net(self):
        """Calcule le nombre total de points de fonctions nets du projet."""
        return self.facteur_ajustement * self.point_de_fonction_brut

    @property
    def charge_de_travail_point_de_fonction(self):
        """Calcule la charge de travail par point de fonction (en jours)."""

        taille_projet = TailleProjet.objects.get(taille_projet=self.taille_projet)

        charge_de_travail = taille_projet.charge_de_travail

        return charge_de_travail * self.point_de_fonction_net

    @property
    def charge_de_travail_point_de_fonction_mois(self):
        """Calcule la charge de travail par point de fonction (en mois)."""

        return self.charge_de_travail_point_de_fonction / 30.0



    @property
    def kilo_ligne_de_code(self):
        """Calcule le nombre de lignes de code d'un projet.

        L'unité utilisée est le kilo ligne de code, soit 1000 lignes de code.
        """
        language_de_programmation = LanguageDeProgrammation.objects.get(language_de_programmation=self.language_de_programmation)

        ligne_de_code = language_de_programmation.ligne_de_code

        ligne_de_code = ligne_de_code * self.point_de_fonction_net

        kilo_ligne_de_code = ligne_de_code / 1000.0

        return kilo_ligne_de_code

    @property
    def effort_simple(self):
        """Calcule l'effort simple selon la méthode Cocomo.

        L'effort simple est une première estimation rapide de la charge de
        travail liée à un projet.
        """
        A = Coefficient.objects.get(
            type_coefficient='A',
            type_projet=self.type_projet,
        )

        A = A.valeur_coefficient

        B = Coefficient.objects.get(
            type_coefficient='B',
            type_projet=self.type_projet,
        )

        B = B.valeur_coefficient

        ligne_de_code = self.kilo_ligne_de_code

        effort_simple = A * (ligne_de_code ** B)
        effort_simple = round(effort_simple, 2)

        return effort_simple

    @property
    def effort_intermediaire(self):
        """Calcule l'effort intermédiaire selon la méthode Cocomo.

        L'effort intermédiaire est une estimation plus complexe de la charge
        de travail liée à un projet, basée sur le calcul de l'effort simple.
        """
        effort_simple = self.effort_simple

        effort_intermediaire = effort_simple * (
            self.fiab * self.donn * self.cplx * self.temp *
            self.espa * self.virt * self.csys * self.apta * self.expa *
            self.aptp * self.expv * self.expl * self.pmod * self.olog * self.dreq
        )

        effort_intermediaire = round(effort_intermediaire, 2)

        return effort_intermediaire

    @property
    def temps_de_developpement(self):
        """Calcule le temps de développement (en mois) d'un projet.

        Le temps de développement est basé sur le calcul de l'effort
        intermédiaire et sur deux coefficients, C et D, qui dépendent
        de la taille du projet.
        """
        C = Coefficient.objects.get(
            type_coefficient='C',
            type_projet=self.type_projet
        )

        D = Coefficient.objects.get(
            type_coefficient='D',
            type_projet=self.type_projet
        )

        C = C.valeur_coefficient

        D = D.valeur_coefficient

        effort_intermediaire = self.effort_intermediaire

        temps_de_developpement = C * (effort_intermediaire ** D)
        temps_de_developpement = round(temps_de_developpement, 2)

        return temps_de_developpement


class Fonction(models.Model):
    """Représente une fonction, dans la méthode des points de fonctions."""

    def __unicode__(self):
        return self.nom_fonction

    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        default=None
    )

    nom_fonction = models.CharField(
        'nom de la fonction',
        max_length=100,
        default=None
    )

    type_fonction = models.ForeignKey(
        TypeFonction,
        on_delete=models.CASCADE,
        default='données internes'
    )

    nombre_sous_fonction = models.PositiveIntegerField(
        'nombre de sous-fonctions (\'GDR ou SLD\')',
        default=0,
    )

    nombre_donnees_elementaires = models.PositiveIntegerField(
        'nombre de données élémentaires',
        default=0,
        validators=[validate_lower_than_100],

    )

    def get_absolute_url(self):
        """Retourne l'url de l'objet.

        Permet, dans les templates, de construire des liens de type:
        <a href="{{ object.get_absolute_url }}">{{ object.name }}</a>

        Cela évite de hardcoder des urls et rend les modifications
        ultérieures d'urls plus simples.
        """
        return reverse('webcosting:fonction', kwargs={'projet_id': self.projet.id})

    @property
    def point_de_fonction_brut(self):
        """Calcule le nombre de points de fonction bruts d'une fonction."""
        calcul_point_de_fonction = CalculPointDeFonction.objects.get(
            type_fonction=self.type_fonction,
            nombre_sous_fonction_deb__lte=self.nombre_sous_fonction,
            nombre_sous_fonction_fin__gte=self.nombre_sous_fonction,
            nombre_donnees_elementaires_deb__lte=self.nombre_donnees_elementaires,
            nombre_donnees_elementaires_fin__gte=self.nombre_donnees_elementaires
        )
        return calcul_point_de_fonction.nombre_point_de_fonction

    @property
    def point_de_fonction_net(self):
        """Calcule le nombre de points de fonction nets d'une fonction."""
        return self.projet.facteur_ajustement * self.point_de_fonction_brut
