#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Tva, DATABASE
from classes.Validators import GenericTextValidator, VALIDATE_FLOAT

###########################################################################
## Class FicheTVA
###########################################################################


class FicheTVA(wx.Panel):
    def __init__(self, parent, tva=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if tva == None:
            tva = Tva()

        self.tva = tva

        self.label_TauxTVA = wx.StaticText(self, -1, "Taux :")
        self.text_TauxTVA = wx.TextCtrl(self, -1, "",
                                       style=wx.TE_PROCESS_ENTER,
                                       validator=GenericTextValidator(flag=VALIDATE_FLOAT))
        self.button_ok = wx.Button(self, wx.ID_OK, "Ok")
        self.button_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.button_ok.Bind(wx.EVT_BUTTON, self.onEnregistre)
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnregistre, self.text_TauxTVA)

        self.Bind(wx.EVT_CLOSE, self.onClose, self)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.button_annuler)

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FicheTVA.__set_properties
        self.label_TauxTVA.SetMinSize((75, 21))
        self.text_TauxTVA.SetMinSize((250, -1))
        self.text_TauxTVA.SetBackgroundColour(wx.Colour(255, 255, 221))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FicheTVA.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_taux = wx.BoxSizer(wx.HORIZONTAL)
        sizer_taux.Add(self.label_TauxTVA, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_taux.Add(self.text_TauxTVA, 0, wx.EXPAND, 0)
        sizer.Add(sizer_taux, 0, wx.ALL|wx.EXPAND, 10)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_ok, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_annuler, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

    def __set_valeurs(self):
        if self.tva.get_id() != None:
            self.text_TauxTVA.SetValue(str(self.tva.taux))

    def GetTVA(self):
        return self.tva

    def OnEnregistre(self, event):
        if self.Validate():
            self.tva.taux = self.text_TauxTVA.GetValue()

            with DATABASE.transaction():
                self.tva.save()

            event.Skip()

    def OnClose(self, event):
        event.Skip()
