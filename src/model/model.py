#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from peewee import SqliteDatabase, Model
from peewee import TextField, CharField, IntegerField, BooleanField, \
                   DateField, DateTimeField, FloatField, \
                   PrimaryKeyField, ForeignKeyField

from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, \
                               TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors

DATABASE = SqliteDatabase('usineagase.sqlite', autocommit=False)
MARGE_VENTE = 1.05


def round05(number):
    """ Fonction pour l'arrondissement au 0.5 près"""
    return (round(number * 20) / 20)


class BaseModel(Model):
    """
    Classe à hériter pour définir directement la base
    de donnée pour chaque model
    """

    class Meta:
        database = DATABASE


class Exercice(BaseModel):
    """
    Classe Exercice
    """

    nom = CharField()
    date_debut = DateField()
    date_fin = DateField()

    def __repr__(self):
        _repr = u"<Exercice : %s du %s au %s>" % (self.nom,
                                                  self.date_debut.strftime("%d/%m/%Y"),
                                                  self.date_fin.strftime("%d/%m/%Y"))
        return _repr.encode("utf-8")

    @classmethod
    def en_cours(cls):
        try:
            return cls.select().where((cls.date_debut < datetime.today()) & (cls.date_fin > datetime.today())).get()
        except:
            return None

    class Meta:
        db_table = 'exercices'


class Fournisseur(BaseModel):
    """
    Classe Fournisseur
    """

    nom = CharField()
    adresse = CharField()
    code_postal = CharField()
    ville = CharField()
    telephone_fixe = CharField(default="")
    telephone_portable = CharField(default="")
    email = CharField(default="")
    nom_contact = CharField(default="")
    remarques = TextField(default="")
    couleur = CharField()

    def __repr__(self):
        _repr = "<Fournisseur : %s>" % self.nom
        return _repr.encode("utf-8")

    def telephone(self):
        telephone = ""
        if len(self.telephone_fixe) > 0:
            telephone += self.telephone_fixe

        if len(self.telephone_portable) > 0:
            if len(self.telephone_fixe) > 0:
                telephone += " - "

            telephone += self.telephone_portable

        return telephone

    class Meta:
        db_table = 'fournisseurs'


class Categorie(BaseModel):
    """
    Classe Categorie
    """

    nom = CharField()

    def __repr__(self):
        _repr = u"<Catégorie : %s>" % self.nom
        return _repr.encode("utf-8")

    def nombre_produits(self):
        """ Retourne le nombre de produits affectés à la catégorie """
        return self.produits.count()

    class Meta:
        db_table = 'categories'


class Tva(BaseModel):
    """
    Classe Tva
    """

    taux = FloatField()

    def __repr__(self):
        _repr = "<Tva : %s %>" % self.taux
        return _repr.encode("utf-8")

    def nombre_produits(self):
        """ Retourne le nombre de produits affectés à la catégorie """
        return self.produits.count()

    class Meta:
        db_table = 'tvas'


