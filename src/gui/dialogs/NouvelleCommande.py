#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx

from model.model import Commande, Fournisseur
from gui.panels.FicheCommande import FicheCommande

###########################################################################
## Class NouvelleCommande
###########################################################################


class NouvelleCommande(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, -1, "Nouvelle commande")

        self.label_SelectionFournisseur = wx.StaticText(self, -1, u"Sélectionnez un fournisseur :")
        self.combo_box_SelectionFournisseur = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.button_SelectionFournisseur = wx.Button(self, -1, "Valider")

        self.__remplissage_liste_fournisseur()

        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onSelectFournisseur, self.button_SelectionFournisseur)

    def __do_layout(self):
        # begin wxGlade: NouvelleCommande.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer_selection_fournisseur = wx.BoxSizer(wx.HORIZONTAL)
        sizer_selection_fournisseur.Add(self.label_SelectionFournisseur, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_selection_fournisseur.Add(self.combo_box_SelectionFournisseur, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 8)
        sizer_selection_fournisseur.Add(self.button_SelectionFournisseur, 0, 0, 0)
        sizer.Add(sizer_selection_fournisseur, 0, wx.ALL|wx.EXPAND, 20)

        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste_fournisseur(self):
        try:
            fournisseurs = Fournisseur.select().order_by(Fournisseur.nom.asc())

            for fournisseur in fournisseurs:
                self.combo_box_SelectionFournisseur.Append(fournisseur.nom, fournisseur)

            self.combo_box_SelectionFournisseur.Select(0)

        except BaseException as ex:
            print ex

    def onSelectFournisseur(self, event):
        fournisseur = self.combo_box_SelectionFournisseur.GetClientData(self.combo_box_SelectionFournisseur.GetSelection())

        commande_existante = Commande.select().where((Commande._statut == 0) & (Commande.fournisseur == fournisseur))

        if commande_existante.exists():
            wx.MessageBox(u"Une commande pour %s" %fournisseur.nom + u" est déjà en cours de création.", u"Commande en création")
            self.commande = commande_existante.get()
        else:
            self.commande = Commande.create(fournisseur=fournisseur)

        ecranprincipal = self.GetParent()
        ecranprincipal.SetPanelPrincipal(FicheCommande, session_close=False, commande=self.commande)

        self.Destroy()
