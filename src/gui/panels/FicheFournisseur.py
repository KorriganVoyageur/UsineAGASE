#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Fournisseur, Referent, Adherent, DATABASE
from classes.Validators import GenericTextValidator, EmailValidator, VALIDATE_INT
from lib.objectlistview import ObjectListView, ColumnDefn


###########################################################################
## Class FicheFournisseur
###########################################################################

class FicheFournisseur(wx.Panel):
    def __init__(self, parent, fournisseur):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        #permet de faire un validate sur tout les panels
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)

        if fournisseur:
            self.fournisseur = fournisseur
        else:
            self.fournisseur = Fournisseur()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook_p1 = wx.Panel(self.notebook, -1)
        self.notebook_p2 = wx.Panel(self.notebook, -1)

        #self.sizer_adhesions_staticbox = wx.StaticBox(self.notebook_p4, -1, u"Types d'adhésion")
        #self.label_description_adhesions = wx.StaticText(self.notebook_p4, -1, u"Ce sont les différentes formules disponibles pour adhérer à l'association.")

        self.panel_fournisseur = FicheFournisseurBase(self.notebook_p1, self.fournisseur)
        self.panel_gestion_referents = GestionReferents(self.notebook_p2, self.fournisseur)
        
        self.bouton_ok = wx.Button(self, wx.ID_OK, "")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")
        
        self.bouton_ok.Bind(wx.EVT_BUTTON, self.OnEnregistre)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnClose)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        #On affiche pas les panneaux secondaires pour un nouveau fournisseur
        if not self.fournisseur.get_id():
            self.notebook_p2.Hide()

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_p1 = wx.BoxSizer(wx.VERTICAL)
        sizer_p2 = wx.BoxSizer(wx.VERTICAL)

        sizer_p1.Add(self.panel_fournisseur, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p1.SetSizer(sizer_p1)

        sizer_p2.Add(self.panel_gestion_referents, 1, wx.ALL|wx.EXPAND, 5)
        self.notebook_p2.SetSizer(sizer_p2)

        self.notebook.AddPage(self.notebook_p1, u"Fournisseur")
        self.notebook.AddPage(self.notebook_p2, u"Référents")

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
        
    def GetFournisseur(self):
        return self.fournisseur

    def OnEnregistre(self, event):
        if self.Validate():
            self.panel_fournisseur.Enregistre()
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
## Class FicheFournisseurBase
###########################################################################


class FicheFournisseurBase(wx.Panel):
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

        self.__set_properties()
        self.__do_layout()
        self.__set_valeurs()

        self.button_Couleur.Bind(wx.EVT_BUTTON, self.selectionCouleur)

    def __set_properties(self):
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

    def Enregistre(self):
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

    def OnClose(self, event):
        #session.rollback()
        event.Skip()
        
        
###########################################################################
## Class GestionReferents
###########################################################################


class GestionReferents(wx.Panel):
    def __init__(self, parent, fournisseur):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        
        self.fournisseur = fournisseur
        
        """ Attention, ici le référent est un objet Adherent"""
        
        self.label_description = wx.StaticText(self, -1, u"Liste des référents du fournisseur.")
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.bouton_ajout_referent = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.bouton_supprime_referent = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))
        self.liste_referents = ObjectListView(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        self.liste_referents.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn(u"Prénom", "left", -1, "prenom", minimumWidth=100,isSpaceFilling=True)
        ])

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutReferent, self.bouton_ajout_referent)
        self.Bind(wx.EVT_BUTTON, self.OnSupprimeReferent, self.bouton_supprime_referent)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionReferent, self.liste_referents)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelectionReferent, self.liste_referents)
        # end wxGlade

    def __set_properties(self):
        self.bouton_ajout_referent.SetToolTip(wx.ToolTip(u"Ajouter un nouveau référent"))
        self.bouton_supprime_referent.SetToolTip(wx.ToolTip(u"Supprimer le référent sélectionné"))
        self.bouton_supprime_referent.Disable()
        
        self.liste_referents.SetEmptyListMsg(u"Aucun référent")
        self.liste_referents.SortBy(0)

    def __do_layout(self):
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add(self.bouton_ajout_referent, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)
        sizer_boutons.Add((10, 10))
        sizer_boutons.Add(self.bouton_supprime_referent, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_description, 0, wx.TOP|wx.EXPAND, 10)
        sizer.Add(self.staticline, 0, wx.BOTTOM|wx.TOP|wx.EXPAND, 10)
        sizer.Add(sizer_boutons, 0, wx.BOTTOM | wx.ALIGN_RIGHT | wx.EXPAND, 5)
        sizer.Add(self.liste_referents, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def __remplissage_liste(self):
        try:
            self.liste_referents.SetObjects([a for a in self.fournisseur.referents])
        except BaseException as ex:
            print ex

    def OnSelectionReferent(self, event):
        if self.liste_referents.GetSelectedObject():
            self.bouton_supprime_referent.Enable()
        else:
            self.bouton_supprime_referent.Disable()

    def OnAjoutReferent(self, event):
        if self.fournisseur:
            dlg = DialogAjoutReferent(self.fournisseur)
                
            dlg.ShowModal()
    
            if dlg.GetReturnCode() == wx.ID_OK:
                Referent.create(fournisseur=self.fournisseur, adherent=dlg.GetReferent())
                self.liste_referents.AddObject(dlg.GetReferent())
                self.liste_referents.AutoSizeColumns()

            dlg.Destroy()
                
    def OnSupprimeReferent(self, event):
        adherent = self.liste_referents.GetSelectedObject()

        msgbox = wx.MessageBox(u"Enlever %s de la liste des référent pour %s ?" % (adherent.prenom_nom, self.fournisseur.nom), "Suppression", wx.YES_NO | wx.ICON_QUESTION)

        if msgbox == wx.YES:
            referent = Referent.select().where((Referent.fournisseur == self.fournisseur) & (Referent.adherent == adherent)).get()
            referent.delete_instance()

            self.liste_referents.RemoveObject(adherent)

            
###########################################################################
## Class DialogAjoutReferent
###########################################################################

class DialogAjoutReferent(wx.Dialog):
    def __init__(self, fournisseur):
        wx.Dialog.__init__(self, None, -1, title=u"Ajouter un référent", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.fournisseur = fournisseur
        
        """ Attention, ici le référent est un objet Adherent"""

        self.liste_referents = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_referents.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn(u"Prénom", "left", -1, "prenom", minimumWidth=100, isSpaceFilling=True)
        ])

        self.liste_referents.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClickReferent)

        self.__set_properties()
        self.__remplissage_liste()
        self.__do_layout()

    def __set_properties(self):
        self.SetMinSize((200,300))
        self.liste_referents.SortBy(0)
    
    def __remplissage_liste(self):
        try:
            requete = Adherent.select().where(~(Adherent.id << self.fournisseur.referents))
            self.liste_referents.SetObjects([a for a in requete])
            
            #On dimentionne le dialog selon la largeur des colonnes
            largeur = 0
            for num_colonne in range(2) :
                largeur += self.liste_referents.GetColumnWidth(num_colonne)
             
            self.liste_referents.SetMinSize((largeur+20,300))
            
        except BaseException as ex:
            print ex

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.liste_referents, 1, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def GetReferent(self):
        return self.liste_referents.GetSelectedObject()

    def OnClickReferent(self, event):
        self.EndModal(wx.ID_OK)