class Produit(BaseModel):
    """
    Classe Produit
    """

    pk = PrimaryKeyField()
    id = IntegerField(default=0)
    nom = CharField(default="")
    ref_fournisseur = CharField(default="")
    origine = CharField(default="")
    liquide = BooleanField(default=0)
    vrac = BooleanField(default=0)
    prix_achat_HT = FloatField(default=0)
    poids_volume = IntegerField(default=0)
    conditionnement = IntegerField(default=0)
    stock = IntegerField(default=0)
    retrait = BooleanField(default=False)
    motif_retrait = TextField(default="")
    a_etiquetter = BooleanField(default=True)

    categorie = ForeignKeyField(Categorie, related_name='produits')
    fournisseur = ForeignKeyField(Fournisseur, related_name='produits')
    tva = ForeignKeyField(Tva, related_name='produits')

    def __repr__(self):
        _repr = u"<Produit : %s>" % self.nom
        return _repr.encode("utf-8")

    @property
    def unite(self):
        """ Retourne l'unité du produit """

        if self.vrac:
            if self.liquide:
                return "L"
            else:
                return "kg"
        else:
            return  u"unité"

    def conditionnement_format(self, majuscule=True, pluriel=False):
        """
        Retourne le type de conditionnement

        Arguments :
        majuscule -- si True, mets des majuscules
        majuscule -- si True, mets au pluriel
        """
        conditionnement = ""
        s = pluriel and "s" or ""

        if self.vrac:
            #Permet d'enlever la virgule si le résultat est un entier
            if self.poids_volume % 1000 != 0:
                poids_volume = float(self.poids_volume)/1000
            else:
                poids_volume = self.poids_volume/1000

            if self.liquide:
                conditionnement = "bidon%s de %s L" % (s, str(poids_volume))
            else:
                conditionnement = "sac%s de %s kg" % (s, str(poids_volume))
        else:
            if self.conditionnement > 1:
                conditionnement = u"carton%s de %s unités" % (s, str(self.conditionnement))
            else:
                conditionnement = u"unité%s" % s

        if majuscule:
            return conditionnement.capitalize()
        else:
            return conditionnement

    def prix_achat_TTC(self):
        """ Retourne le prix d'achat TTC """
        return round(float(self.prix_achat_HT) * (1 + self.tva.taux / 100), 2)

    def prix_vente(self):
        """
        Retourne le prix de vente
        en fonction du type de vente (vrac ou à l'unité)
        """

        if self.vrac:
            return round05((self.prix_achat_TTC() * MARGE_VENTE) / \
                           (float(self.poids_volume) / 1000))
        else:
            return round05(self.prix_achat_TTC() * MARGE_VENTE)

    def prix_vente_format(self):
        """
        Retourne le prix de vente formatté
        en fonction du type de vente (vrac ou à l'unité)
        """
        return u"%.2f €" % self.prix_vente() + (self.vrac and " / " + self.unite or "")

    def ref_GASE(self):
        """
        Retourne la référence GASE de type 00-111

        00 -- numéro de la catégorie
        111 --- numéro du produit
        """

        return str(self.categorie.get_id()).zfill(2) + "-" + \
               str(self.id).zfill(3)

    def stock_format(self):
        """ Retourne, formatté, le stock """
        if self.vrac:
            return "%.2f %s" % (float(self.stock)/1000, self.unite)
        else:
            return "%i %s%s" % (self.stock,
                                self.unite,
                                (lambda x: (x.stock > 1 and x.vrac == False) and "s" or  "")(self))

    class Meta:
        db_table = 'produits'


class CotisationType(BaseModel):
    """
    Classe CotisationType
    """

    nom = CharField()
    prix = FloatField()

    def __repr__(self):
        _repr = "<Type de cotisation : %s>" % self.nom
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'cotisations'


class Adherent(BaseModel):
    """
    Classe Adherent
    """

    nom = CharField()
    prenom = CharField()
    adresse = CharField()
    code_postal = CharField()
    ville = CharField()
    email = CharField(default="")
    telephone_fixe = CharField(default="")
    telephone_portable = CharField(default="")
    login = CharField(default="")
    mot_de_passe = CharField(default="")
    ancien_adherent = BooleanField(default=False)
    utilisateur_paniers = BooleanField(default=False)

    cotisation_type = ForeignKeyField(CotisationType, related_name='adherents')

    def __repr__(self):
        _repr = u"<Adhérant : %s>" % self.nom_prenom
        return _repr.encode("utf-8")

    @property
    def prenom_nom(self):
        return self.prenom + " " + self.nom

    @property
    def nom_prenom(self):
        return self.nom + " " + self.prenom

    #TODO : voir si cette méthode est vraiment nécessaire
    """def logins(self):
        try:
            logins = session.query(Adherant.Login).filter(Adherant.Login != \
            self.Login).all()

            return [a for (a,) in logins]

        except BaseException as ex:
            print ex
            return []"""

    @property
    def telephone(self):
        """ Retourne le ou les numéros de téléphone"""
        telephone = ""
        if len(self.telephone_fixe) > 0:
            telephone += self.telephone_fixe

        if len(self.telephone_portable) > 0:
            if len(self.telephone_fixe) > 0:
                telephone += " - "

            telephone += self.telephone_portable

        return telephone

    @property
    def is_adhesion_a_jour(self):
        for adhesion in self.adhesions:
            if adhesion.is_valide():
                return True

        return False

    class Meta:
        db_table = 'adherents'


