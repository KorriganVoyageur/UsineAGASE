#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import wx.lib.agw.genericmessagedialog as GMD

from lib.objectlistview import ObjectListView, ColumnDefn, Filter
from textwrap import fill

from classes.Validators import GenericTextValidator, VALIDATE_INT

from model.model import Achat, LigneAchat, Produit, Adherent, DATABASE
from datetime import datetime

###########################################################################
## Class FicheAchat
###########################################################################


class FicheAchat(wx.Panel):
    def __init__(self, parent, achat=None, adherent=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if achat == None:
            if adherent == None:
                #TODO : à modifier quand le système d'identification sera en place
                adherent = Adherent.select().where(Adherent.id == 1).get()
        
            achat = Achat.create(adherent=adherent)

        self.achat = achat

        self.sizer_achat_staticbox = wx.StaticBox(self, -1, "Achat")
        self.sizer_fournisseur_produits_staticbox = wx.StaticBox(self, -1, "Liste des produits")
        self.label_titre_achat = wx.StaticText(self, -1, "Achat pour ")
        self.search_nom = wx.SearchCtrl(self, -1, "")
        self.liste_produits = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.label_total = wx.StaticText(self, -1, "Total des achats :")
        self.label_total_valeur = wx.StaticText(self, -1, u"0.00 €", style=wx.ALIGN_RIGHT)
        self.liste_lignes_achat = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.bouton_sauvegarder = wx.Button(self, -1, "Enregistrer l'achat")

        self.liste_produits.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "ref_GASE", minimumWidth=70),
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn("Prix", "right", -1, "prix_vente_format", minimumWidth=100, isSpaceFilling=True)
        ])
        self.liste_produits.SetEmptyListMsg("Aucun produits")
        self.liste_produits.AutoSizeColumns()

        self.liste_lignes_achat.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "produit.ref_GASE", minimumWidth=70),
            ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=100),
            ColumnDefn("Prix", "left", -1, "produit.prix_vente_format", minimumWidth=100),
            ColumnDefn(u"Quantité", "left", -1, "quantite_format", minimumWidth=70),
            ColumnDefn("Total TTC", "right", -1, "prix_total", stringConverter=u"%.2f €", minimumWidth=70, isSpaceFilling=True)
        ])
        self.liste_lignes_achat.AutoSizeColumns()

        self.liste_lignes_achat.SetEmptyListMsg(u"Produits achetés")

        self.__set_properties()
        self.__set_values()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnSauvegarder, self.bouton_sauvegarder)
        self.Bind(wx.EVT_TEXT, self.OnFilter, self.search_nom)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnAjoutProduit, self.liste_produits)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnModifProduit, self.liste_lignes_achat)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)

    def __set_properties(self):
        self.label_titre_achat.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_fournisseur_produits_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_achat_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.search_nom.SetMinSize((200, -1))        
        self.search_nom.SetDescriptiveText("Recherche sur le nom")

    def __set_values(self):
        try:
            produits = Produit.select().where((Produit.retrait == False) |
                                              (Produit.retrait == True and Produit.stock > 0))
            self.liste_produits.SetObjects([p for p in produits])
            self.liste_produits.AutoSizeColumns()
            
            self.liste_lignes_achat.SetObjects([la for la in self.achat.lignes_achat])
            self.label_total_valeur.SetLabel(u"%.2f €" % self.achat.total)

        except BaseException as ex:
            print ex


    def __do_layout(self):
        # begin wxGlade: NouvelleAchat.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_achat = wx.StaticBoxSizer(self.sizer_achat_staticbox, wx.VERTICAL)
        sizer_fournisseur_produits = wx.StaticBoxSizer(self.sizer_fournisseur_produits_staticbox, wx.HORIZONTAL)
        sizer_ligne_total = wx.BoxSizer(wx.HORIZONTAL)
        sizer_liste_produits = wx.BoxSizer(wx.VERTICAL)

        """sizer_entete = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entete.Add(self.label_titre_achat, 1, wx.EXPAND, 0)
        sizer_entete.Add(self.bouton_infos_fournisseur, 0, wx.EXPAND, 0)
        sizer.Add(sizer_entete, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)"""
        
        sizer.Add(self.label_titre_achat, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        sizer_liste_produits.Add(self.search_nom, 0, wx.BOTTOM, 6)
        sizer_liste_produits.Add(self.liste_produits, 1, wx.EXPAND, 0)
        sizer_fournisseur_produits.Add(sizer_liste_produits, 1, wx.EXPAND, 0)
        sizer.Add(sizer_fournisseur_produits, 1, wx.TOP|wx.EXPAND, 10)

        sizer_ligne_total.Add(self.label_total, 0, wx.EXPAND|wx.RIGHT, 20)
        sizer_ligne_total.Add(self.label_total_valeur, 0, wx.ALIGN_RIGHT, 0)

        sizer_achat.Add(sizer_ligne_total, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 6)
        sizer_achat.Add(self.liste_lignes_achat, 1, wx.EXPAND, 0)
        sizer.Add(sizer_achat, 1, wx.EXPAND, 0)

        sizer_boutons.Add(self.bouton_sauvegarder, 0, 0, 0)
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 6)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __update_total(self):
        self.label_total_valeur.SetLabel(u"%.2f €" % self.achat.total)
        self.Layout()

    def SetFournisseur(self, fournisseur):
        self.achat.fournisseur = fournisseur

        self.label_titre_achat.SetLabel("Achat pour " + self.achat.fournisseur.nom)

        try:
            produits = Produit.select().where((Produit.fournisseur == fournisseur) &
                                              (Produit.retrait == False))
            self.liste_produits.SetObjects([p for p in produits])
            self.liste_produits.AutoSizeColumns()

        except BaseException as ex:
            print ex

        self.Layout()

    def OnFilter(self, event):
        filtre_texte = Filter.TextSearch(self.liste_produits, text=self.search_nom.GetValue())
        self.liste_produits.SetFilter(filtre_texte)
        self.liste_produits.RepopulateList()

    def OnAjoutProduit(self, event):
        deja_ajoute = False
        produit_selectionne = self.liste_produits.GetSelectedObject()

        for la_liste in self.liste_lignes_achat.GetObjects():
            if la_liste.produit.get_id() == produit_selectionne.get_id():
                deja_ajoute = True
                break

        if deja_ajoute == False:
            la = LigneAchat(achat=self.achat, produit=produit_selectionne)
            
            dlg = DialogChoixQuantite(la)

            if dlg.ShowModal() == wx.ID_OK:
                if dlg.GetQuantite() != 0:
                    la.quantite = dlg.GetQuantite()
                    la.save()
                    self.liste_lignes_achat.AddObject(la)
                    self.liste_lignes_achat.AutoSizeColumns()

                    #Mise à jour du total de l'achat
                    self.__update_total()

            dlg.Destroy()

    def OnModifProduit(self, event):
        la_selectionnee = self.liste_lignes_achat.GetSelectedObject()

        dlg = DialogChoixQuantite(la_selectionnee)

        id_resultat = dlg.ShowModal()

        if id_resultat == wx.ID_OK and dlg.GetQuantite() != 0:
            la_selectionnee.quantite = dlg.GetQuantite()
            la_selectionnee.save()
            self.liste_lignes_achat.RefreshObject(la_selectionnee)
            self.liste_lignes_achat.AutoSizeColumns()
        elif id_resultat == wx.ID_DELETE or dlg.GetQuantite() == 0:
            self.liste_lignes_achat.RemoveObject(la_selectionnee)
            self.liste_lignes_achat.RefreshObject(la_selectionnee)
            la_selectionnee.delete_instance()
            self.liste_lignes_achat.AutoSizeColumns()

        #Mise à jour du total de la achat
        self.__update_total()

        dlg.Destroy()

    def OnSauvegarder(self, event):
        try:
            self.achat.date = datetime.today()
            self.achat.save()
            DATABASE.commit()
            wx.MessageBox(u"L'achat a été enregistré", "Notification")
        except BaseException as ex:
            wx.MessageBox(u"Problème lors de l'enregistrement : %s" % ex, "Erreur")

    def OnDestroy(self, event):
        dlg = wx.MessageDialog(parent=None, message=u"Voulez vous sauvegarder cet achat ?",
                               caption=u"Sauvegarde de l'achat", style=wx.YES_NO|wx.ICON_QUESTION)
    
        if dlg.ShowModal() == wx.ID_YES:
            self.achat.date = datetime.today()
            self.achat.save()
            DATABASE.commit()
        else:
            DATABASE.rollback()
    
        dlg.Destroy()

        event.Skip()


