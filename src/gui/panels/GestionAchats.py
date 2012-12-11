#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from model.model import Adherent, Achat, LigneAchat, Credit, Cotisation, DATABASE
from gui.panels.FicheAchat import FicheAchat
from lib.objectlistview import ObjectListView, ColumnDefn
from datetime import datetime


class GestionAchats(wx.Panel):
    def __init__(self, parent, adherent=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)
        
        if adherent:
            self.adherent = adherent
        else:
            self.adherent = Adherent.select().where(Adherent.id == 1).get()

        self.label_total_achats = wx.StaticText(self, -1, "Total des achats du mois en cours :")
        self.label_total_achats_v = wx.StaticText(self, -1, u"XX.XX €")
        self.label_credit = wx.StaticText(self, -1, u"Crédit :")
        self.label_credit_v = wx.StaticText(self, -1, u"XX.XX €")
        self.static_line = wx.StaticLine(self, -1)
        self.bouton_ajout_achat = wx.Button(self, -1, "Nouvel achat")
        self.bouton_ajout_credit = wx.Button(self, -1, "Nouveau paiement")
        self.label_info = wx.StaticText(self, -1, u"Note : Le dernier achat et le dernier paiement sont modifiable le jour même.")

        self.notebook_achats = wx.Notebook(self, -1, style=0)

        #Page "Dernieres produits achetés"
        self.panel_page_achat_mois = wx.Panel(self.notebook_achats, -1)
        self.search_nom = wx.SearchCtrl(self.panel_page_achat_mois, -1, "")
        self.label_date_recherche = wx.StaticText(self.panel_page_achat_mois, -1, u"Afficher les produits achetés depuis le :")
        self.datepicker_date_max = wx.DatePickerCtrl(self.panel_page_achat_mois, -1)
        self.liste_achats_mois = ObjectListView(self.panel_page_achat_mois, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_achats_mois.SetColumns([
            ColumnDefn("Date", "center", -1, "achat.date", stringConverter="%d-%m-%y", minimumWidth=70),
            ColumnDefn("Ref GASE", "center", -1, "produit.ref_GASE", minimumWidth=70),
            ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=100),
            ColumnDefn("Prix", "left", -1, "produit.prix_vente_format", minimumWidth=100),
            ColumnDefn(u"Quantité", "left", -1, "quantite_format", minimumWidth=70),
            ColumnDefn(u"Total", "right", -1, "prix_total", stringConverter=u"%.2f €", minimumWidth=70, isSpaceFilling=True)
        ])
        
        self.liste_achats_mois.AutoSizeColumns()

        self.notebook_achats.AddPage(self.panel_page_achat_mois, u"Achats du mois")

        #Page "Achats"
        self.panel_page_achats = wx.Panel(self.notebook_achats, -1)

        self.liste_achats =  ObjectListView(self.panel_page_achats, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)
        
        self.liste_achats.SetColumns([
            ColumnDefn("Date", "left", -1, "date", stringConverter="Achat du %d-%m-%y", minimumWidth=100),
            ColumnDefn(u"Total", "right", -1, "total", stringConverter=u"%.2f €", minimumWidth=100, isSpaceFilling=True)
        ])

        self.liste_achats.AutoSizeColumns()

        self.liste_lignes_achat = ObjectListView(self.panel_page_achats, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_lignes_achat.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "produit.ref_GASE", minimumWidth=70),
            ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=100),
            ColumnDefn("Prix", "left", -1, "produit.prix_vente_format", minimumWidth=100),
            ColumnDefn(u"Quantité", "left", -1, "quantite_format", minimumWidth=70),
            ColumnDefn(u"Total", "right", -1, "prix_total", stringConverter=u"%.2f €", minimumWidth=70, isSpaceFilling=True)
        ])

        self.liste_lignes_achat.AutoSizeColumns()
        self.liste_lignes_achat.SortBy(1)

        self.notebook_achats.AddPage(self.panel_page_achats, "Achats")

        #Page "Paiements"
        self.panel_page_credits = wx.Panel(self.notebook_achats, -1)
        self.liste_credits = wx.ListCtrl(self.panel_page_credits, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        
        self.notebook_achats.AddPage(self.panel_page_credits, "Paiements")


        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.search_nom.Bind(wx.EVT_TEXT, self.OnRechercheNom)
        self.datepicker_date_max.Bind(wx.EVT_DATE_CHANGED, self.OnRechercheDate)
        self.bouton_ajout_achat.Bind(wx.EVT_BUTTON, self.OnAjoutAchat)
        self.liste_achats.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDetailsAchat)

    def __set_properties(self):
        self.search_nom.SetMinSize((200, -1))
        self.search_nom.SetDescriptiveText("Recherche sur le nom")

    def __set_valeurs(self):
        try:
            date_mois = datetime(datetime.today().year, datetime.today().month, 1)
            print date_mois
            lignes_achat = LigneAchat.select().join(Achat).where((Achat.adherent == self.adherent) and
                                                                 (Achat.date >= date_mois)).order_by(Achat.date.desc())            
            self.liste_achats_mois.SetObjects([la for la in lignes_achat])

            achats = Achat.select().where(Achat.adherent == self.adherent).order_by(Achat.date.desc())            
            self.liste_achats.SetObjects([a for a in achats])

        except BaseException as ex:
            print ex

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_panel_page_credits = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel_page_achats = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel_page_achat_mois = wx.BoxSizer(wx.VERTICAL)
        sizer_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)

        grid_infos = wx.GridSizer(2, 2, 5, 5)
        grid_infos.Add(self.label_total_achats, 0, 0, 0)
        grid_infos.Add(self.label_total_achats_v, 0, 0, 0)
        grid_infos.Add(self.label_credit, 0, 0, 0)
        grid_infos.Add(self.label_credit_v, 0, 0, 0)

        sizer.Add(grid_infos, 0, wx.ALL, 5)
        sizer.Add(self.static_line, 0, wx.ALL | wx.EXPAND, 10)

        sizer_boutons.Add(self.bouton_ajout_achat, 0, 0, 0)
        sizer_boutons.Add(self.bouton_ajout_credit, 0, wx.LEFT, 20)

        sizer.Add(sizer_boutons, 0, wx.EXPAND, 0)
        sizer.Add(self.label_info, 0, wx.ALL, 5)

        sizer_toolbar.Add(self.search_nom, 0, wx.RIGHT, 10)
        sizer_toolbar.Add(self.label_date_recherche, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_toolbar.Add(self.datepicker_date_max, 0, 0, 0)

        sizer_panel_page_achat_mois.Add(sizer_toolbar, 0, wx.ALL | wx.EXPAND, 5)
        sizer_panel_page_achat_mois.Add(self.liste_achats_mois, 1, wx.ALL | wx.EXPAND, 5)

        self.panel_page_achat_mois.SetSizer(sizer_panel_page_achat_mois)

        sizer_panel_page_achats.Add(self.liste_achats, 1, wx.ALL | wx.EXPAND, 5)
        sizer_panel_page_achats.Add(self.liste_lignes_achat, 2, wx.ALL | wx.EXPAND, 5)

        self.panel_page_achats.SetSizer(sizer_panel_page_achats)

        sizer_panel_page_credits.Add(self.liste_credits, 1, wx.ALL | wx.EXPAND, 5)
        self.panel_page_credits.SetSizer(sizer_panel_page_credits)

        sizer.Add(self.notebook_achats, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def OnAjoutAchat(self, event):
        self.Hide()

        fiche_achat = FicheAchat(self.GetParent())

        sizer = self.GetParent().GetSizer()
        sizer.Add(fiche_achat, 1, wx.EXPAND)
        self.GetParent().SetSizer(sizer)
        self.GetParent().Layout()
        
    def OnDetailsAchat(self, event):
        self.achat = self.liste_achats.GetSelectedObject()
        self.liste_lignes_achat.SetObjects([la for la in self.achat.lignes_achat])

    def OnRechercheNom(self, event):
        print "Event handler `OnRechercheNom' not implemented!"
        event.Skip()

    def OnRechercheDate(self, event):
        print "Event handler `OnRechercheDate' not implemented!"
        event.Skip()