class Referent(BaseModel):
    """
    Classe Referent
    """

    adherent = ForeignKeyField(Adherent)
    fournisseur = ForeignKeyField(Fournisseur)

    def __repr__(self):
        _repr = "<%s réferent de %s>" % (self.adherent, self.fournisseur)
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'referents'


class AdhesionType(BaseModel):
    """
    Classe AdhesionType
    """

    nom = TextField()
    prix = FloatField()

    def __repr__(self):
        _repr = u"<Type d'adhésion : %s>" % self.nom
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'adhesion_types'


class Adhesion(BaseModel):
    """
    Classe Adhesion
    """

    date = DateField()
    montant = FloatField()
    cheque = CharField(default="0")

    adherent = ForeignKeyField(Adherent, related_name='adhesions')
    adhesion_type = ForeignKeyField(AdhesionType, related_name='adhesions')

    def __repr__(self):
        print self.is_valide()
        _repr = u"<Adhésion de %.2f € pour %s le %s>" % (self.montant,
                                                       self.adherent,
                                                       self.date.strftime("%d/%m/%Y"))

        return _repr.encode("utf-8")

    def is_valide(self):
        """ Permet de vérifier si l'adhésion
        est valide pour l'exercice en cours """

        if Parametre.get(nom="ASSO_typeadhesion").valeur == "1":
            if EXERCICE_EN_COURS:
                if EXERCICE_EN_COURS.date_debut <= self.date <= \
                   EXERCICE_EN_COURS.date_fin:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if self.date + relativedelta(years=+1) > date.today() or \
               self.date < date.today():
                return False
            else:
                return True

    class Meta:
        db_table = 'adhesions'


class Credit(BaseModel):
    """
    Classe Credit
    """

    date = DateField()
    montant = FloatField()
    cheque = CharField()

    adherent = ForeignKeyField(Adherent, related_name='Credits')

    def __repr__(self):
        _repr = "<Credit de %f € pour %s le %s>" % (self.montant,
                                                    self.adherent,
                                                    self.date.strftime("%d/%m/%Y"))
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'credits'


class Achat(BaseModel):
    """
    Classe Achat
    """

    date = DateField()

    adherent = ForeignKeyField(Adherent, related_name='achats')

    def __repr__(self):
        _repr = "<Achat fait par %s le %s>" % (self.adherent,
                                               self.date.strftime("%d/%m/%Y, %H:%M:%S"))
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'achats'


class LigneAchat(BaseModel):
    """
    Classe LigneAchat
    """

    quantite = IntegerField()
    prix_total = FloatField()

    achat = ForeignKeyField(Achat, related_name='lignes_achat')
    produit = ForeignKeyField(Produit)

    def __repr__(self):
        _repr = "<LigneAchat : id_achat %i - produit %s>" % (self.achat.get_id(), self.produit.nom)
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'lignes_achat'