###########################################################################
## Class DialogChoixQuantite
###########################################################################


class DialogChoixQuantite(wx.Dialog):
    def __init__(self, ligne_achat):
        wx.Dialog.__init__(self, None, -1, u"Quantité", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.ligne_achat = ligne_achat

        self.label_quantite = wx.StaticText(self, -1, u"Quantité :")
        self.text_quantite = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER, validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_unite = wx.StaticText(self, -1, "Label unite")
        self.bouton_ok = wx.Button(self, wx.ID_OK, "")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "")

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnregistrer, self.text_quantite)

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        self.text_quantite.SetMinSize((80, -1))
        self.text_quantite.SetFocus()
        
    def __set_valeurs(self):
        if self.ligne_achat.produit.vrac:
            self.label_unite.SetLabel(self.ligne_achat.produit.unite_vente)
        else:
            self.label_unite.SetLabel(self.ligne_achat.produit.unite_vente +"(s)")
            
        self.text_quantite.SetValue(str(self.ligne_achat.quantite))
            
        if self.ligne_achat.quantite > 0:
            self.bouton_annuler.SetLabel("Supprimer")
            self.bouton_annuler.SetId(wx.ID_DELETE)
            self.bouton_annuler.Bind(wx.EVT_BUTTON, self.OnSupprimer)

    def __do_layout(self):
        sizer_choix = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choix.Add(self.label_quantite, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_choix.Add(self.text_quantite, 0, wx.LEFT|wx.RIGHT, 6)
        sizer_choix.Add(self.label_unite, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_choix, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer_boutons, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def GetQuantite(self):
        return int(self.text_quantite.GetValue())

    def OnEnregistrer(self, event):
        if self.Validate():
            self.EndModal(wx.ID_OK)

    def OnSupprimer(self, event):
        self.EndModal(wx.ID_DELETE)
