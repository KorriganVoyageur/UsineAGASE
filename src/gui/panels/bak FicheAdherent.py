#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Adherent, CotisationType, DATABASE
from lib.objectlistview import ObjectListView, ColumnDefn
from classes.Validators import GenericTextValidator, EmailValidator, LoginValidator, MotDePasseValidator, VALIDATE_INT

class PanelAdherant(wx.Panel):
    






###########################################################################
## Class FicheAdherent
###########################################################################


class FicheAdherent(wx.Panel):
    def __init__(self, parent, adherent=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if adherent == None:
            adherent = Adherent()

        self.adherent = adherent
        
        self.notebook = wx.Notebook(self, -1, style=0)

        self.notebook_p1 = wx.Panel(self.notebook, -1)

        self.notebook_p1.label_Nom = wx.StaticText(self, -1, "Nom :")
        self.notebook_p1.text_Nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.notebook_p1.label_Prenom = wx.StaticText(self, -1, u"Pr�nom :")
        self.notebook_p1.text_Prenom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.notebook_p1.label_Adresse = wx.StaticText(self, -1, "Adresse :")
        self.notebook_p1.text_Adresse = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.notebook_p1.label_CodePostal = wx.StaticText(self, -1, "Code Postal :")
        self.notebook_p1.text_CodePostal = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(flag=VALIDATE_INT))
        self.notebook_p1.label_Ville = wx.StaticText(self, -1, "Ville :")
        self.notebook_p1.text_Ville = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.notebook_p1.label_TelephoneFixe = wx.StaticText(self, -1, u"Tel fixe:")
        self.notebook_p1.text_TelephoneFixe = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(obligatoire=False))
        self.notebook_p1.label_TelephonePortable = wx.StaticText(self, -1, u"Tel portable :")
        self.notebook_p1.text_TelephonePortable = wx.TextCtrl(self, -1, "", validator=GenericTextValidator(obligatoire=False))
        self.notebook_p1.label_Email = wx.StaticText(self, -1, "Email :")
        self.notebook_p1.text_Email = wx.TextCtrl(self, -1, "", validator=EmailValidator(obligatoire=False))
        self.notebook_p1.label_Cotisation = wx.StaticText(self, -1, "Cotisation :")
        self.notebook_p1.combo_box_CotisationTypes = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.notebook_p1.label_Login = wx.StaticText(self, -1, "Login :")
        self.notebook_p1.text_Login = wx.TextCtrl(self, -1, "")
        self.notebook_p1.label_ConfirmMotdepasse = wx.StaticText(self, -1, "Confirmation :")
        self.notebook_p1.text_ConfirmMotdepasse = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.notebook_p1.label_Motdepasse = wx.StaticText(self, -1, "Mot de passe :")
        self.notebook_p1.text_Motdepasse = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD, validator=MotDePasseValidator(self.notebook_p1.text_ConfirmMotdepasse))

        self.notebook_p1.button_ok = wx.Button(self, wx.ID_OK, "")
        self.notebook_p1.button_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        '''self.notebook_p2 = wx.Panel(self.notebook, -1)
        
        self.notebook_p2.bouton_ajout_adhesion = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.notebook_p2.bouton_supprime_adhesion = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))
        self.notebook_p2.liste_categories = ObjectListView(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        self.notebook_p2.liste_categories.SetColumns([
            ColumnDefn(u"Adh�sion", "left", -1, "adhesion_type.nom"),
            ColumnDefn("Date", "left", -1, "date"),
            ColumnDefn("Montant", "left", 100,
                       "montant",
                       stringConverter="%f �",
                       isSpaceFilling=True)
        ])'''
        

        self.__set_properties()
        self.__do_layout()
        self.__set_combobox_cotisations()
        self.__set_valeurs()

        self.notebook_p1.button_ok.Bind(wx.EVT_BUTTON, self.OnEnregistre)

        self.notebook_p1.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.notebook_p1.Bind(wx.EVT_BUTTON, self.OnClose, self.notebook_p1.button_annuler)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FicheFournisseur.__set_properties
        self.notebook_p1.text_Nom.SetMinSize((250, -1))
        self.notebook_p1.text_CodePostal.SetMinSize((80, -1))
        self.notebook_p1.text_TelephoneFixe.SetMinSize((150, -1))
        self.notebook_p1.text_TelephonePortable.SetMinSize((150, -1))

        '''self.notebook_p2.bouton_ajout_adhesion.SetToolTip(wx.ToolTip(u"Ajouter une nouvelle adh�sion"))
        self.notebook_p2.bouton_supprime_adhesion.SetToolTip(wx.ToolTip(u"Supprimer l'adh�sion s�lectionn�e"))
        self.notebook_p2.bouton_supprime_adhesion.Disable()'''

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer_p1 = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons_p1 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_p1 = wx.FlexGridSizer(10, 2, 6, 6)

        grid_sizer_p1.Add(self.notebook_p1.label_Nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Nom, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Prenom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Prenom, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Adresse, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Adresse, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_CodePostal, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_CodePostal, 0, 0, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Ville, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Ville, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_TelephoneFixe, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_TelephoneFixe, 0, 0, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_TelephonePortable, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_TelephonePortable, 0, 0, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Email, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Email, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Cotisation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.combo_box_CotisationTypes, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Login, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Login, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_Motdepasse, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_Motdepasse, 0, wx.EXPAND, 0)
        grid_sizer_p1.Add(self.notebook_p1.label_ConfirmMotdepasse, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_p1.Add(self.notebook_p1.text_ConfirmMotdepasse, 0, wx.EXPAND, 0)

        sizer_p1.Add(grid_sizer_p1, 0, wx.ALL|wx.EXPAND, 10)

        sizer_boutons_p1.Add((20, 20), 1, 0, 0)
        sizer_boutons_p1.Add(self.notebook_p1.button_ok, 0, 0, 0)
        sizer_boutons_p1.Add((20, 20), 1, 0, 0)
        sizer_boutons_p1.Add(self.notebook_p1.button_annuler, 0, 0, 0)
        sizer_boutons_p1.Add((20, 20), 1, 0, 0)

        sizer_p1.Add(sizer_boutons_p1, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        self.notebook_p1.SetSizer(sizer_p1)
        #self.notebook_p1.Fit()
        
        '''sizer_p2 = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons_p2 = wx.BoxSizer(wx.HORIZONTAL)
        #grid_sizer_p2 = wx.FlexGridSizer(10, 2, 6, 6)
        
        sizer_boutons_p2.Add((20, 20), 1, 0, 0)
        sizer_boutons_p2.Add(self.notebook_p2.bouton_ajout_adhesion, 0, 0, 0)
        sizer_boutons_p2.Add((20, 20), 1, 0, 0)
        sizer_boutons_p2.Add(self.notebook_p2.bouton_supprime_adhesion, 0, 0, 0)
        sizer_boutons_p2.Add((20, 20), 1, 0, 0)
        
        sizer_p2.Add(sizer_boutons_p2, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        sizer_p2.Add(self.notebook_p2.liste_categories, 0, wx.ALL|wx.EXPAND, 10)
        
        self.notebook_p2.SetSizer(sizer_p2)
        self.notebook_p2.Fit()'''
        
        self.notebook.AddPage(self.notebook_p1, u"Adh�rant")
        #self.notebook.AddPage(self.notebook_p2, u"Adh�sions")
        
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        self.Layout()
        # end wxGlade

    def __set_combobox_cotisations(self):
        try:
            cotisation_types = [c for c in CotisationType.select().order_by(CotisationType.nom.asc())]
            for c in cotisation_types:
                self.notebook_p1.combo_box_CotisationTypes.Append(c.nom + u" - %s �" % c.prix, c)

            self.notebook_p1.combo_box_CotisationTypes.Select(0)

        except BaseException as ex:
            print ex

    def __set_valeurs(self):
        if self.adherent.get_id():
            self.notebook_p1.text_Nom.SetValue(self.adherent.nom)
            self.notebook_p1.text_Prenom.SetValue(self.adherent.prenom)
            self.notebook_p1.text_Adresse.SetValue(self.adherent.adresse)
            self.notebook_p1.text_CodePostal.SetValue(self.adherent.code_postal)
            self.notebook_p1.text_Ville.SetValue(self.adherent.ville)
            self.notebook_p1.text_TelephoneFixe.SetValue(self.adherent.telephone_fixe)
            self.notebook_p1.text_TelephonePortable.SetValue(self.adherent.telephone_portable)
            self.notebook_p1.text_Email.SetValue(self.adherent.email)
            self.notebook_p1.text_Login.SetValue(self.adherent.login)
            #self.text_Login.SetValidator(LoginValidator(self.adherent.GetLogins()))

            for i in range(len(self.notebook_p1.combo_box_CotisationTypes.GetItems())):
                if self.adherent.cotisation_type == self.notebook_p1.combo_box_CotisationTypes.GetClientData(i):
                    self.notebook_p1.combo_box_CotisationTypes.Select(i)
                    break

        #TODO: On ajoute le validator de logins
        #self.text_Login.SetValidator(LoginValidator(self.adherent.GetLogins()))

    def GetAdherent(self):
        return self.adherent

    def OnEnregistre(self, event):
        if self.Validate():
            self.adherent.nom = self.notebook_p1.text_Nom.GetValue()
            self.adherent.prenom = self.notebook_p1.text_Prenom.GetValue()
            self.adherent.adresse = self.notebook_p1.text_Adresse.GetValue()
            self.adherent.code_postal = self.notebook_p1.text_CodePostal.GetValue()
            self.adherent.ville = self.notebook_p1.text_Ville.GetValue()
            self.adherent.telephone_fixe = self.notebook_p1.text_TelephoneFixe.GetValue()
            self.adherent.telephone_portable = self.notebook_p1.text_TelephonePortable.GetValue()
            self.adherent.email = self.notebook_p1.text_Email.GetValue()
            self.adherent.cotisation_type = self.notebook_p1.combo_box_CotisationTypes.GetClientData(self.notebook_p1.combo_box_CotisationTypes.GetSelection())
            self.adherent.login = self.notebook_p1.text_Login.GetValue()

            if self.notebook_p1.text_Motdepasse.GetValue() != '':
                self.adherent.mot_de_passe = self.notebook_p1.text_Motdepasse.GetValue()

            with DATABASE.transaction():
                self.adherent.save()

            event.Skip()

    def OnClose(self, event):
        #session.rollback()
        event.Skip()