class Commande(BaseModel):
    """
    Classe Commande
    """

    date_commande = DateTimeField(default=datetime.today())
    date_livraison = DateTimeField(null=True)
    _statut = IntegerField(db_column="statut", default=0)
    remarques = TextField(default="")

    fournisseur = ForeignKeyField(Fournisseur, cascade=True, related_name='commandes')

    def __repr__(self):
        _repr = "<Commande pour %s le %s>" % (self.fournisseur, self.date_commande_format())
        return _repr.encode("utf-8")

    def statut_nom(self):
        if self.statut == 0:
            return u"Création"
        elif self.statut == 1:
            return u"Commandée"
        elif self.statut == 2:
            return u"Livrée"
        elif self.statut == 3:
            return u"Vérifiée"
        else:
            return "Statut inconnu"

    def date_commande_format(self):
        if self.statut == 0:
            return u"Pas encore commandée"
        else:
            return self.date_commande.strftime("%d-%m-%Y")

    def date_livraison_format(self):
        if self.date_livraison and self.statut >= 2:
            return self.date_livraison.strftime("%d-%m-%Y")
        elif self.statut == 1:
            return u"En attente de livraison"
        else:
            return "/"

    def total_commande_HT(self):
        total = 0
        for lc in self.lignes_commande:
            total += lc.prix_total_commande_ht

        return total

    def total_commande_TTC(self):
        total = 0
        for lc in self.lignes_commande:
            total += lc.prix_total_commande_ttc

        return total

    def total_livraison_HT(self):
        total = 0
        for lc in self.lignes_commande:
            total += lc.prix_total_livraison_ht

        return total

    def total_livraison_TTC(self):
        total = 0
        for lc in self.lignes_commande:
            total += lc.prix_total_livraison_ttc

        return total

    def total_HT(self):
        if self.statut == 3:
            return self.prix_total_livraison_HT()
        else:
            return self.total_commande_HT()

    def total_TTC(self):
        if self.statut == 3:
            return self.total_livraison_TTC()
        else:
            return self.total_commande_TTC()

    def numero_commande(self):
        n_commande = 1

        for commande in self.fournisseur.commandes:
            if commande.id == self.id:
                break

            n_commande += 1

        return n_commande

    def nombre_lignes_commande(self):
        return len(self.lignes_commande)

    def is_verifiee(self):
        commande_verifiee = True

        for lc in self.lignes_commande:
            if not lc.is_verifiee:
                commande_verifiee = False

        return commande_verifiee

    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, statut):
        if statut == 1:
            self._statut = statut
            self.date_commande = datetime.today()
            return True
        elif statut == 2:
            for lc in self.lignes_commande:
                lc.quantite_livree = lc.quantite_commandee
                lc.prix_total_livraison_ht = lc.prix_total_commande_ht
                lc.prix_total_livraison_ttc = lc.prix_total_livraison_ttc

            self._statut = statut
            self.date_livraison = datetime.today()
            return True
        elif statut == 3:
            #TODO : faire une verif plus correcte, en accros avec GestionCommandes
            #if self.is_verifiee():
            self._statut = statut
            #On augmente le stock
            for lc in self.lignes_commande:
                lc.produit.stock += lc.quantite_livree

            '''    return True
            else:
                return False'''

    def genere_PDF(self, chemin_fichier):

        lst = []

        tableau = []
        tableau.append([Parametre.get(nom="ASSO_nom"),
                        self.fournisseur.nom])
        tableau.append([Parametre.get(nom="ASSO_adresse"),
                        self.fournisseur.adresse])
        tableau.append([Parametre.get(nom="ASSO_codepostal") + " " +
                        Parametre.get(nom="ASSO_ville"),
                        self.fournisseur.code_postal + " " +
                        self.fournisseur.ville])
        tableau.append([Parametre.get(nom="ASSO_telephone"),
                        self.fournisseur.telephone()])
        tableau.append([Parametre.get(nom="ASSO_email"),
                        self.fournisseur.email])

        tableau_entete = Table(tableau, ([10 * cm, 8 * cm]))
        tableau_entete.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 10),
                               ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONT', (0, 1), (-1, -1), 'Helvetica'),
                               ('BOX', (1, 0), (1, -1), 0.5, colors.black)]))

        lst.append(tableau_entete)

        lst.append(Spacer(1, 2 * cm))

        styles = getSampleStyleSheet()

        if self.statut == 0:
            date_commande = datetime.today()
        else:
            date_commande = self.date_commande

        titre = "Bon de commande du " + date_commande.strftime("%d-%m-%Y")

        lst.append(Paragraph(titre, styles["Title"]))

        lst.append(Spacer(1, 2 * cm))

        entete = [u"Reférence", "Nom", u"Quantité", "Prix HT"]

        tableau = []
        tableau.append(entete)

        for lc in self.lignes_commande:
            ligne_commande = []
            ligne_commande.append(lc.produit.ref_fournisseur)
            ligne_commande.append(lc.produit.nom)
            ligne_commande.append(lc.quantite_commandee_conditionnement())
            ligne_commande.append(u"%.2f €" % lc.prix_total_commande_ht)
            tableau.append(ligne_commande)

        tableau.append(["", "", "", ""])
        tableau.append(["", "", "Total HT",
                        u"%.2f €" % self.total_commande_HT()])
        tableau.append(["", "", "Total TTC",
                        u"%.2f €" % self.total_commande_TTC()])

        tableau_commande = Table(tableau,
                                 ([3 * cm, 9 * cm, 4 * cm, 2 * cm]))
        tableau_commande.setStyle(TableStyle([
                               ('FONTSIZE', (0, 0), (-1, -1), 10),
                               ('INNERGRID', (0, 0), (-1, -4), 0.5,
                                colors.black),
                               ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('FONT', (0, 1), (-1, -1), 'Helvetica'),
                               ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
                               ('BOX', (0, 0), (-1, -4), 0.5, colors.black),
                               ('FONT', (2, -1), (3, -1), 'Helvetica-Bold'),
                               #('BACKGROUND',(2,-1),(3,-1),colors.lightgrey),
                               ('INNERGRID', (2, -2), (3, -1), 0.5,
                                colors.black),
                               ('BOX', (2, -2), (3, -1), 0.5, colors.black)]))

        lst.append(tableau_commande)

        #Création des répertoires si ils n'xistent pas
        #dir = os.path.dirname("./Bons de commande/" + self.Fournisseur.Nom +
        # "/")
        #if not os.path.exists(dir):
        #    os.makedirs(dir)

        def pied_de_page(canvas, doc):
            canvas.saveState()
            canvas.setLineWidth(5)
            #canvas.line(66,72,66,PAGE_HEIGHT-72)
            canvas.setFont('Helvetica', 10)
            canvas.drawString(1.5 * cm, cm, self.fournisseur.nom +
                              u" - Commande n°" +
                              str(self.numero_commande()).zfill(3) +
                              " - " + date_commande.strftime("%d-%m-%Y"))
            canvas.drawRightString(A4[0] - (1.5 * cm), cm,
                                   "Page %d" % doc.page)
            canvas.restoreState()

        doc = SimpleDocTemplate(chemin_fichier,
                                title=self.fournisseur.nom + " - " + titre,
                                pagesize=A4,
                                topMargin=2 * cm,
                                bottomMargin=2 * cm,
                                leftMargin=1.5 * cm,
                                rightMargin=1.5 * cm)

        doc.build(lst, onFirstPage=pied_de_page, onLaterPages=pied_de_page)

    class Meta:
        db_table = 'commandes'
        

