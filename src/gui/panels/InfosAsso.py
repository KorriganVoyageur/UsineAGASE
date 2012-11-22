#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Parametre, DATABASE
from peewee import DoesNotExist

###########################################################################
## Class InfosAsso
###########################################################################


class InfosAsso(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        self.label_nom = wx.StaticText(self, -1, "Nom")
        self.text_ctrl_nom = wx.TextCtrl(self, -1, "")
        self.label_telephone = wx.StaticText(self, -1, u"Téléphone")
        self.text_ctrl_telephone = wx.TextCtrl(self, -1, "")
        self.label_adresse = wx.StaticText(self, -1, "Adresse")
        self.text_ctrl_adresse = wx.TextCtrl(self, -1, "")
        self.label_email = wx.StaticText(self, -1, "Email asso")
        self.text_ctrl_email = wx.TextCtrl(self, -1, "")
        self.label_code_postal = wx.StaticText(self, -1, "Code postal")
        self.text_ctrl_code_postal = wx.TextCtrl(self, -1, "")
        self.label_ville = wx.StaticText(self, -1, "Ville")
        self.text_ctrl_ville = wx.TextCtrl(self, -1, "")
        self.radio_box_type_adhesion = wx.RadioBox(self, -1, u"Type d'adhésion", choices=[u"Adhésion à l'année (valable 1 an à partir de la date d'adhésion)", u"Adhésion à l'exercice (valable entre le début et la fin de l'exercice)"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.bouton_sauvegarde_infos = wx.Button(self, -1, "Sauvegarder les informations sur l'association")

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnModifInfos, self.bouton_sauvegarde_infos)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: InfosAsso.__set_properties
        self.text_ctrl_nom.SetMinSize((200, -1))
        self.text_ctrl_telephone.SetMinSize((200, -1))
        self.text_ctrl_adresse.SetMinSize((200, -1))
        self.text_ctrl_email.SetMinSize((200, -1))
        self.text_ctrl_code_postal.SetMinSize((80, -1))
        self.text_ctrl_ville.SetMinSize((200, -1))
        self.radio_box_type_adhesion.SetSelection(0)
        # end wxGlade

    def __set_valeurs(self):
        self.ASSO_nom = Parametre.get_or_create(nom="ASSO_nom")
        self.ASSO_adresse = Parametre.get_or_create(nom="ASSO_adresse")
        self.ASSO_codepostal = Parametre.get_or_create(nom="ASSO_codepostal")
        self.ASSO_ville = Parametre.get_or_create(nom="ASSO_ville")
        self.ASSO_telephone = Parametre.get_or_create(nom="ASSO_telephone")
        self.ASSO_email = Parametre.get_or_create(nom="ASSO_email")

        #on doit retourner un entier, donc procédure spéciale
        try:
            self.ASSO_typeadhesion = Parametre.get(Parametre.nom == "ASSO_typeadhesion")
        except DoesNotExist:
            self.ASSO_typeadhesion = Parametre.create(nom="ASSO_typeadhesion", valeur="0")

        self.text_ctrl_nom.SetValue(self.ASSO_nom.valeur)
        self.text_ctrl_adresse.SetValue(self.ASSO_adresse.valeur)
        self.text_ctrl_code_postal.SetValue(self.ASSO_codepostal.valeur)
        self.text_ctrl_ville.SetValue(self.ASSO_ville.valeur)
        self.text_ctrl_telephone.SetValue(self.ASSO_telephone.valeur)
        self.text_ctrl_email.SetValue(self.ASSO_email.valeur)
        self.radio_box_type_adhesion.SetSelection(int(self.ASSO_typeadhesion.valeur))

    def __do_layout(self):
        # begin wxGlade: InfosAsso.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bouton_infos = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_infos = wx.FlexGridSizer(4, 4, 5, 10)
        grid_sizer_infos.Add(self.label_nom, 0, 0, 0)
        grid_sizer_infos.Add(self.text_ctrl_nom, 0, 0, 0)
        grid_sizer_infos.Add(self.label_telephone, 0, 0, 0)
        grid_sizer_infos.Add(self.text_ctrl_telephone, 0, 0, 0)
        grid_sizer_infos.Add(self.label_adresse, 0, 0, 0)
        grid_sizer_infos.Add(self.text_ctrl_adresse, 0, 0, 0)
        grid_sizer_infos.Add(self.label_email, 0, 0, 0)
        grid_sizer_infos.Add(self.text_ctrl_email, 0, 0, 0)
        grid_sizer_infos.Add(self.label_code_postal, 0, 0, 0)
        grid_sizer_infos.Add(self.text_ctrl_code_postal, 0, 0, 0)
        grid_sizer_infos.Add((1, 1), 0, 0, 0)
        grid_sizer_infos.Add((1, 1), 0, 0, 0)
        grid_sizer_infos.Add(self.label_ville, 0, 0, 0)
        grid_sizer_infos.Add(self.text_ctrl_ville, 0, 0, 0)
        sizer.Add(grid_sizer_infos, 0, wx.ALL, 5)
        sizer.Add(self.radio_box_type_adhesion, 0, wx.ALL|wx.EXPAND, 5)
        sizer_bouton_infos.Add(self.bouton_sauvegarde_infos, 0, 0, 0)
        sizer.Add(sizer_bouton_infos, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def OnModifInfos(self, event):
        self.ASSO_nom.valeur = self.text_ctrl_nom.GetValue()
        self.ASSO_adresse.valeur = self.text_ctrl_adresse.GetValue()
        self.ASSO_codepostal.valeur = self.text_ctrl_code_postal.GetValue()
        self.ASSO_ville.valeur = self.text_ctrl_ville.GetValue()
        self.ASSO_telephone.valeur = self.text_ctrl_telephone.GetValue()
        self.ASSO_email.valeur = self.text_ctrl_email.GetValue()
        self.ASSO_typeadhesion.valeur = str(self.radio_box_type_adhesion.GetSelection())

        with DATABASE.transaction():
            self.ASSO_nom.save()
            self.ASSO_adresse.save()
            self.ASSO_codepostal.save()
            self.ASSO_ville.save()
            self.ASSO_telephone.save()
            self.ASSO_email.save()
            self.ASSO_typeadhesion.save()
