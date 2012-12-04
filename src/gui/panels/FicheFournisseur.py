#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Fournisseur, DATABASE
from classes.Validators import GenericTextValidator, EmailValidator, VALIDATE_INT

###########################################################################
## Class FicheFournisseur
###########################################################################


class FicheFournisseur(wx.Panel):
    def __init__(self, parent, fournisseur=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if fournisseur == None:
            fournisseur = Fournisseur()

        self.fournisseur = fournisseur

        self.label_Nom = wx.StaticText(self, -1, "Nom :")
        self.text_Nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_Adresse = wx.StaticText(self, -1, "Adresse :")
        self.text_Adresse = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_CodePostal = wx.StaticText(self, -1, "Code Postal :")
        self.text_CodePostal = wx.TextCtrl(self, -1, "",
                                           validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_Ville = wx.StaticText(self, -1, "Ville :")
        self.text_Ville = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_TelephoneFixe = wx.StaticText(self, -1, u"Tel fixe :")
        self.text_TelephoneFixe = wx.TextCtrl(self, -1, "")
        self.label_TelephonePortable = wx.StaticText(self, -1, u"Tel portable :")
        self.text_TelephonePortable = wx.TextCtrl(self, -1, "")
        self.label_Email = wx.StaticText(self, -1, "Email :")
        self.text_Email = wx.TextCtrl(self, -1, "", validator=EmailValidator())
        self.label_NomContact = wx.StaticText(self, -1, "Nom du contact :")
        self.text_NomContact = wx.TextCtrl(self, -1, "")
        self.label_Remarques = wx.StaticText(self, -1, "Remarques :")
        self.text_Remarques = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.label_Couleur = wx.StaticText(self, -1, "Couleur :")
        self.button_Couleur = wx.Button(self, -1, "Choix de la couleur")
        self.text_Couleur = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.button_ok = wx.Button(self, wx.ID_OK, "")
        self.button_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__do_layout()
        self.__set_valeurs()

        self.button_ok.Bind(wx.EVT_BUTTON, self.OnEnregistre)
        self.button_Couleur.Bind(wx.EVT_BUTTON, self.selectionCouleur)

        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.button_annuler)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FicheFournisseur.__set_properties
        self.text_Nom.SetMinSize((300, -1))
        self.text_Nom.SetMaxLength(40)
        self.text_CodePostal.SetMinSize((80, -1))
        self.text_TelephoneFixe.SetMinSize((150, -1))
        self.text_TelephonePortable.SetMinSize((150, -1))
        self.text_Remarques.SetMinSize((-1, 87))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FicheFournisseur.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(8, 2, 6, 6)
        sizer_Couleur = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer.Add(self.label_Nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Nom, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Adresse, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Adresse, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_CodePostal, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_CodePostal, 0, 0, 0)
        grid_sizer.Add(self.label_Ville, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Ville, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_TelephoneFixe, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_TelephoneFixe, 0, 0, 0)
        grid_sizer.Add(self.label_TelephonePortable, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_TelephonePortable, 0, 0, 0)
        grid_sizer.Add(self.label_Email, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Email, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_NomContact, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_NomContact, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Remarques, 0, wx.TOP, 3)
        grid_sizer.Add(self.text_Remarques, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Couleur, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_Couleur.Add(self.text_Couleur, 1, wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 8)
        sizer_Couleur.Add(self.button_Couleur, 0, 0, 0)
        grid_sizer.Add(sizer_Couleur, 1, wx.EXPAND, 0)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer_boutons.Add(self.button_ok, 0, 0, 0)
        sizer_boutons.Add((80, 23), 0, 0, 0)
        sizer_boutons.Add(self.button_annuler, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer.Add(sizer_boutons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.SetSizer(sizer)
        self.Fit()
        self.Layout()
        # end wxGlade

    def __set_valeurs(self):
        if self.fournisseur.get_id() != None:
            self.text_Nom.SetValue(self.fournisseur.nom)
            self.text_Adresse.SetValue(self.fournisseur.adresse)
            self.text_CodePostal.SetValue(self.fournisseur.code_postal)
            self.text_Ville.SetValue(self.fournisseur.ville)
            self.text_TelephoneFixe.SetValue(self.fournisseur.telephone_fixe)
            self.text_TelephonePortable.SetValue(self.fournisseur.telephone_portable)
            self.text_Email.SetValue(self.fournisseur.email)
            self.text_NomContact.SetValue(self.fournisseur.nom_contact)
            self.text_Remarques.SetValue(self.fournisseur.remarques)
            self.text_Couleur.SetValue(self.fournisseur.couleur)
            self.text_Couleur.SetBackgroundColour(self.fournisseur.couleur)
        else:
            self.text_Couleur.SetValue("#FFFFFF")
            self.text_Couleur.SetBackgroundColour("#FFFFFF")

    def selectionCouleur(self, event):
        couleur_data = wx.ColourData()
        couleur_data.SetColour(self.text_Couleur.GetBackgroundColour())

        dlg = wx.ColourDialog(self, couleur_data)

        if dlg.ShowModal() == wx.ID_OK:
            self.couleur_fournisseur = dlg.GetColourData()
            couleur_data = self.couleur_fournisseur.GetColour()
            couleur_hex = couleur_data.GetAsString(wx.C2S_HTML_SYNTAX)
            self.text_Couleur.SetBackgroundColour(couleur_hex)
            self.text_Couleur.SetValue(couleur_hex)

        dlg.Destroy()

    def OnEnregistre(self, event):
        if self.Validate():
            self.fournisseur.nom = self.text_Nom.GetValue()
            self.fournisseur.adresse = self.text_Adresse.GetValue()
            self.fournisseur.code_postal = self.text_CodePostal.GetValue()
            self.fournisseur.ville = self.text_Ville.GetValue()
            self.fournisseur.telephone_fixe = self.text_TelephoneFixe.GetValue()
            self.fournisseur.telephone_portable = self.text_TelephonePortable.GetValue()
            self.fournisseur.email = self.text_Email.GetValue()
            self.fournisseur.nom_contact = self.text_NomContact.GetValue()
            self.fournisseur.remarques = self.text_Remarques.GetValue()
            self.fournisseur.couleur = self.text_Couleur.GetValue()

            with DATABASE.transaction():
                self.fournisseur.save()

            event.Skip()

    def OnClose(self, event):
        #session.rollback()
        event.Skip()
