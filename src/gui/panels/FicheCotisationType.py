#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import CotisationType, DATABASE
from classes.Validators import GenericTextValidator, VALIDATE_FLOAT

###########################################################################
## Class FicheCotisationType
###########################################################################


class FicheCotisationType(wx.Panel):
    def __init__(self, parent, cotisation_type=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if cotisation_type == None:
            cotisation_type = CotisationType()

        self.cotisation_type = cotisation_type

        self.label_nom = wx.StaticText(self, -1, "Nom")
        self.text_ctrl_nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_prix = wx.StaticText(self, -1, "Prix")
        self.text_ctrl_prix = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(flag=VALIDATE_FLOAT))
        self.label_euros = wx.StaticText(self, -1, u"€")
        self.bouton_valider = wx.Button(self, wx.ID_OK, "Valider")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnValider, self.bouton_valider)
        # end wxGlade

    def __set_properties(self):
        self.text_ctrl_nom.SetMinSize((200, -1))
        self.text_ctrl_prix.SetMinSize((100, -1))
        # end wxGlade

    def __set_valeurs(self):
        if self.cotisation_type.get_id():
            self.text_ctrl_nom.SetValue(self.cotisation_type.nom)
            self.text_ctrl_prix.SetValue(str(self.cotisation_type.prix))

    def __do_layout(self):
        # begin wxGlade: FicheTypeCotisation.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(3, 2, 5, 10)
        sizer_prix = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer.Add(self.label_nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_ctrl_nom, 0, 0, 0)
        grid_sizer.Add(self.label_prix, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_prix.Add(self.text_ctrl_prix, 0, 0, 0)
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
        # end wxGlade

    def GetTypeCotisation(self):
        return self.cotisation_type

    def OnValider(self, event):
        if self.Validate():
            self.cotisation_type.nom = self.text_ctrl_nom.GetValue()
            self.cotisation_type.prix = self.text_ctrl_prix.GetValue()

            with DATABASE.transaction():
                self.cotisation_type.save()

            event.Skip()
