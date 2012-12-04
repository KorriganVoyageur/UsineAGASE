#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import model

###########################################################################
## Class VerificationLigneCommande
###########################################################################

class VerificationLigneCommande(wx.Dialog):
    def __init__(self, label_tc="", label_u=u"unit�(s)", validator=None, title="", quantite=0, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
        # begin wxGlade: FicheCategorie.__init__
        #kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, None, -1, title, pos, size, style)
        self.label_type_conditionnement = wx.StaticText(self, -1, label_tc)
        self.label_quantite = wx.StaticText(self, -1, u"Quantit� :")
        self.text_ctrl_quantite = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER, validator=validator)
        self.label_unite = wx.StaticText(self, -1, label_u)
        self.button_ok = wx.Button(self, wx.ID_OK, "")
        if quantite > 0 :
            self.text_ctrl_quantite.SetValue(str(quantite))
            self.button_annuler = wx.Button(self, wx.ID_DELETE, "Supprimer")
            self.Bind(wx.EVT_BUTTON, self.OnSupprimer, self.button_annuler)
        else :
            self.button_annuler = wx.Button(self, wx.ID_CANCEL, "")
            
        self.Bind(wx.EVT_TEXT_ENTER, self.onEnregistrer, self.text_ctrl_quantite)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ChoixQuantiteDialog.__set_properties
        self.SetTitle(u"Quantit�")
        self.text_ctrl_quantite.SetMinSize((80, -1))
        self.text_ctrl_quantite.SetFocus()
        if self.label_type_conditionnement.GetLabel() == "" :
            self.label_type_conditionnement.Hide()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ChoixQuantiteDialog.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_type_conditionnement, 0, wx.ALIGN_CENTER|wx.TOP, 5)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choix = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choix.Add(self.label_quantite, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_choix.Add(self.text_ctrl_quantite, 0, wx.LEFT|wx.RIGHT, 6)
        sizer_choix.Add(self.label_unite, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer.Add(sizer_choix, 0, wx.ALL|wx.EXPAND, 5)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.button_ok, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.button_annuler, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer.Add(sizer_boutons, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        # end wxGlade
    
    def GetValue(self):
        return int(self.text_ctrl_quantite.GetValue())

    def OnEnregistrer(self, event):
        if self.Validate() :
            self.EndModal(wx.ID_OK)
    
    def OnSupprimer(self, event):
        self.EndModal(wx.ID_DELETE)