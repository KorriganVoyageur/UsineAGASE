#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Adherent, CotisationType, DATABASE
from gui.panels.GestionAdhesions import GestionAdhesions
from classes.Validators import GenericTextValidator, EmailValidator, LoginValidator, MotDePasseValidator, VALIDATE_INT

###########################################################################
## Class FicheAdherentBase
###########################################################################

class FicheAdherentBase(wx.Panel):
    def __init__(self, parent, adherent=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if adherent:
            self.adherent = adherent
        else:
            self.adherent = Adherent()

        self.label_Nom = wx.StaticText(self, -1, "Nom :")
        self.text_Nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_Prenom = wx.StaticText(self, -1, u"Prénom :")
        self.text_Prenom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_Adresse = wx.StaticText(self, -1, "Adresse :")
        self.text_Adresse = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_CodePostal = wx.StaticText(self, -1, "Code Postal :")
        self.text_CodePostal = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_Ville = wx.StaticText(self, -1, "Ville :")
        self.text_Ville = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_TelephoneFixe = wx.StaticText(self, -1, u"Tel fixe:")
        self.text_TelephoneFixe = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(obligatoire=False))
        self.label_TelephonePortable = wx.StaticText(self, -1, u"Tel portable :")
        self.text_TelephonePortable = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(obligatoire=False))
        self.label_Email = wx.StaticText(self, -1, "Email :")
        self.text_Email = wx.TextCtrl(self, -1, "", validator=EmailValidator(obligatoire=False))
        self.label_Cotisation = wx.StaticText(self, -1, "Cotisation :")
        self.combo_box_CotisationTypes = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_Login = wx.StaticText(self, -1, "Login :")
        self.text_Login = wx.TextCtrl(self, -1, "")
        self.label_ConfirmMotdepasse = wx.StaticText(self, -1, "Confirmation :")
        self.text_ConfirmMotdepasse = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.label_Motdepasse = wx.StaticText(self, -1, "Mot de passe :")
        self.text_Motdepasse = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD, validator=MotDePasseValidator(self.text_ConfirmMotdepasse))

        self.button_ok = wx.Button(self, wx.ID_OK, "")
        self.button_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")
        
        self.__set_properties()
        self.__do_layout()
        self.__set_combobox_cotisations()
        self.__set_valeurs()

        self.button_ok.Bind(wx.EVT_BUTTON, self.onEnregistre)

        self.Bind(wx.EVT_CLOSE, self.onClose, self)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.button_annuler)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FicheFournisseur.__set_properties
        self.text_Nom.SetMinSize((250, -1))
        self.text_CodePostal.SetMinSize((80, -1))
        self.text_TelephoneFixe.SetMinSize((150, -1))
        self.text_TelephonePortable.SetMinSize((150, -1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FicheFournisseur.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(10, 2, 6, 6)

        grid_sizer.Add(self.label_Nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Nom, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Prenom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Prenom, 0, wx.EXPAND, 0)
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
        grid_sizer.Add(self.label_Cotisation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.combo_box_CotisationTypes, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Login, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Login, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Motdepasse, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Motdepasse, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_ConfirmMotdepasse, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_ConfirmMotdepasse, 0, wx.EXPAND, 0)

        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)

        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_ok, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_annuler, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)

        sizer.Add(sizer_boutons, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()
        # end wxGlade

    def __set_combobox_cotisations(self):
        try:
            cotisation_types = [c for c in CotisationType.select().order_by(CotisationType.prix.asc())]
            for c in cotisation_types:
                self.combo_box_CotisationTypes.Append(c.nom + u" - %s €" % c.prix, c)

            self.combo_box_CotisationTypes.Select(0)

        except BaseException as ex:
            print ex

    def __set_valeurs(self):
        if self.adherent.get_id():
            self.text_Nom.SetValue(self.adherent.nom)
            self.text_Prenom.SetValue(self.adherent.prenom)
            self.text_Adresse.SetValue(self.adherent.adresse)
            self.text_CodePostal.SetValue(self.adherent.code_postal)
            self.text_Ville.SetValue(self.adherent.ville)
            self.text_TelephoneFixe.SetValue(self.adherent.telephone_fixe)
            self.text_TelephonePortable.SetValue(self.adherent.telephone_portable)
            self.text_Email.SetValue(self.adherent.email)
            self.text_Login.SetValue(self.adherent.login)
            #self.text_Login.SetValidator(LoginValidator(self.adherent.GetLogins()))

            for i in range(len(self.combo_box_CotisationTypes.GetItems())):
                if self.adherent.cotisation_type == self.combo_box_CotisationTypes.GetClientData(i):
                    self.combo_box_CotisationTypes.Select(i)
                    break

        #TODO: On ajoute le validator de logins
        #self.text_Login.SetValidator(LoginValidator(self.adherent.GetLogins()))

    def GetAdherent(self):
        return self.adherent

    def onEnregistre(self, event):
        if self.Validate():
            self.adherent.nom = self.text_Nom.GetValue()
            self.adherent.prenom = self.text_Prenom.GetValue()
            self.adherent.adresse = self.text_Adresse.GetValue()
            self.adherent.code_postal = self.text_CodePostal.GetValue()
            self.adherent.ville = self.text_Ville.GetValue()
            self.adherent.telephone_fixe = self.text_TelephoneFixe.GetValue()
            self.adherent.telephone_portable = self.text_TelephonePortable.GetValue()
            self.adherent.email = self.text_Email.GetValue()
            self.adherent.cotisation_type = self.combo_box_CotisationTypes.GetClientData(self.combo_box_CotisationTypes.GetSelection())
            self.adherent.login = self.text_Login.GetValue()

            if self.text_Motdepasse.GetValue() != '':
                self.adherent.mot_de_passe = self.text_Motdepasse.GetValue()

            with DATABASE.transaction():
                self.adherent.save()

            event.Skip()

    def onClose(self, event):
        event.Skip()
        

###########################################################################
## Class FicheAdherentBase
###########################################################################

class FicheAdherent(wx.Panel):
    def __init__(self, parent, adherent=None):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        if adherent:
            self.adherent = adherent
        else:
            self.adherent = Adherent()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook_p2 = wx.Panel(self.notebook, -1)
        self.notebook_p1 = wx.Panel(self.notebook, -1)

        #self.sizer_adhesions_staticbox = wx.StaticBox(self.notebook_p4, -1, u"Types d'adhésion")
        #self.label_description_adhesions = wx.StaticText(self.notebook_p4, -1, u"Ce sont les différentes formules disponibles pour adhérer à l'association.")

        self.panel_adherent = FicheAdherentBase(self.notebook_p1, self.adherent)
        self.panel_gestion_adhesions = GestionAdhesions(self.notebook_p2, self.adherent)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        #On affiche pas le panneau cotisation pour un nouvel adhérent
        if not self.adherent.get_id():
            self.notebook_p2.Hide()

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_p2 = wx.BoxSizer(wx.VERTICAL)
        sizer_p1 = wx.BoxSizer(wx.VERTICAL)

        sizer_p1.Add(self.panel_adherent, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p1.SetSizer(sizer_p1)

        sizer_p2.Add(self.panel_gestion_adhesions, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p2.SetSizer(sizer_p2)

        self.notebook.AddPage(self.notebook_p1, u"Adhérent")
        self.notebook.AddPage(self.notebook_p2, u"Adhésions")
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
    def GetAdherent(self):
        return self.adherent
