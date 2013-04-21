#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Adherent, Referent, Fournisseur, CotisationType, DATABASE
from lib.objectlistview import ObjectListView, ColumnDefn
from gui.panels.FicheAdhesion import FicheAdhesion
from classes.Validators import GenericTextValidator, EmailValidator, LoginValidator, MotDePasseValidator, VALIDATE_INT


###########################################################################
## Class FicheAdherent
###########################################################################

class FicheAdherent(wx.Panel):
    def __init__(self, parent, adherent=None):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        #permet de faire un validate sur tout les panels
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)

        if adherent:
            self.adherent = adherent
        else:
            self.adherent = Adherent()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook_p1 = wx.Panel(self.notebook, -1)
        self.notebook_p2 = wx.Panel(self.notebook, -1)
        self.notebook_p3 = wx.Panel(self.notebook, -1)

        #self.sizer_adhesions_staticbox = wx.StaticBox(self.notebook_p4, -1, u"Types d'adhésion")
        #self.label_description_adhesions = wx.StaticText(self.notebook_p4, -1, u"Ce sont les différentes formules disponibles pour adhérer à l'association.")

        self.panel_adherent = FicheAdherentBase(self.notebook_p1, self.adherent)
        self.panel_gestion_adhesions = GestionAdhesions(self.notebook_p2, self.adherent)
        self.panel_gestion_fournisseurs = GestionFournisseurs(self.notebook_p3, self.adherent)
        
        self.bouton_ok = wx.Button(self, wx.ID_OK, "")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")
        
        self.bouton_ok.Bind(wx.EVT_BUTTON, self.OnEnregistre)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        #On affiche pas les panneaux secondaires pour un nouvel adhérent
        if not self.adherent.get_id():
            self.notebook_p2.Hide()
            self.notebook_p3.Hide()

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_p1 = wx.BoxSizer(wx.VERTICAL)
        sizer_p2 = wx.BoxSizer(wx.VERTICAL)
        sizer_p3 = wx.BoxSizer(wx.VERTICAL)

        sizer_p1.Add(self.panel_adherent, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p1.SetSizer(sizer_p1)

        sizer_p2.Add(self.panel_gestion_adhesions, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p2.SetSizer(sizer_p2)

        sizer_p3.Add(self.panel_gestion_fournisseurs, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p3.SetSizer(sizer_p3)

        self.notebook.AddPage(self.notebook_p1, u"Adhérent")
        self.notebook.AddPage(self.notebook_p2, u"Adhésions")
        self.notebook.AddPage(self.notebook_p3, u"Fournisseurs")

        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)

        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)

        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
    def GetAdherent(self):
        return self.adherent

    def OnEnregistre(self, event):
        if self.Validate():
            self.panel_adherent.Enregistre()
            DATABASE.commit()
            
            event.Skip()
        else:
            control = wx.Window.FindFocus()
            self.notebook.ChangeSelection(0)
            control.SetFocus()

    def OnClose(self, event):
        DATABASE.rollback()
        event.Skip()


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
        
        self.__set_properties()
        self.__do_layout()
        self.__set_combobox_cotisations()
        self.__set_valeurs()

    def __set_properties(self):
        self.text_Nom.SetMinSize((250, -1))
        self.text_CodePostal.SetMinSize((80, -1))
        self.text_TelephoneFixe.SetMinSize((150, -1))
        self.text_TelephonePortable.SetMinSize((150, -1))
        # end wxGlade

    def __do_layout(self):
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

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

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

    def Enregistre(self):
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

            #TODO: à revoir
            if self.text_Motdepasse.GetValue() != '':
                self.adherent.mot_de_passe = self.text_Motdepasse.GetValue()

            self.adherent.save()


###########################################################################
## Class GestionAdhesions
###########################################################################


class GestionAdhesions(wx.Panel):
    def __init__(self, parent, adherent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        
        self.adherent = adherent

        self.label_description = wx.StaticText(self, -1, u"Liste des cotisations réglées par l'adhérent.")
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.bouton_ajout_adhesion = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.bouton_supprime_adhesion = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))
        self.liste_adhesions = ObjectListView(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        self.liste_adhesions.SetColumns([
            ColumnDefn(u"Adhésion", "left", -1, "adhesion_type.nom", minimumWidth=100),
            ColumnDefn("Date", "left", -1, "date", stringConverter="%d-%m-%Y", minimumWidth=100),
            ColumnDefn("Montant", "left", 100,
                       "montant",
                       stringConverter=u"%.2f €",
                       isSpaceFilling=True)
        ])

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutAdhesion, self.bouton_ajout_adhesion)
        self.Bind(wx.EVT_BUTTON, self.OnSupprimeAdhesion, self.bouton_supprime_adhesion)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionAdhesion, self.liste_adhesions)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionAdhesion, self.liste_adhesions)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelectionAdhesion, self.liste_adhesions)
        # end wxGlade

    def __set_properties(self):
        self.bouton_ajout_adhesion.SetToolTip(wx.ToolTip(u"Ajouter une nouvelle adhésion"))
        self.bouton_supprime_adhesion.SetToolTip(wx.ToolTip(u"Supprimer l'adhésion sélectionnée"))
        self.bouton_supprime_adhesion.Disable()
        
        self.liste_adhesions.SetEmptyListMsg(u"Aucune adhésion")
        self.liste_adhesions.SortBy(1, False)

    def __do_layout(self):
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add(self.bouton_ajout_adhesion, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)
        sizer_boutons.Add((10, 10))
        sizer_boutons.Add(self.bouton_supprime_adhesion, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_description, 0, wx.TOP|wx.EXPAND, 10)
        sizer.Add(self.staticline, 0, wx.BOTTOM|wx.TOP|wx.EXPAND, 10)
        sizer.Add(sizer_boutons, 0, wx.BOTTOM | wx.ALIGN_RIGHT | wx.EXPAND, 5)
        sizer.Add(self.liste_adhesions, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def __remplissage_liste(self):
        try:
            self.liste_adhesions.SetObjects([a for a in self.adherent.adhesions])
        except BaseException as ex:
            print ex

    def OnSelectionAdhesion(self, event):
        if self.liste_adhesions.GetSelectedObject():
            self.bouton_supprime_adhesion.Enable()
        else:
            self.bouton_supprime_adhesion.Disable()

    def OnAjoutAdhesion(self, event):
        if self.adherent:
            dialog_adhesion = wx.Dialog(self, title=u"Nouvelle adhésion")
            fiche_adhesion = FicheAdhesion(dialog_adhesion, adherent=self.adherent)
                
            dialog_adhesion.Fit()
            dialog_adhesion.ShowModal()
            dialog_adhesion.Destroy()
    
            if dialog_adhesion.GetReturnCode() == wx.ID_OK:
                self.liste_adhesions.AddObject(fiche_adhesion.adhesion)
                self.liste_adhesions.AutoSizeColumns()
                
    def OnSupprimeAdhesion(self, event):
        adhesion = self.liste_adhesions.GetSelectedObject()

        msgbox = wx.MessageBox(u"Supprimer l'adhésion du %s ?" % adhesion.date.strftime("%d/%m/%y"), "Suppression", wx.YES_NO | wx.ICON_QUESTION)

        if msgbox == wx.YES:
            with DATABASE.transaction():
                adhesion.delete_instance()

            self.liste_adhesions.RemoveObject(adhesion)

    def OnEditionAdhesion(self, event):
        adhesion = self.liste_adhesions.GetSelectedObject()

        dialog_adhesion = wx.Dialog(self, title=u"Edition de l'adhésion")
        FicheAdhesion(dialog_adhesion, adhesion=adhesion)
        dialog_adhesion.Fit()
        dialog_adhesion.ShowModal()
        dialog_adhesion.Destroy()

        if dialog_adhesion.GetReturnCode() == wx.ID_OK:
            self.liste_adhesions.RefreshObject(self.liste_adhesions.GetSelectedObject())
            self.liste_adhesions.AutoSizeColumns()


###########################################################################
## Class GestionFournisseurs
###########################################################################


class GestionFournisseurs(wx.Panel):
    def __init__(self, parent, adherent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        
        self.adherent = adherent
        
        self.label_description = wx.StaticText(self, -1, u"Liste des fournisseurs dont l'adhérent est référent.")
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.bouton_ajout_fournisseur = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.bouton_supprime_fournisseur = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))
        self.liste_fournisseurs = ObjectListView(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        self.liste_fournisseurs.SetColumns([
            ColumnDefn(u"Fournisseur", "left", -1, "nom", minimumWidth=100,isSpaceFilling=True)
        ])

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutFournisseur, self.bouton_ajout_fournisseur)
        self.Bind(wx.EVT_BUTTON, self.OnSupprimeFournisseur, self.bouton_supprime_fournisseur)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionFournisseur, self.liste_fournisseurs)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelectionFournisseur, self.liste_fournisseurs)
        # end wxGlade

    def __set_properties(self):
        self.bouton_ajout_fournisseur.SetToolTip(wx.ToolTip(u"Ajouter un nouveau fournisseur"))
        self.bouton_supprime_fournisseur.SetToolTip(wx.ToolTip(u"Supprimer le fournisseur sélectionné"))
        self.bouton_supprime_fournisseur.Disable()
        
        self.liste_fournisseurs.SetEmptyListMsg("Aucun fournisseur")
        self.liste_fournisseurs.SortBy(0)

    def __do_layout(self):
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add(self.bouton_ajout_fournisseur, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)
        sizer_boutons.Add((10, 10))
        sizer_boutons.Add(self.bouton_supprime_fournisseur, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_description, 0, wx.TOP|wx.EXPAND, 10)
        sizer.Add(self.staticline, 0, wx.BOTTOM|wx.TOP|wx.EXPAND, 10)
        sizer.Add(sizer_boutons, 0, wx.BOTTOM | wx.ALIGN_RIGHT | wx.EXPAND, 5)
        sizer.Add(self.liste_fournisseurs, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def __remplissage_liste(self):
        try:
            self.liste_fournisseurs.SetObjects([f for f in self.adherent.fournisseurs])
        except BaseException as ex:
            print ex

    def OnSelectionFournisseur(self, event):
        if self.liste_fournisseurs.GetSelectedObject():
            self.bouton_supprime_fournisseur.Enable()
        else:
            self.bouton_supprime_fournisseur.Disable()

    def OnAjoutFournisseur(self, event):
        if self.adherent:
            dlg = DialogAjoutFournisseur(self.adherent)
                
            dlg.ShowModal()
    
            if dlg.GetReturnCode() == wx.ID_OK:
                Referent.create(adherent=self.adherent, fournisseur=dlg.GetFournisseur())
                self.liste_fournisseurs.AddObject(dlg.GetFournisseur())
                self.liste_fournisseurs.AutoSizeColumns()

            dlg.Destroy()
                
    def OnSupprimeFournisseur(self, event):
        fournisseur = self.liste_fournisseurs.GetSelectedObject()

        msgbox = wx.MessageBox(u"Supprimer le fournisseur \"%s\" ?" % fournisseur.nom, "Suppression", wx.YES_NO | wx.ICON_QUESTION)

        if msgbox == wx.YES:
            referent = Referent.select().where((Referent.adherent == self.adherent) & (Referent.fournisseur == fournisseur)).get()
            referent.delete_instance()

            self.liste_fournisseurs.RemoveObject(fournisseur)

            
###########################################################################
## Class DialogAjoutFournisseur
###########################################################################

class DialogAjoutFournisseur(wx.Dialog):
    def __init__(self, adherent):
        wx.Dialog.__init__(self, None, -1, title=u"Ajouter un fournisseur", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.adherent = adherent

        self.liste_fournisseurs = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_fournisseurs.SetColumns([
            ColumnDefn("Fournisseur", "left", -1, "nom", minimumWidth=100)
        ])

        self.liste_fournisseurs.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClickFournisseur)

        self.__set_properties()
        self.__remplissage_liste()
        self.__do_layout()

    def __set_properties(self):
        self.SetMinSize((200,300))
        self.liste_fournisseurs.SortBy(0)
    
    def __remplissage_liste(self):
        try:
            requete = Fournisseur.select().where(~(Fournisseur.id << self.adherent.fournisseurs))
            self.liste_fournisseurs.SetObjects([f for f in requete])
            
            #On dimentionne le dialog selon la largeur des colonnes
            largeur = 0
            for num_colonne in range(1) :
                largeur += self.liste_fournisseurs.GetColumnWidth(num_colonne)
             
            self.liste_fournisseurs.SetMinSize((largeur+20,300))
            
        except BaseException as ex:
            print ex

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.liste_fournisseurs, 1, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def GetFournisseur(self):
        return self.liste_fournisseurs.GetSelectedObject()

    def OnClickFournisseur(self, event):
        self.EndModal(wx.ID_OK)
