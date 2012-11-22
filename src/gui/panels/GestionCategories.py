#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Categorie
from lib.objectlistview import ObjectListView, ColumnDefn
from gui.panels.FicheCategorie import FicheCategorie

###########################################################################
## Class GestionCategories
###########################################################################


class GestionCategories(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GestionCategories.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.sizer_navigation_staticbox = wx.StaticBox(self, -1,
                                                       u"Gestion des catégories")
        self.button_ajout_categorie = wx.Button(self, -1,
                                                u"Ajouter une nouvelle catégorie")
        self.liste_categories = ObjectListView(self, -1,
                                               style=wx.LC_REPORT |
                                                     wx.SUNKEN_BORDER |
                                                     wx.LC_SINGLE_SEL)

        self.liste_categories.SetColumns([
            ColumnDefn("ID", "right", valueGetter="get_id", fixedWidth=70),
            ColumnDefn("Nom", "left", -1, "nom"),
            ColumnDefn("Nombre de produits", "left", 100,
                       "nombre_produits",
                       stringConverter="%s produit(s)",
                       isSpaceFilling=True)
        ])

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutCategorie,
                  self.button_ajout_categorie)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnModifCategorie,
                  self.liste_categories)
        # end wxGlade

    def __set_properties(self):
        self.sizer_navigation_staticbox.SetFont(wx.Font(14,
                                                        wx.DEFAULT,
                                                        wx.NORMAL,
                                                        wx.BOLD,
                                                        0, ""))

    def __do_layout(self):
        # begin wxGlade: GestionCategories.__do_layout
        sizer_entete = wx.StaticBoxSizer(self.sizer_navigation_staticbox,
                                         wx.HORIZONTAL)
        sizer_entete.Add((1, 1), 1)
        sizer_entete.Add(self.button_ajout_categorie, 0,
                         wx.BOTTOM |
                         wx.TOP |
                         wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_entete, 0,
                  wx.BOTTOM |
                  wx.ALIGN_RIGHT |
                  wx.EXPAND, 10)
        sizer.Add(self.liste_categories, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste(self):
        try:
            self.liste_categories.SetObjects([c for c in Categorie.select()])
        except BaseException as ex:
            print ex

    def OnAjoutCategorie(self, event):
        dialog_categorie = wx.Dialog(self, title=u"Nouvelle catégorie")
        fiche_categorie = FicheCategorie(dialog_categorie)
        dialog_categorie.Fit()
        dialog_categorie.ShowModal()
        dialog_categorie.Destroy()

        if dialog_categorie.GetReturnCode() == wx.ID_OK:
            self.liste_categories.AddObject(fiche_categorie.categorie)
            self.liste_categories.AutoSizeColumns()

    def OnModifCategorie(self, event):
        categorie = self.liste_categories.GetSelectedObject()

        dialog_categorie = wx.Dialog(self,
                                     title=u"Catégorie : " + categorie.nom)
        FicheCategorie(dialog_categorie, categorie)
        dialog_categorie.Fit()
        dialog_categorie.ShowModal()
        dialog_categorie.Destroy()

        if dialog_categorie.GetReturnCode() == wx.ID_OK:
            self.liste_categories.RefreshObject(
                                  self.liste_categories.GetSelectedObject())
            self.liste_categories.AutoSizeColumns()
