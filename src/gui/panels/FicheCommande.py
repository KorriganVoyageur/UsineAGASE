#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import wx.lib.agw.genericmessagedialog as GMD

from lib.objectlistview import ObjectListView, ColumnDefn, Filter
from textwrap import fill

from classes.Validators import GenericTextValidator, VALIDATE_INT

from model.model import Commande, LigneCommande, Produit, DATABASE
from gui.dialogs.ChoixQuantite import ChoixQuantite

###########################################################################
## Class FicheCommande
###########################################################################


class FicheCommande(wx.Panel):
    def __init__(self, parent, commande=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if commande == None:
            commande = Commande.create()

        self.commande = commande

        self.sizer_commande_staticbox = wx.StaticBox(self, -1, "Commande")
        self.sizer_fournisseur_produits_staticbox = wx.StaticBox(self, -1, "Liste des produits")
        self.label_titre_commande = wx.StaticText(self, -1, "Commande pour ")
        self.button_infos_fournisseur = wx.Button(self, -1, "Afficher les infos du fournisseur")
        self.label_FiltreRecherche = wx.StaticText(self, -1, "Recherche sur le nom :")
        self.text_ctrl_FiltreRecherche = wx.TextCtrl(self, -1, "")
        self.liste_produits = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.label_total = wx.StaticText(self, -1, "Total de la commande :")
        self.label_total_valeur = wx.StaticText(self, -1, u"0.00 €", style=wx.ALIGN_RIGHT)
        self.liste_lignes_commande = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.button_Sauvegarder = wx.Button(self, -1, "Enregistrer la commande")

        self.liste_produits.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "ref_GASE", minimumWidth=100),
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn("Prix TTC", "right", -1, "prix_achat_TTC", stringConverter=u"%.2f €", minimumWidth=100),
            ColumnDefn("Conditionnement", "left", -1, "conditionnement_format", isSpaceFilling=True, minimumWidth=200)
        ])
        self.liste_produits.SetEmptyListMsg("Ce fournisseur n'a aucun produit")
        self.liste_produits.AutoSizeColumns()

        self.liste_lignes_commande.SetColumns([
            ColumnDefn("Ref Fournisseur", "left", -1, "produit.ref_fournisseur", minimumWidth=120),
            ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=100),
            ColumnDefn(u"Quantité", "left", -1, "quantite_commandee_conditionnement", minimumWidth=150),
            ColumnDefn("Total TTC", "right", -1, "prix_total_commande_ttc", stringConverter=u"%s €", isSpaceFilling=True, minimumWidth=100)
        ])
        self.liste_lignes_commande.AutoSizeColumns()

        self.liste_lignes_commande.SetEmptyListMsg("La commande ne contient aucun produit")

        self.__set_properties()
        self.__set_values()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onInfosFournisseur, self.button_infos_fournisseur)
        self.Bind(wx.EVT_BUTTON, self.onSauvegarder, self.button_Sauvegarder)
        self.Bind(wx.EVT_TEXT, self.onFilter, self.text_ctrl_FiltreRecherche)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onAjoutProduit, self.liste_produits)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onModifProduit, self.liste_lignes_commande)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy, self)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: NouvelleCommande.__set_properties
        self.label_titre_commande.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_fournisseur_produits_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_commande_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.text_ctrl_FiltreRecherche.SetMinSize((200, -1))
        # end wxGlade

    def __set_values(self):
        if self.commande.fournisseur:
            self.setFournisseur(self.commande.fournisseur)
            self.liste_lignes_commande.SetObjects([lc for lc in self.commande.lignes_commande])
            self.label_total_valeur.SetLabel(u"%.2f €" % self.commande.total_commande_TTC())

    def __do_layout(self):
        # begin wxGlade: NouvelleCommande.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entete = wx.BoxSizer(wx.HORIZONTAL)
        sizer_commande = wx.StaticBoxSizer(self.sizer_commande_staticbox, wx.VERTICAL)
        sizer_fournisseur_produits = wx.StaticBoxSizer(self.sizer_fournisseur_produits_staticbox, wx.HORIZONTAL)
        sizer_ligne_total = wx.BoxSizer(wx.HORIZONTAL)
        sizer_liste_produits = wx.BoxSizer(wx.VERTICAL)
        sizer_fitre_recherche = wx.BoxSizer(wx.HORIZONTAL)

        sizer_entete.Add(self.label_titre_commande, 1, wx.EXPAND, 0)
        sizer_entete.Add(self.button_infos_fournisseur, 0, wx.EXPAND, 0)
        sizer.Add(sizer_entete, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        sizer_fitre_recherche.Add(self.label_FiltreRecherche, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_fitre_recherche.Add(self.text_ctrl_FiltreRecherche, 0, 0, 0)
        sizer_liste_produits.Add(sizer_fitre_recherche, 0, wx.BOTTOM|wx.EXPAND, 6)
        sizer_liste_produits.Add(self.liste_produits, 1, wx.EXPAND, 0)
        sizer_fournisseur_produits.Add(sizer_liste_produits, 1, wx.EXPAND, 0)
        sizer.Add(sizer_fournisseur_produits, 1, wx.TOP|wx.EXPAND, 10)

        sizer_ligne_total.Add(self.label_total, 0, wx.EXPAND|wx.RIGHT, 20)
        sizer_ligne_total.Add(self.label_total_valeur, 0, wx.ALIGN_RIGHT, 0)

        sizer_commande.Add(sizer_ligne_total, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 6)
        sizer_commande.Add(self.liste_lignes_commande, 1, wx.EXPAND, 0)
        sizer.Add(sizer_commande, 1, wx.EXPAND, 0)

        sizer_boutons.Add(self.button_Sauvegarder, 0, 0, 0)
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 6)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __update_total(self):
        total = 0

        for ligne in self.liste_lignes_commande.GetObjects():
            total += ligne.prix_total_commande_ttc

        self.label_total_valeur.SetLabel(u"%.2f €" % total)
        self.Layout()

    def setFournisseur(self, fournisseur):
        self.commande.fournisseur = fournisseur

        self.label_titre_commande.SetLabel("Commande pour " + self.commande.fournisseur.nom)

        try:
            produits = Produit.select().where((Produit.fournisseur == fournisseur) &
                                              (Produit.retrait == False))
            self.liste_produits.SetObjects([p for p in produits])
            self.liste_produits.AutoSizeColumns()

        except BaseException as ex:
            print ex

        self.Layout()

    def onFilter(self, event):
        filtre_texte = Filter.TextSearch(self.liste_produits, text=self.text_ctrl_FiltreRecherche.GetValue())
        self.liste_produits.SetFilter(filtre_texte)
        self.liste_produits.RepopulateList()

    def onInfosFournisseur(self, event):  # wxGlade: NouvelleCommande.<event_handler>
        message = ""
        message += self.commande.fournisseur.nom + "\n\n"
        message += self.commande.fournisseur.adresse +"\n"
        message += self.commande.fournisseur.code_postal + " " + \
                   self.commande.fournisseur.ville + "\n\n"
        message += u"Tel fixe : " + self.commande.fournisseur.telephone_fixe + "\n"
        message += u"Tel portable : " + self.commande.fournisseur.telephone_portable + "\n"
        message += u"Email : " + self.commande.fournisseur.email + "\n\n"
        message += u"Nom du contact : " + self.commande.fournisseur.nom_contact + "\n\n"
        message += "Remarques : \n\n"

        message += fill(self.commande.fournisseur.remarques, 50)

        dlg = GMD.GenericMessageDialog(self, message, self.commande.fournisseur.nom,
                                       wx.OK|wx.ICON_INFORMATION)

        dlg.Fit()
        dlg.ShowModal()
        dlg.Destroy()

    def onAjoutProduit(self, event):
        deja_ajoute = False
        produit_selectionne = self.liste_produits.GetSelectedObject()

        for lc_liste in self.liste_lignes_commande.GetObjects():
            if lc_liste.produit.get_id() == produit_selectionne.get_id():
                deja_ajoute = True
                break

        if deja_ajoute == False:
            if produit_selectionne.vrac:
                label_type_conditionnement = ""
                label_u = produit_selectionne.conditionnement_format(majuscule=False)
            else:
                label_type_conditionnement = produit_selectionne.conditionnement_format()
                label_u = u"unité(s)"

            dlg = ChoixQuantite(label_type_conditionnement, label_u, validator=GenericTextValidator(flag=VALIDATE_INT))

            if dlg.ShowModal() == wx.ID_OK:
                if dlg.GetValue() != 0:
                    #lc = self.commande.ajout_ligne_commande(produit_selectionne, dlg.GetValue())
                    lc = LigneCommande.create(commande=self.commande, produit=produit_selectionne, quantite_commandee=dlg.GetValue())
                    self.liste_lignes_commande.AddObject(lc)
                    self.liste_lignes_commande.AutoSizeColumns()

                    #Mise à jour du total de la commande
                    self.__update_total()

            dlg.Destroy()

    def onModifProduit(self, event):
        lc_selectionne = self.liste_lignes_commande.GetSelectedObject()

        if lc_selectionne.produit.vrac:
            label_type_conditionnement = ""
            label_u = lc_selectionne.produit.conditionnement_format(majuscule=False)
            quantite_commandee = lc_selectionne.quantite_commandee /1000
        else:
            label_type_conditionnement = lc_selectionne.produit.conditionnement_format()
            label_u = u"unité(s)"
            quantite_commandee = lc_selectionne.quantite_commandee

        dlg = ChoixQuantite(label_type_conditionnement, label_u, quantite=quantite_commandee, validator=GenericTextValidator(flag=VALIDATE_INT))

        id_resultat = dlg.ShowModal()

        if id_resultat == wx.ID_OK and dlg.GetValue() != 0:
            lc_selectionne.quantite_commandee = dlg.GetValue()
            lc_selectionne.save()
            self.liste_lignes_commande.RefreshObject(lc_selectionne)
            self.liste_lignes_commande.AutoSizeColumns()
        elif id_resultat == wx.ID_DELETE or dlg.GetValue() == 0:
            self.liste_lignes_commande.RemoveObject(lc_selectionne)
            self.liste_lignes_commande.RefreshObject(lc_selectionne)
            lc_selectionne.delete_instance()
            self.liste_lignes_commande.AutoSizeColumns()

        #Mise à jour du total de la commande
        self.__update_total()

        dlg.Destroy()

    def onSauvegarder(self, event):
        try:
            DATABASE.commit()
            wx.MessageBox(u"La commande a été enregistrée", "Notification")
        except BaseException as ex:
            wx.MessageBox(u"Problème lors de l'enregistrement : %s" % ex, "Erreur")

    def onDestroy(self, event):
        if self.commande.fournisseur != None:
            dlg = wx.MessageDialog(parent=None, message=u"Voulez vous sauvegarder la commande ?",
                                   caption=u"Sauvegarde de la commande", style=wx.YES_NO|wx.ICON_QUESTION)

            if dlg.ShowModal() == wx.ID_YES:
                DATABASE.commit()
            else:
                DATABASE.rollback()

            dlg.Destroy()

        event.Skip()
