#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import AdhesionType, DATABASE
from classes.Validators import GenericTextValidator, VALIDATE_FLOAT

###########################################################################
## Class FicheAdhesionType
###########################################################################


class FicheAdhesionType(wx.Panel):
    def __init__(self, parent, adhesion_type=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if adhesion_type == None:
            adhesion_type = AdhesionType()

        self.adhesion_type = adhesion_type

        self.label_nom = wx.StaticText(self, -1, "Nom")
        self.text_ctrl_Nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_prix = wx.StaticText(self, -1, "Prix")
        self.text_ctrl_Prix = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(flag=VALIDATE_FLOAT))
        self.label_euros = wx.StaticText(self, -1, u"€")
        self.bouton_valider = wx.Button(self, wx.ID_OK, "Valider")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnValider, self.bouton_valider)

    def __set_properties(self):
        self.text_ctrl_Nom.SetMinSize((200, -1))
        self.text_ctrl_Prix.SetMinSize((100, -1))

    def __set_valeurs(self):
        if self.adhesion_type.get_id():
            self.text_ctrl_Nom.SetValue(self.adhesion_type.nom)
            self.text_ctrl_Prix.SetValue(str(self.adhesion_type.prix))

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(3, 2, 5, 10)
        sizer_prix = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer.Add(self.label_nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_ctrl_Nom, 0, 0, 0)
        grid_sizer.Add(self.label_prix, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_prix.Add(self.text_ctrl_Prix, 0, 0, 0)
        sizer_prix.Add(self.label_euros, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer.Add(sizer_prix, 1, wx.EXPAND, 0)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_valider, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_annuler, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer.Add(sizer_bouton, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def GetTypeAdhesion(self):
        return self.adhesion_type

    def OnValider(self, event):
        if self.Validate():
            self.adhesion_type.nom = self.text_ctrl_Nom.GetValue()
            self.adhesion_type.prix = self.text_ctrl_Prix.GetValue()

            with DATABASE.transaction():
                self.adhesion_type.save()
            event.Skip()