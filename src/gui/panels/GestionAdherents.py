#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from lib.objectlistview import ObjectListView, ColumnDefn, OLVEvent, Filter
from model.model import Adherent, CotisationType
from peewee import DoesNotExist

from gui.panels.FicheAdherent import FicheAdherent
from gui.panels.FicheAdhesion import FicheAdhesion

###########################################################################
## Class GestionAdherents
###########################################################################


class GestionAdherents(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        self.sizer_communication_staticbox = wx.StaticBox(self, -1, "Communication")
        self.sizer_autre_staticbox = wx.StaticBox(self, -1, "Autre")
        self.sizer_critere_utilisateur_staticbox = wx.StaticBox(self, -1, "Utilisateurs")
        self.checkbox_gase = wx.CheckBox(self, -1, "GASE")
        self.checkbox_paniers = wx.CheckBox(self, -1, "Paniers")
        self.radio_box_etat_adhesion = wx.RadioBox(self, -1, u"Etat de l'adhésion", choices=["Tous", u"Adhésion à jour", u"Adhésion à renouveler"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.checkbox_sans_email = wx.CheckBox(self, -1, "Sans email")
        self.checkbox_sans_telephone = wx.CheckBox(self, -1, u"Sans téléphone")
        self.checkbox_ancien_adherents = wx.CheckBox(self, -1, u"Anciens adhérents")
        self.bouton_ajout_adhesion = wx.BitmapButton(self, -1, wx.Bitmap("../icons/32x32/nouvelle_adhesion.ico", wx.BITMAP_TYPE_ANY))
        self.bouton_ajout_credit = wx.BitmapButton(self, -1, wx.Bitmap("../icons/32x32/ajout_credit.png", wx.BITMAP_TYPE_ANY))
        self.static_line_1 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.label_recherche = wx.StaticText(self, -1, "Recherche sur le nom")
        self.text_ctrl_recherche = wx.TextCtrl(self, -1, "")
        self.static_line_2 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.bouton_ajout_adherent = wx.BitmapButton(self, -1, wx.Bitmap("../icons/32x32/nouvel_adherent.ico", wx.BITMAP_TYPE_ANY))
        self.liste_adherents = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        def AJour(value):
            if value:
                return "A jour"
            else:
                return u"Pas à jour"

        self.liste_adherents.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom",  minimumWidth=100, useInitialLetterForGroupKey=True),
            ColumnDefn(u"Prénom", "left", -1, "prenom", minimumWidth=100),
            ColumnDefn("Ville", "left", -1, "ville", minimumWidth=100),
            ColumnDefn(u"Téléphone", "left", -1, "telephone", minimumWidth=100),
            ColumnDefn(u"Cotisation", "left", -1, "cotisation_type.nom", minimumWidth=100),
            ColumnDefn(u"Adhésion", "left", 100, "is_adhesion_a_jour", stringConverter=AJour, isSpaceFilling=True, minimumWidth=100)
        ])

        def RFListeAdherents(listItem, adherent):
            if adherent.is_adhesion_a_jour:
                listItem.SetBackgroundColour("#E3FFCB")
            else:
                listItem.SetBackgroundColour("#FFD3D3")

        self.liste_adherents.rowFormatter = RFListeAdherents

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()
        self.liste_adherents.SetSortColumn(0, True)

        self.filtres = {}

        self.Bind(wx.EVT_BUTTON, self.OnAjoutAdhesion, self.bouton_ajout_adhesion)
        self.Bind(wx.EVT_BUTTON, self.OnAjoutCredit, self.bouton_ajout_credit)
        self.Bind(wx.EVT_BUTTON, self.OnAjoutAdherent, self.bouton_ajout_adherent)
        self.Bind(wx.EVT_RADIOBOX, self.OnFilterAdhesion, self.radio_box_etat_adhesion)
        self.Bind(wx.EVT_CHECKBOX, self.OnFilterSansEmail, self.checkbox_sans_email)
        self.Bind(wx.EVT_CHECKBOX, self.OnFilterSansTelephone, self.checkbox_sans_telephone)
        self.Bind(wx.EVT_CHECKBOX, self.OnFilterUtilisateursPaniers, self.checkbox_paniers)
        self.Bind(wx.EVT_CHECKBOX, self.OnFilterAnciensAdherents, self.checkbox_ancien_adherents)
        self.Bind(wx.EVT_TEXT, self.OnFilterNom, self.text_ctrl_recherche)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionAdherent, self.liste_adherents)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionAdherent, self.liste_adherents)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeselectionAdherent, self.liste_adherents)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnClickDroitListe, self.liste_adherents)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GestionAdherents.__set_properties
        self.checkbox_gase.SetToolTipString("Afficher les utilisateurs du GASE")
        self.checkbox_paniers.SetToolTipString("Afficher les utilisateurs des paniers")
        self.radio_box_etat_adhesion.SetSelection(0)
        self.checkbox_sans_email.SetToolTipString(u"Afficher les adhérents n'ayant pas d'email")
        self.checkbox_sans_telephone.SetToolTipString(u"Afficher les adhérents n'ayant pas de téléphone")
        self.checkbox_ancien_adherents.SetToolTipString(u"Afficher les anciens adhérents")
        self.bouton_ajout_adhesion.SetToolTipString(u"Ajouter un adhésion")
        self.bouton_ajout_adhesion.Enable(False)
        self.bouton_ajout_adhesion.SetSize(self.bouton_ajout_adhesion.GetBestSize())
        self.bouton_ajout_credit.SetToolTipString(u"Ajouter un crédit")
        self.bouton_ajout_credit.Enable(False)
        self.bouton_ajout_credit.SetSize(self.bouton_ajout_credit.GetBestSize())
        self.text_ctrl_recherche.SetMinSize((200, -1))
        self.bouton_ajout_adherent.SetToolTipString(u"Ajouter un nouvel adhérent")
        self.bouton_ajout_adherent.SetSize(self.bouton_ajout_adherent.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GestionAdherents.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        sizer_criteres = wx.BoxSizer(wx.HORIZONTAL)
        sizer_autre = wx.StaticBoxSizer(self.sizer_autre_staticbox, wx.VERTICAL)
        sizer_communication = wx.StaticBoxSizer(self.sizer_communication_staticbox, wx.VERTICAL)

        sizer_critere_utilisateur = wx.StaticBoxSizer(self.sizer_critere_utilisateur_staticbox, wx.VERTICAL)
        sizer_critere_utilisateur.Add(self.checkbox_gase, 0, 0, 0)
        sizer_critere_utilisateur.Add(self.checkbox_paniers, 0, 0, 0)
        sizer_criteres.Add(sizer_critere_utilisateur, 1, wx.EXPAND, 0)

        sizer_criteres.Add(self.radio_box_etat_adhesion, 1, 0, 20)

        sizer_communication.Add(self.checkbox_sans_email, 0, 0, 0)
        sizer_communication.Add(self.checkbox_sans_telephone, 0, 0, 0)
        sizer_criteres.Add(sizer_communication, 1, wx.EXPAND, 0)

        sizer_autre.Add(self.checkbox_ancien_adherents, 0, 0, 0)
        sizer_criteres.Add(sizer_autre, 1, wx.EXPAND, 0)

        sizer.Add(sizer_criteres, 0, wx.EXPAND, 0)

        sizer_toolbar.Add(self.bouton_ajout_adhesion, 0, wx.RIGHT, 5)
        sizer_toolbar.Add(self.bouton_ajout_credit, 0, 0, 0)
        sizer_toolbar.Add(self.static_line_1, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        sizer_toolbar.Add(self.label_recherche, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_toolbar.Add(self.text_ctrl_recherche, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_toolbar.Add(self.static_line_2, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        sizer_toolbar.Add(self.bouton_ajout_adherent, 0, 0, 0)
        sizer.Add(sizer_toolbar, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 20)

        sizer.Add(self.liste_adherents, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste(self):
        try:
            self.liste_adherents.SetObjects([a for a in Adherent.select()])
            self.liste_adherents.AutoSizeColumns()
        except BaseException as ex:
            print ex

    def OnAjoutAdhesion(self, event):
        dialog_adhesion = wx.Dialog(self, title=u"Nouvelle adhésion")
        FicheAdhesion(dialog_adhesion, adherent=self.liste_adherents.GetSelectedObject())
        dialog_adhesion.Fit()
        dialog_adhesion.ShowModal()
        dialog_adhesion.Destroy()

        if dialog_adhesion.GetReturnCode() == wx.ID_OK:
            self.liste_adherents.RefreshObject(self.liste_adherents.GetSelectedObject())
            self.liste_adherents.AutoSizeColumns()

    def OnAjoutCredit(self, event):
        print "Event handler `OnAjoutCredit' not implemented"
        event.Skip()

    def OnAjoutAdherent(self, event):
        try:
            CotisationType.select().get()

            dialog_adherent = wx.Dialog(self, title=u"Nouvel adhérent")
            fiche_adherent = FicheAdherent(dialog_adherent)
            dialog_adherent.Fit()
            dialog_adherent.ShowModal()
            dialog_adherent.Destroy()
            
            if dialog_adherent.GetReturnCode() == wx.ID_OK:
                adherent = fiche_adherent.GetAdherent()

                dialog_adhesion = wx.Dialog(self, title=u"Nouvelle adhésion")
                FicheAdhesion(dialog_adhesion, adherent=adherent)
                dialog_adhesion.Fit()
                dialog_adhesion.ShowModal()
                dialog_adhesion.Destroy()

                self.liste_adherents.AddObject(adherent)
                self.liste_adherents.AutoSizeColumns()

        except DoesNotExist:
            wx.MessageBox(u"Vous devez d'abord créer des cotisations", "Notification")

    def OnEditionAdherent(self, event):
        adherent = self.liste_adherents.GetSelectedObject()

        dialog_adherent = wx.Dialog(self, title=adherent.nom_prenom)
        FicheAdherent(dialog_adherent, adherent)
        dialog_adherent.Fit()
        dialog_adherent.ShowModal()
        dialog_adherent.Destroy()

        self.liste_adherents.RefreshObject(self.liste_adherents.GetSelectedObject())
        self.liste_adherents.AutoSizeColumns()

    def OnSelectionAdherent(self, event):
        self.bouton_ajout_adhesion.Enable()
        self.bouton_ajout_credit.Enable()

    def OnDeselectionAdherent(self, event):
        self.bouton_ajout_adhesion.Disable()
        self.bouton_ajout_credit.Disable()

    def OnClickDroitListe(self, event):
        menu = wx.Menu()

        menu.Append(1, u"Ajouter une adhésion")
        wx.EVT_MENU(menu, 1, self.OnAjoutAdhesion)

        menu.Append(2, u"Ajouter un crédit")
        wx.EVT_MENU(menu, 2, self.OnAjoutCredit)

        self.liste_adherents.PopupMenu(menu, event.GetPoint())
        menu.Destroy()

    #filtres de recherche

    def OnFilter(self, event):
        self.liste_adherents.SetFilter(Filter.Chain(*self.filtres.values()))
        self.liste_adherents.RepopulateList()
        event.Skip()

    def OnFilterNom(self, event):
        self.filtres["nom"] = Filter.TextSearch(self.liste_adherents,
                                            [self.liste_adherents.columns[0], self.liste_adherents.columns[1]],
                                            text=self.text_ctrl_recherche.GetValue())
        self.OnFilter(event)
        event.Skip()

    def OnFilterAdhesion(self, event):
        if self.radio_box_etat_adhesion.GetSelection() == 1:
            self.filtres["adhesion"] = Filter.Predicate(lambda x: x.is_adhesion_a_jour)
        elif self.radio_box_etat_adhesion.GetSelection() == 2:
            self.filtres["adhesion"] = Filter.Predicate(lambda x: not x.is_adhesion_a_jour)
        else:
            self.filtres.pop("adhesion")

        self.OnFilter(event)
        event.Skip()

    def OnFilterSansEmail(self, event):
        if self.checkbox_sans_email.IsChecked():
            self.filtres["sans_email"] = Filter.Predicate(lambda x: x.email=="")
        else:
            self.filtres.pop("sans_email")

        self.OnFilter(event)
        event.Skip()

    def OnFilterSansTelephone(self, event):
        if self.checkbox_sans_telephone.IsChecked():
            self.filtres["sans_telephone"] = Filter.Predicate(lambda x: x.telephone=="")
        else:
            self.filtres.pop("sans_telephone")

        self.OnFilter(event)
        event.Skip()

    def OnFilterUtilisateursPaniers(self, event):
        if self.checkbox_paniers.IsChecked():
            self.filtres["utilisateurs_paniers"] = Filter.Predicate(lambda x: x.utilisateur_paniers)
        else:
            self.filtres.pop("utilisateurs_paniers")

        self.OnFilter(event)
        event.Skip()

    def OnFilterAnciensAdherents(self, event):
        if self.checkbox_ancien_adherents.IsChecked():
            self.filtres["anciens_adherents"] = Filter.Predicate(lambda x: x.ancien_adherent)
        else:
            self.filtres.pop("anciens_adherents")

        self.OnFilter(event)
        event.Skip()
