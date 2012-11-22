#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import os, subprocess, sys
from lib import desktop

from lib.objectlistview import ObjectListView, ColumnDefn
from datetime import datetime

from classes.Validators import GenericTextValidator, VALIDATE_INT

from model.model import Commande, DATABASE

from gui.dialogs.ChoixQuantite import ChoixQuantite
from gui.dialogs.EnvoiEmailCommande import EnvoiEmailCommande

from gui.panels.FicheCommande import FicheCommande
from gui.dialogs.NouvelleCommande import NouvelleCommande
#from dialogs.PreviewPDF import PreviewPDF

###########################################################################
## Class GestionCommandes
###########################################################################


class GestionCommandes(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SuiviCommandes.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        #self.sizer_navigation_staticbox = wx.StaticBox(self, -1, u"Suivi des commandes")

        self.commande = None

        self.sizer_navigation_staticbox = wx.StaticBox(self, -1, "Gestion des commandes")
        #self.sizer_liste_commandes_staticbox = wx.StaticBox(self, -1, "Liste des commandes")
        self.sizer_commande_staticbox = wx.StaticBox(self, -1, u"Détails de la Commande")
        self.button_Modifier = wx.Button(self, -1, "Modifier")
        self.button_nouvelle_commande = wx.Button(self, -1, "Faire une nouvelle commande")
        self.button_Supprimer = wx.Button(self, -1, "Supprimer")
        self.button_Imprimer = wx.Button(self, -1, "Imprimer le bon de commande")
        self.button_PDF = wx.Button(self, -1, u"Générer le bon de commande")
        self.button_Email = wx.Button(self, -1, u"Envoyer le bon de commande")
        self.button_Commandee = wx.Button(self, -1, u"Commandée")
        self.button_Livree = wx.Button(self, -1, u"Livrée")
        self.button_Verifiee = wx.Button(self, -1, u"Vérifiée")
        self.label_nom_fournisseur = wx.StaticText(self, -1, "Fournisseur :")
        self.label_montant_commande = wx.StaticText(self, -1, "Montant :")
        self.label_nom_fournisseur_valeur = wx.StaticText(self, -1, "")
        self.label_montant_commande_valeur = wx.StaticText(self, -1, "")
        self.label_date_commande = wx.StaticText(self, -1, "Date de commande :")
        self.label_date_livraison = wx.StaticText(self, -1, u"Date de réception :")
        self.label_date_commande_valeur = wx.StaticText(self, -1, "")
        self.label_date_livraison_valeur = wx.StaticText(self, -1, "")

        #self.label_suivi_commandes = wx.StaticText(self, -1, u"Suivi des commandes")

        #self.label_suivi_commandes_description = wx.StaticText(self, -1, u"C'est là qu'on gère les commandes")

        self.liste_commandes = ObjectListView(self, -1, style=wx.LC_REPORT|
                                              wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_commandes.SetColumns([
            ColumnDefn("Fournisseur", "left", -1, "fournisseur.nom", minimumWidth=100),
            ColumnDefn("Date commande", "left", -1, "date_commande", stringConverter=u"%d/%m/%y", minimumWidth=130),
            ColumnDefn("Total TTC", "left", -1, "total_TTC", stringConverter=u"%.2f €", minimumWidth=100),
            ColumnDefn("statut", "left", -1, "statut_nom", isSpaceFilling=True, minimumWidth=100)
        ])

        def rowFormatterLC(listItem, commande):
            if commande.statut == 0:
                #C5CBFF
                listItem.SetBackgroundColour("#D8DDFF")
            elif commande.statut == 1:
                #FFA3A2
                listItem.SetBackgroundColour("#FFD3D3")
            elif commande.statut == 2:
                #E8E9A0
                listItem.SetBackgroundColour("#FBFCC8")
            elif commande.statut == 3:
                #B7D69E
                listItem.SetBackgroundColour("#E3FFCB")

        self.liste_commandes.rowFormatter = rowFormatterLC
        self.liste_commandes.AutoSizeColumns()
        self.liste_commandes.SortBy(1, False)

        self.liste_commandes.SetEmptyListMsg("Il n'y a aucune commande")

        self.liste_lignes_commande = ObjectListView(self, -1,
                                                    style=wx.LC_REPORT|wx.SUNKEN_BORDER|
                                                    wx.LC_SINGLE_SEL)

        self.__set_lignes_commandes_colonnes()

        self.liste_lignes_commande.SetEmptyListMsg("La commande ne contient aucun produit")

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()
        self.__affichage_boutons(-1, 0)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelectionCommande, self.liste_commandes)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onVerifLigne, self.liste_lignes_commande)
        self.Bind(wx.EVT_BUTTON, self.onNouvelleCommande, self.button_nouvelle_commande)
        self.Bind(wx.EVT_BUTTON, self.onModifier, self.button_Modifier)
        self.Bind(wx.EVT_BUTTON, self.onSupprimer, self.button_Supprimer)
        self.Bind(wx.EVT_BUTTON, self.onImprimer, self.button_Imprimer)
        self.Bind(wx.EVT_BUTTON, self.onPDF, self.button_PDF)
        self.Bind(wx.EVT_BUTTON, self.onEmail, self.button_Email)
        self.Bind(wx.EVT_BUTTON, self.onCommandee, self.button_Commandee)
        self.Bind(wx.EVT_BUTTON, self.onLivree, self.button_Livree)
        self.Bind(wx.EVT_BUTTON, self.onVerifiee, self.button_Verifiee)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SuiviCommandes.__set_properties
        self.sizer_navigation_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_nom_fournisseur.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        #self.label_suivi_commandes.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_montant_commande.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_date_commande.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_date_livraison.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_nom_fournisseur_valeur.SetMinSize((200, -1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SuiviCommandes.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_titre = wx.StaticBoxSizer(self.sizer_navigation_staticbox, wx.VERTICAL)

        sizer_haut = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons = wx.BoxSizer(wx.VERTICAL)
        #wx.StaticBoxSizer(self.sizer_liste_commandes_staticbox,wx.VERTICAL)

        sizer_bas = wx.StaticBoxSizer(self.sizer_commande_staticbox, wx.VERTICAL)

        sizer_infos_commande = wx.BoxSizer(wx.HORIZONTAL)

        sizer_col4 = wx.BoxSizer(wx.VERTICAL)
        sizer_col3 = wx.BoxSizer(wx.VERTICAL)
        sizer_col2 = wx.BoxSizer(wx.VERTICAL)
        sizer_col1 = wx.BoxSizer(wx.VERTICAL)

        #sizer.Add(self.label_suivi_commandes, 0, wx.EXPAND, 0)
        #sizer_titre.Add(self.label_suivi_commandes_description, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer_titre.Add(self.button_nouvelle_commande, 0, wx.TOP|wx.BOTTOM, 5)
        sizer.Add(sizer_titre, 0, wx.EXPAND, 0)

        #sizer haut
        sizer_boutons.Add(self.button_Modifier, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_Supprimer, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_Imprimer, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_PDF, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_Email, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_Commandee, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_Livree, 0, wx.BOTTOM|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_Verifiee, 0, wx.EXPAND, 0)
        sizer_boutons.Add(sizer_boutons.GetMinSize(), 0, wx.EXPAND, 0)

        sizer_haut.Add(sizer_boutons, 0, wx.RIGHT|wx.EXPAND, 10)

        sizer_haut.Add(self.liste_commandes, 1, wx.TOP|wx.EXPAND, 0)

        sizer.Add(sizer_haut, 1, wx.TOP|wx.EXPAND, 5)

        #sizer infos
        sizer_col1.Add(self.label_nom_fournisseur, 0, 0, 0)
        sizer_col1.Add((20, 10), 0, 0, 0)
        sizer_col1.Add(self.label_montant_commande, 0, 0, 0)
        sizer_infos_commande.Add(sizer_col1, 0, wx.RIGHT|wx.EXPAND, 10)
        sizer_col2.Add(self.label_nom_fournisseur_valeur, 0, 0, 0)
        sizer_col2.Add((20, 10), 0, 0, 0)
        sizer_col2.Add(self.label_montant_commande_valeur, 0, 0, 0)
        sizer_infos_commande.Add(sizer_col2, 0, wx.RIGHT|wx.EXPAND, 20)
        sizer_col3.Add(self.label_date_commande, 0, 0, 0)
        sizer_col3.Add((20, 10), 0, 0, 0)
        sizer_col3.Add(self.label_date_livraison, 0, 0, 0)
        sizer_infos_commande.Add(sizer_col3, 0, wx.RIGHT|wx.EXPAND, 10)
        sizer_col4.Add(self.label_date_commande_valeur, 0, 0, 0)
        sizer_col4.Add((20, 10), 0, 0, 0)
        sizer_col4.Add(self.label_date_livraison_valeur, 0, 0, 0)
        sizer_infos_commande.Add(sizer_col4, 0, wx.EXPAND, 0)

        sizer_bas.Add(sizer_infos_commande, 0, wx.TOP|wx.EXPAND, 5)

        sizer.Add(sizer_bas, 0, wx.TOP|wx.EXPAND, 5)

        sizer.Add(self.liste_lignes_commande, 1, wx.TOP|wx.EXPAND, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste(self):
        try:
            commandes = Commande.select()

            self.liste_commandes.SetObjects([c for c in commandes])
            self.liste_commandes.AutoSizeColumns()

        except BaseException as ex:
            print ex

    def __affichage_boutons(self, statut, n_lignes):
        if statut == 0:
            self.button_Modifier.Enable()
            self.button_Supprimer.Enable()
            if n_lignes>0:
                self.button_Imprimer.Enable()
                self.button_PDF.Enable()
                self.button_Email.Enable()
                self.button_Commandee.Show()
            else:
                self.button_Imprimer.Disable()
                self.button_PDF.Disable()
                self.button_Email.Disable()
                self.button_Commandee.Hide()

            self.button_Livree.Hide()
            self.button_Verifiee.Hide()
        elif statut == 1:
            self.button_Modifier.Enable()
            self.button_Supprimer.Disable()
            self.button_Imprimer.Enable()
            self.button_PDF.Enable()
            self.button_Email.Enable()
            self.button_Commandee.Hide()
            self.button_Livree.Show()
            self.button_Verifiee.Hide()
        elif statut == 2:
            self.button_Modifier.Disable()
            self.button_Supprimer.Disable()
            self.button_Imprimer.Enable()
            self.button_PDF.Enable()
            self.button_Email.Disable()
            self.button_Commandee.Hide()
            self.button_Livree.Hide()
            self.button_Verifiee.Show()
        elif statut == 3:
            self.button_Modifier.Disable()
            self.button_Supprimer.Disable()
            self.button_Imprimer.Enable()
            self.button_PDF.Enable()
            self.button_Email.Disable()
            self.button_Commandee.Hide()
            self.button_Livree.Hide()
            self.button_Verifiee.Hide()
        else:
            self.button_Modifier.Disable()
            self.button_Supprimer.Disable()
            self.button_Imprimer.Disable()
            self.button_PDF.Disable()
            self.button_Email.Disable()
            self.button_Commandee.Hide()
            self.button_Livree.Hide()
            self.button_Verifiee.Hide()

        self.Layout()

    def __set_lignes_commandes_colonnes(self):
        if self.commande:
            if self.commande.statut >= 2:

                def rowFormatter(listItem, lc):
                    if lc.is_verifiee:
                        if lc.quantite_livree != lc.quantite_commandee:
                            listItem.SetBackgroundColour("#FFD3D3")
                        else:
                            listItem.SetBackgroundColour("#E3FFCB")

                self.liste_lignes_commande.rowFormatter = rowFormatter

                self.liste_lignes_commande.SetColumns([
                    ColumnDefn("Ref Fournisseur", "left", -1, "produit.ref_fournisseur", minimumWidth=120),
                    ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=200),
                    ColumnDefn(u"Quantité commandée", "left", -1, "quantite_commandee_conditionnement", minimumWidth=200),
                    ColumnDefn(u"Quantité livrée", "left", -1, "quantite_livree_conditionnement", minimumWidth=200, isSpaceFilling=True),
                    ])
                self.liste_lignes_commande.AutoSizeColumns()
            else:
                self.liste_lignes_commande.SetColumns([
                    ColumnDefn("Ref Fournisseur", "left", -1, "produit.ref_fournisseur", minimumWidth=120),
                    ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=200),
                    ColumnDefn(u"Quantité commandée", "left", -1, "quantite_commandee_conditionnement", minimumWidth=150),
                    ColumnDefn("Total TTC", "right", -1, "prix_total_commande_ttc", stringConverter=u"%s €", isSpaceFilling=True, minimumWidth=100)
                    ])
                self.liste_lignes_commande.AutoSizeColumns()

    def onSelectionCommande(self, event):
        self.commande = self.liste_commandes.GetSelectedObject()

        if self.commande:
            self.liste_lignes_commande.SetObjects([lc for lc in self.commande.lignes_commande])
            self.__set_lignes_commandes_colonnes()
            self.label_nom_fournisseur_valeur.SetLabel(self.commande.fournisseur.nom)

            if self.commande.statut > 1:
                self.label_montant_commande_valeur.SetLabel(u"%.2f €" % self.commande.total_livraison_TTC())
            else:
                self.label_montant_commande_valeur.SetLabel(u"%.2f €" % self.commande.total_commande_TTC())

            self.label_date_commande_valeur.SetLabel(self.commande.date_commande_format())
            self.label_date_livraison_valeur.SetLabel(self.commande.date_livraison_format())
            self.__affichage_boutons(self.commande.statut, self.commande.lignes_commande.count())

            if self.commande.fournisseur.email == "":
                self.button_Email.Disable()

        else:
            self.liste_lignes_commande.SetObjects(None)
            self.label_nom_fournisseur_valeur.SetLabel("")
            self.label_montant_commande_valeur.SetLabel("")
            self.label_date_commande_valeur.SetLabel("")
            self.label_date_livraison_valeur.SetLabel("")
            self.__affichage_boutons(-1, 0)

    def onVerifLigne(self, event):
        if self.commande.statut == 2:
            lc_selectionne = self.liste_lignes_commande.GetSelectedObject()

            if lc_selectionne.produit.vrac:
                label_u = lc_selectionne.produit.conditionnement_format(majuscule=False)
                quantite = lc_selectionne.quantite_livree / lc_selectionne.produit.poids_volume
            else:
                label_u = u"unité(s)"
                quantite = lc_selectionne.quantite_livree

            dlg = ChoixQuantite("", label_u, quantite=quantite, validator=GenericTextValidator(flag=VALIDATE_INT))

            id_resultat = dlg.ShowModal()

            if id_resultat == wx.ID_OK:
                lc_selectionne.is_verifiee = True
                lc_selectionne.quantite_livree = dlg.GetValue()
                self.liste_lignes_commande.RefreshObject(lc_selectionne)

            elif id_resultat == wx.ID_DELETE:
                lc_selectionne.is_verifiee = True
                lc_selectionne.quantite_livree = 0
                self.liste_lignes_commande.RefreshObject(lc_selectionne)

            dlg.Destroy()

    def onNouvelleCommande(self, event):
        nouvelle_commande = NouvelleCommande(self.GetTopLevelParent())
        nouvelle_commande.ShowModal()

    def onModifier(self, event):
        if self.commande:
            if self.commande.statut < 2:
                ecranprincipal = self.GetTopLevelParent()
                ecranprincipal.SetPanelPrincipal(FicheCommande, session_close=False, commande=self.commande)

    def onSupprimer(self, event):
        if self.commande:
            if self.commande.statut == 0:
                dlg = wx.MessageDialog(parent=None, message=u"Voulez vous vraiment supprimer la commande ?",
                                       caption=u"Suppression de la commande", style=wx.OK|wx.CANCEL|wx.ICON_QUESTION)

                if dlg.ShowModal() == wx.ID_OK:
                    self.liste_commandes.RemoveObject(self.commande)
                    self.liste_lignes_commande.SetObjects(None)

                    self.commande.delete_instance(recursive=True)

                    self.commande = None

                    self.onSelectionCommande(None)

                    DATABASE.commit()

    def onPDF(self, event):
        if self.commande:

            if not self.commande.date_commande:
                nom_fichier = self.commande.fournisseur.nom + " - Bon de commande du " + datetime.today().strftime("%d-%m-%Y") + ".pdf"
            else:
                nom_fichier = self.commande.fournisseur.nom + " - Bon de commande du " + self.commande.date_commande_format() + ".pdf"

            dlg = wx.FileDialog(
                self, message="Sauvegarde du bon de commande ...",
                defaultDir="",
                defaultFile=nom_fichier, wildcard="PDF (*.pdf)|*.pdf", style=wx.SAVE
                )

            if dlg.ShowModal() == wx.ID_OK:
                chemin = dlg.GetPath()
                self.commande.genere_PDF(chemin)

            dlg.Destroy()

    def onEmail(self, event):
        if self.commande:
            if self.commande.statut < 2:
                envoi_email = EnvoiEmailCommande(self, self.commande)
                envoi_email.ShowModal()
                envoi_email.Destroy()

                if envoi_email.ShowModal() == wx.ID_OK:
                    self.commande.statut(1)
                    self.commande.save()
                    self.liste_commandes.RefreshObject(self.commande)
                    self.onSelectionCommande(None)

                    DATABASE.commit()

    def onImprimer(self, event):
        if self.commande:
            self.commande.genere_PDF(os.getcwd() + "/dernier_bon_imprime.pdf")

            '''if sys.platform.startswith('linux'):
			    subprocess.call(["xdg-open", os.getcwd() + "/dernier_bon_imprime.pdf"])
            else:
                os.startfile(file)'''

            desktop.open(os.getcwd() + "/dernier_bon_imprime.pdf")

            '''preview_pdf = PreviewPDF(os.getcwd() + "/dernier_bon_imprime.pdf")
            preview_pdf.ShowModal()
            preview_pdf.Destroy()'''

    def onCommandee(self, event):
        if self.commande:
            dlg = wx.MessageDialog(parent=None, message=u"La commande a bien été commandée ?",
                                   caption=u"Commande de la commande", style=wx.YES_NO|wx.ICON_QUESTION)

            if dlg.ShowModal() == wx.ID_YES:
                self.commande.statut = 1
                self.commande.save()
                self.liste_commandes.RefreshObject(self.commande)
                self.onSelectionCommande(None)
                DATABASE.commit()

            dlg.Destroy()

    def onLivree(self, event):
        #TODO : ajouter la possibilité de choisir la date de livraison
        #Ajouter également une vérification sur les prix
        if self.commande:
            dlg = wx.MessageDialog(parent=None, message=u"La commande a bien été livrée ?",
                                   caption=u"Livraison de la commande", style=wx.YES_NO|wx.ICON_QUESTION)

            if dlg.ShowModal() == wx.ID_YES:
                self.commande.statut = 2
                self.commande.save()
                self.liste_commandes.RefreshObject(self.commande)
                self.onSelectionCommande(None)
                DATABASE.commit()

            dlg.Destroy()

    def onVerifiee(self, event):
        if self.commande:
            commande_verifiee = True

            for lc in self.liste_lignes_commande.GetObjects():
                if not lc.is_verifiee:
                    commande_verifiee = False

            if commande_verifiee:
                dlg = wx.MessageDialog(parent=None, message=u"La livraison a bien été vérifiée ?",
                                      caption=u"Vérification de la livraison", style=wx.YES_NO|wx.ICON_QUESTION)

                if dlg.ShowModal() == wx.ID_YES:
                    for lc in self.liste_lignes_commande.GetObjects():
                        lc.save()
                        
                    self.commande.statut = 3
                    self.commande.save()

                    self.liste_commandes.RefreshObject(self.commande)
                    self.onSelectionCommande(None)

                    with DATABASE.transaction():
                        DATABASE.commit()

                dlg.Destroy()
            else:
                wx.MessageBox(u"La livraison n'a pas encoré été entièrement vérifiée", "Erreur", style=wx.ICON_ERROR)