class LigneCommande(BaseModel):
    """
    Classe LigneCommande
    """

    prix_total_commande_ht = FloatField(default=0)
    prix_total_commande_ttc = FloatField(default=0)
    prix_total_livraison_ht = FloatField(default=0)
    prix_total_livraison_ttc = FloatField(default=0)
    _quantite_commandee = IntegerField(db_column='quantite_commandee', default=0)
    _quantite_livree = IntegerField(db_column='quantite_livree', default=0)

    commande = ForeignKeyField(Commande, cascade=True, related_name='lignes_commande')
    produit = ForeignKeyField(Produit)
    _is_verifiee = False

    def __repr__(self):
        _repr = "<LigneCommande : id_commande %i - produit %s>" % (self.commande.get_id(), self.produit.nom)
        return _repr.encode("utf-8")

    @property
    def quantite_commandee(self):
        #TODO : A nettoyer
        #if self.QuantiteCommandee % self.Produit.UnitesParCarton == 0 :
        #if self.produit.vrac:
        #    return self._quantite_commandee / self.produit.UnitesParCarton
        #else:
        return self._quantite_commandee

    @quantite_commandee.setter
    def quantite_commandee(self, quantite):
        if self.produit and quantite:
            if self.produit.vrac:
                self._quantite_commandee = int(quantite) * \
                                           self.produit.poids_volume
            else:
                self._quantite_commandee = int(quantite)

            self.prix_total_commande_ht = self.produit.prix_achat_HT * \
                                          int(quantite)
            self.prix_total_commande_ttc = round(self.prix_total_commande_ht * \
                                           (1 + (self.produit.tva.taux / 100)), 2)

            self._quantite_livree = self._quantite_commandee
            self.prix_total_livraison_ht = self.prix_total_commande_ht
            self.prix_total_livraison_ttc = self.prix_total_commande_ttc

    @property
    def quantite_livree(self):
        #TODO : A nettoyer
        #if self.QuantiteCommandee % self.Produit.UnitesParCarton == 0 :
        #if self.Produit.vrac :
        #    return self.QuantiteLivree/self.Produit.UnitesParCarton
        #else :
        return self._quantite_livree

    @quantite_livree.setter
    def quantite_livree(self, quantite):
        if self.produit.vrac:
            self._quantite_livree = int(quantite) * \
                                    self.produit.poids_volume
        else:
            self._quantite_livree = int(quantite)

        self.prix_total_livraison_ht = self.produit.prix_achat_HT * int(quantite)
        self.prix_total_livraison_ttc = round(self.prix_total_livraison_ht * \
                                        (1 + (self.produit.tva.taux / 100)), 2)

    @property
    def is_verifiee(self):
        if self.commande.statut == 3:
            self._is_verifiee = True

        return self._is_verifiee

    @is_verifiee.setter
    def is_verifiee(self, value):
        self._is_verifiee = value

    #TODO:fusionner les 2 fonctiones suivantes
    def quantite_commandee_conditionnement(self):        
        if self.quantite_commandee % self.produit.conditionnement == 0:
            if self.produit.vrac:
                return str(self.quantite_commandee / self.produit.poids_volume) + " " + \
                       self.produit.conditionnement_format( \
                                    majuscule=False, \
                                    pluriel=self.quantite_commandee > self.produit.poids_volume)
            else:
                return str(self.quantite_commandee / \
                           self.produit.conditionnement) + " " + \
                           self.produit.conditionnement_format( \
                                majuscule=False, \
                                pluriel=self.quantite_commandee > \
                                self.produit.conditionnement)
        else:
            return str(self.quantite_commandee) + " " + \
                   self.produit.unite + \
                   ("s" if self.quantite_commandee > 1 else "")

    def quantite_livree_conditionnement(self):
        if self.quantite_livree % self.produit.conditionnement == 0:
            if self.produit.vrac:
                return str(self.quantite_livree / self.produit.poids_volume) + " " + \
                       self.produit.conditionnement_format( \
                                    majuscule=False, \
                                    pluriel=self.quantite_livree > self.produit.poids_volume)
            else:
                return str(self.quantite_livree / \
                           self.produit.conditionnement) + " " + \
                           self.produit.conditionnement_format( \
                                majuscule=False, \
                                pluriel=self.quantite_livree > \
                                self.produit.conditionnement)
        else:
            return str(self.quantite_livree) + " " + \
                   self.produit.unite + \
                   ("s" if self.quantite_livree > 1 else "")

    def quantite_commandee_format(self):
        if self.produit.vrac:
            return str(self.quantite_commandee()) + " " + \
                       self.produit.conditionnement_format(majuscule=False, \
                                    pluriel=self.quantite_commandee() > 1)
        else:
            return str(self.quantite_commandee()) + " " + \
                       self.produit.unite + \
                       ("s" if self.quantite_commandee() > 1 else "")

    def quantite_livree_format(self):
        if self.produit.vrac:
            return str(self.quantite_commandee()) + " " + \
                       self.produit.conditionnement_format(majuscule=False, \
                                    pluriel=self.quantite_commandee() > 1)
        else:
            return str(self.quantite_commandee()) + " " + \
                       self.produit.unite + \
                       ("s" if self.quantite_commandee() > 1 else "")

    class Meta:
        db_table = 'lignes_commande'
        

