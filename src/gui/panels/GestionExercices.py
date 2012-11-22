#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Exercice
from datetime import date

from lib.objectlistview import ObjectListView, ColumnDefn

from gui.panels.DetailsExercice import DetailsExercice
from gui.panels.FicheExercice import FicheExercice

###########################################################################
## Class GestionExercice
###########################################################################


class GestionExercices(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        description = u"Les exercices correspondent aux exercices comptables de l'association.\nIls permettent d'avoir un aperçu, sur une période définie, des mouvements de trésorerie."

        self.sizer_details_exercice_staticbox = wx.StaticBox(self, -1, u"Détails de l'exercice sélectionné")
        self.sizer_navigation_staticbox = wx.StaticBox(self, -1, "Gestion des exercices")
        self.label_description = wx.StaticText(self, -1, description)
        self.static_line_1 = wx.StaticLine(self, -1)
        self.bouton_ajout_exercice = wx.Button(self, -1, "Ajouter un nouvel exercice")
        self.liste_exercices = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)
        self.details_exercice = DetailsExercice(self, -1)

        self.liste_exercices.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn(u"Date début", "left", -1, "date_debut", stringConverter="%d-%m-%Y", minimumWidth=100),
            ColumnDefn(u"Date fin", "left", 100, "date_fin", stringConverter="%d-%m-%Y", isSpaceFilling=True)
        ])

        def rowFormatterLE(listItem, exercice):
            if exercice.date_debut < date.today() and exercice.date_fin > date.today():
                listItem.SetTextColour(wx.BLACK)
            else:
                listItem.SetTextColour("#616161")

        self.liste_exercices.rowFormatter = rowFormatterLE
        self.liste_exercices.SortBy(1, False)
        self.liste_exercices.SetEmptyListMsg(u"Il n'y a aucun exercice pour l'instant")

        self.__set_properties()
        self.__remplissage_liste()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutExercice, self.bouton_ajout_exercice)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionExercice, self.liste_exercices)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnExerciceSelectionne, self.liste_exercices)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GestionExercices.__set_properties
        self.sizer_navigation_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GestionExercices.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bas = wx.BoxSizer(wx.HORIZONTAL)
        sizer_details_exercice = wx.StaticBoxSizer(self.sizer_details_exercice_staticbox, wx.HORIZONTAL)
        sizer_header = wx.StaticBoxSizer(self.sizer_navigation_staticbox, wx.VERTICAL)
        sizer_header.Add(self.label_description, 0, wx.ALL, 5)
        sizer_header.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_header.Add(self.bouton_ajout_exercice, 0, wx.ALL, 5)
        sizer.Add(sizer_header, 0, wx.EXPAND, 0)
        sizer_bas.Add(self.liste_exercices, 1, wx.EXPAND, 0)
        sizer_details_exercice.Add(self.details_exercice, 1, wx.EXPAND, 0)
        sizer_bas.Add(sizer_details_exercice, 1, wx.LEFT, 10)
        sizer.Add(sizer_bas, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste(self):
        try:
            self.liste_exercices.SetObjects([e for e in Exercice.select()])
        except BaseException as ex:
            print ex

    def OnExerciceSelectionne(self, event):
        self.details_exercice.SetExercice(self.liste_exercices.GetSelectedObject())

    def OnAjoutExercice(self, event):
        dialog_exercice = wx.Dialog(self, title=u"Nouvel exercice")
        fiche_exercice = FicheExercice(dialog_exercice)
        dialog_exercice.Fit()
        dialog_exercice.ShowModal()
        dialog_exercice.Destroy()

        if dialog_exercice.GetReturnCode() == wx.ID_OK:
            self.liste_exercices.AddObject(fiche_exercice.GetExercice())
            self.liste_exercices.AutoSizeColumns()

    def OnEditionExercice(self, event):
        exercice = self.liste_exercices.GetSelectedObject()

        dialog_exercice = wx.Dialog(self, title=u"Exercice : " + exercice.nom)
        FicheExercice(dialog_exercice, exercice)
        dialog_exercice.Fit()
        dialog_exercice.ShowModal()
        dialog_exercice.Destroy()

        if dialog_exercice.GetReturnCode() == wx.ID_OK:
            self.liste_exercices.RefreshObject(self.liste_exercices.GetSelectedObject())
            self.liste_exercices.AutoSizeColumns()
