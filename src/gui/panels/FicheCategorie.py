#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Categorie, DATABASE
from classes.Validators import GenericTextValidator


###########################################################################
## Class FicheCategorie
###########################################################################


class FicheCategorie(wx.Panel):
    def __init__(self, parent, categorie=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if categorie == None:
            categorie = Categorie()

        self.categorie = categorie

        self.label_IDCategorie = wx.StaticText(self, -1, u"ID Catégorie :")
        self.combo_box_IDCategorie = wx.ComboBox(self, -1, choices=[],
                                                 style=wx.CB_DROPDOWN |
                                                 wx.CB_READONLY)
        self.label_IDCategorieV = wx.StaticText(self, -1, "IDCategorieV")
        self.label_NomCategorie = wx.StaticText(self, -1, "Nom :")
        self.text_NomCategorie = wx.TextCtrl(self, -1, "",
                                             style=wx.TE_PROCESS_ENTER,
                                             validator=GenericTextValidator())
        self.button_ok = wx.Button(self, wx.ID_OK, "Ok")
        self.button_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.button_ok.Bind(wx.EVT_BUTTON, self.onEnregistre)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnregistre, self.text_NomCategorie)

        self.Bind(wx.EVT_CLOSE, self.onClose, self)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.button_annuler)

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):

        # begin wxGlade: FicheCategorie2.__set_properties
        self.combo_box_IDCategorie.SetMinSize((70, -1))
        self.label_NomCategorie.SetMinSize((75, 21))
        self.text_NomCategorie.SetMinSize((250, -1))
        self.text_NomCategorie.SetBackgroundColour(wx.Colour(255, 255, 221))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FicheCategorie2.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(2, 2, 6, 6)
        sizer_id = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer.Add(self.label_IDCategorie, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_id.Add(self.label_IDCategorieV, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_id.Add(self.combo_box_IDCategorie, 0, 0, 0)
        grid_sizer.Add(sizer_id, 1, 0, 0)
        grid_sizer.Add(self.label_NomCategorie, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_NomCategorie, 0, wx.EXPAND, 0)
        sizer.Add(grid_sizer, 0, wx.ALL | wx.EXPAND, 10)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_ok, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_annuler, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer.Add(sizer_boutons, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

    def __set_valeurs(self):
        if self.categorie.get_id() != None:
            self.combo_box_IDCategorie.Hide()
            self.label_IDCategorieV.SetLabel(str(self.categorie.get_id()))
            self.text_NomCategorie.SetValue(self.categorie.nom)
        else:
            self.label_IDCategorieV.Hide()

            liste_ids = [str(n + 1).zfill(2) for n in range(99)]
            liste_ids_occupees = [str(x).zfill(2) for x in
                                  [cat.get_id() for cat in Categorie.select()]]

            liste_ids_libres = set(liste_ids) - set(liste_ids_occupees)

            self.combo_box_IDCategorie.SetItems(sorted(liste_ids_libres))

            self.combo_box_IDCategorie.Select(0)

    def onEnregistre(self, event):
        if self.Validate():
            self.categorie.nom = self.text_NomCategorie.GetValue()

            with DATABASE.transaction():
                if not self.categorie.get_id():
                    self.categorie.set_id(int(self.combo_box_IDCategorie.GetValue()))
                    self.categorie.insert(**dict(self.categorie._data)).execute()
                else:
                    self.categorie.save()

            event.Skip()

    def onClose(self, event):
        #session.rollback()
        event.Skip()