class Inventaire(BaseModel):
    """
    Classe Inventaire
    """

    date = DateField(default=date.today())
    commentaire = TextField(default="")
    is_valide = BooleanField(default=False)

    def initialisation(self):
        for produit in Produit.select().where(Produit.retrait == False or (Produit.retrait == True and Produit.stock > 0)):
            LigneInventaire.create(inventaire=self, produit=produit, stock_theorique=produit.stock)

    def __repr__(self):
        _repr = u"<Inventaire du %s>" % self.date.strftime("%d/%m/%Y")
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'inventaires'


class LigneInventaire(BaseModel):
    """
    Classe LigneInventaire
    """

    stock_theorique = IntegerField(default=0)
    stock_reel = IntegerField(null=True)
    
    inventaire = ForeignKeyField(Inventaire, cascade=True, related_name='lignes_inventaire')
    produit = ForeignKeyField(Produit)

    def __repr__(self):
        _repr = u"<Inventaire du %s : %s>" % (self.inventaire.date.strftime("%d/%m/%Y"), self.produit.nom)
        return _repr.encode("utf-8")

    def stock_theorique_format(self):
        """ Retourne, formatté, le stock théorique """
        if self.produit.vrac:
            return "%.2f %s" % (float(self.stock_theorique)/1000, self.produit.unite)
        else:
            return "%i %s%s" % (self.stock_theorique,
                                self.produit.unite,
                                (lambda x: (x.stock_theorique > 1 and x.produit.vrac == False) and "s" or  "")(self))
            
    def stock_reel_format(self):
        """ Retourne, formatté, le stock réel """
        if self.stock_reel >= 0:        
            if self.produit.vrac:
                return "%.2f %s" % (float(self.stock_reel)/1000, self.produit.unite)
            else:
                return "%i %s%s" % (self.stock_reel,
                                    self.produit.unite,
                                    (lambda x: (x.stock_reel > 1 and x.produit.vrac == False) and "s" or  "")(self))
        else:
            return ""
        
    def stock_difference(self):
        """ Retourne, formatté, la différence enter stock réel et théorique """
        if self.stock_reel >= 0:        
            if self.produit.vrac:
                return "%.2f %s" % (float(self.stock_reel - self.stock_theorique)/1000, self.produit.unite)
            else:
                return "%i %s%s" % (self.stock_reel - self.stock_theorique,
                                    self.produit.unite,
                                    (lambda x: (x.stock_reel > 1 and x.produit.vrac == False) and "s" or  "")(self))
        else:
            return ""

    class Meta:
        db_table = 'lignes_inventaire'


