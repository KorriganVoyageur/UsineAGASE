#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import model

###########################################################################
## Class DetailsExercices
###########################################################################


class DetailsExercice(wx.Panel):
    def __init__(self, parent, exercice):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        self.exercice = exercice

        self.sizer_depenses_staticbox = wx.StaticBox(self, -1, u"Dépenses")
        self.sizer_recettes_staticbox = wx.StaticBox(self, -1, "Recettes")
        self.label_ex_nom = wx.StaticText(self, -1, "Nom de l'exercice :")
        self.label_ex_nom_v = wx.StaticText(self, -1, "XXX")
        self.label_exercice_dates = wx.StaticText(self, -1, "Dates de l'exercice :")
        self.label_exercice_dates_v = wx.StaticText(self, -1, "du XX-XX-XXXX au XX-XX-XXXX")
        self.label_adhesions_annuelles = wx.StaticText(self, -1, u"Adhésions annuelles :")
        self.label_adhesions_annulles_v = wx.StaticText(self, -1, u"XX.XX €")
        self.label_gase = wx.StaticText(self, -1, "GASE :")
        self.label_gase_v = wx.StaticText(self, -1, u"XX.XX €")
        self.label_cotisations = wx.StaticText(self, -1, "    - dont cotisations :")
        self.label_cotisations_v = wx.StaticText(self, -1, u"XX.XX€")
        self.static_line_recettes = wx.StaticLine(self, -1)
        self.label_total_recettes = wx.StaticText(self, -1, "Total :")
        self.label_total_recettes_v = wx.StaticText(self, -1, u"XX.XX €")
        self.label_loyers = wx.StaticText(self, -1, "Loyers :")
        self.label_loyers_v = wx.StaticText(self, -1, u"XX.XX €")
        self.label_commandes_GASE = wx.StaticText(self, -1, "Commandes du GASE :")
        self.label_commandes_GASE_v = wx.StaticText(self, -1, u"XX.XX €")
        self.static_line_depenses = wx.StaticLine(self, -1)
        self.label_total_depenses = wx.StaticText(self, -1, "Total :")
        self.label_total_depenses_v = wx.StaticText(self, -1, u"XX.XX €")

        self.__set_properties()
        #self.__set_valeurs()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GestionExcercices.__set_properties
        self.label_ex_nom.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_adhesions_annuelles.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_gase.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total_recettes.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_loyers.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_commandes_GASE.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total_depenses.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __set_valeurs(self):
        #self.exercice = model.Exercice()
        self.label_ex_nom_v.SetLabel(self.exercice.nom)
        self.label_exercice_dates_v.SetLabel("du " + self.exercice.date_debut.strftime("%d-%m-%Y") + " au " + self.exercice.date_fin.strftime("%d-%m-%Y"))

    def __do_layout(self):
        # begin wxGlade: GestionExcercices.__do_layout
        sizer_exercice = wx.BoxSizer(wx.VERTICAL)
        sizer_depenses = wx.StaticBoxSizer(self.sizer_depenses_staticbox, wx.HORIZONTAL)
        grid_sizer_depenses = wx.FlexGridSizer(5, 2, 5, 10)
        sizer_recettes = wx.StaticBoxSizer(self.sizer_recettes_staticbox, wx.HORIZONTAL)
        grid_sizer_recettes = wx.FlexGridSizer(5, 2, 5, 10)
        sizer_dates_ex_v = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ex_en_cours = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ex_en_cours.Add(self.label_ex_nom, 0, wx.RIGHT, 10)
        sizer_ex_en_cours.Add(self.label_ex_nom_v, 0, 0, 0)
        sizer_exercice.Add(sizer_ex_en_cours, 0, wx.ALL|wx.EXPAND, 5)
        sizer_dates_ex_v.Add(self.label_exercice_dates, 0, wx.RIGHT, 10)
        sizer_dates_ex_v.Add(self.label_exercice_dates_v, 0, 0, 0)
        sizer_exercice.Add(sizer_dates_ex_v, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        grid_sizer_recettes.Add(self.label_adhesions_annuelles, 0, 0, 0)
        grid_sizer_recettes.Add(self.label_adhesions_annulles_v, 0, 0, 0)
        grid_sizer_recettes.Add(self.label_gase, 0, 0, 0)
        grid_sizer_recettes.Add(self.label_gase_v, 0, 0, 0)
        grid_sizer_recettes.Add(self.label_cotisations, 0, 0, 0)
        grid_sizer_recettes.Add(self.label_cotisations_v, 0, 0, 0)
        grid_sizer_recettes.Add((180, 17), 0, 0, 0)
        grid_sizer_recettes.Add(self.static_line_recettes, 0, wx.EXPAND, 0)
        grid_sizer_recettes.Add(self.label_total_recettes, 0, 0, 0)
        grid_sizer_recettes.Add(self.label_total_recettes_v, 0, 0, 0)
        sizer_recettes.Add(grid_sizer_recettes, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer_exercice.Add(sizer_recettes, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_depenses.Add(self.label_loyers, 0, 0, 0)
        grid_sizer_depenses.Add(self.label_loyers_v, 0, 0, 0)
        grid_sizer_depenses.Add(self.label_commandes_GASE, 0, 0, 0)
        grid_sizer_depenses.Add(self.label_commandes_GASE_v, 0, 0, 0)
        grid_sizer_depenses.Add((180, 17), 0, 0, 0)
        grid_sizer_depenses.Add(self.static_line_depenses, 0, wx.EXPAND, 0)
        grid_sizer_depenses.Add(self.label_total_depenses, 0, 0, 0)
        grid_sizer_depenses.Add(self.label_total_depenses_v, 0, 0, 0)
        sizer_depenses.Add(grid_sizer_depenses, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer_exercice.Add(sizer_depenses, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_exercice)
        sizer_exercice.Fit(self)
        # end wxGlade

    def SetExercice(self, exercice):
        self.exercice = exercice
        self.__set_valeurs()