class Parametre(BaseModel):
    """
    Classe Parametre
    """

    nom = CharField(primary_key=True)
    valeur = TextField(default="")

    def __repr__(self):
        _repr = u"<Paramètre : %s" % self.nom
        return _repr.encode("utf-8")

    class Meta:
        db_table = 'parametres'


creation_tables = 1

if creation_tables == 1:
    DATABASE.connect()

    # create the tables
    if not Exercice.table_exists():
        Exercice.create_table()
    if not Fournisseur.table_exists():
        Fournisseur.create_table()
    if not Categorie.table_exists():
        Categorie.create_table()
    if not Tva.table_exists():
        Tva.create_table()
    if not Produit.table_exists():
        Produit.create_table()
    if not CotisationType.table_exists():
        CotisationType.create_table()
    if not Adherent.table_exists():
        Adherent.create_table()
    if not Referent.table_exists():
        Referent.create_table()
    if not AdhesionType.table_exists():
        AdhesionType.create_table()
    if not Adhesion.table_exists():
        Adhesion.create_table()
    if not Credit.table_exists():
        Credit.create_table()
    if not Achat.table_exists():
        Achat.create_table()
    if not LigneAchat.table_exists():
        LigneAchat.create_table()
    if not Commande.table_exists():
        Commande.create_table()
    if not LigneCommande.table_exists():
        LigneCommande.create_table()
    if not Inventaire.table_exists():
        Inventaire.create_table()
    if not LigneInventaire.table_exists():
        LigneInventaire.create_table()
    if not Parametre.table_exists():
        Parametre.create_table()

EXERCICE_EN_COURS = Exercice.en_cours()
