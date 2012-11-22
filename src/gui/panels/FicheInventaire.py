#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Inventaire, DATABASE

from lib.objectlistview import ObjectListView, ColumnDefn
from datetime import datetime

###########################################################################
## Class FicheInventaire
###########################################################################


class FicheInventaire(wx.Panel):
    def __init__(self, parent, inventaire=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)
        
        #TODO : harmoniser les fiches avec les instructions suivantes
        if inventaire:
            self.inventaire = inventaire
        else:
            self.inventaire = Inventaire(inventaire=inventaire)

        self.label_date = wx.StaticText(self, -1, u"Date de l'inventaire :")
        self.label_date_v = wx.StaticText(self, -1, "")
        self.label_commentaire = wx.StaticText(self, -1, "Commentaire")
        self.text_commentaire = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.liste_lignes_inventaire = ObjectListView(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        self.liste_lignes_inventaire.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "produit.ref_GASE", fixedWidth=90),
            ColumnDefn("Nom", "left", -1, "produit.nom"),
            ColumnDefn("Fournisseur", "left", -1, "produit.fournisseur.nom", minimumWidth=100),
            ColumnDefn(u"Stock théorique", "left", 100,
                       "stock_theorique_format",
                       stringConverter="%s", minimumWidth=100),
            ColumnDefn(u"Stock réel", "left", 100,
                       "stock_reel_format",
                       stringConverter="%s",
                       isSpaceFilling=True, minimumWidth=100)
        ])

        def RFListeProduits(listItem, ligne_inventaire):
            if ligne_inventaire.produit.retrait:
                listItem.SetTextColour("#AAAAAA")
            else:
                listItem.SetTextColour("#000000")


        self.bouton_enregistrer = wx.Button(self, wx.ID_SAVE, "Enregistrer")
        self.bouton_valider = wx.Button(self, wx.ID_OK, u"Valider l'inventaire")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnEnregistrer, self.bouton_enregistrer)
        self.Bind(wx.EVT_BUTTON, self.OnValider, self.bouton_valider)
        # end wxGlade

    def __set_properties(self):
        pass

    def __set_valeurs(self):
        if self.inventaire.get_id() != None:
            if not self.inventaire.is_valide:
                self.inventaire.date = datetime.today()
            
            self.label_date_v.SetLabel(self.inventaire.date.strftime("%d/%m/%y"))
            self.text_commentaire.SetValue(self.inventaire.commentaire)
        else:
            self.label_date_v.SetLabel(datetime.today().strftime("%d/%m/%y"))
            
    def __do_layout(self):
        # begin wxGlade: FicheInventaire.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)

        grid_sizer = wx.FlexGridSizer(5, 2, 5, 10)
        grid_sizer.Add(self.label_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.label_date_v, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.label_commentaire, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_commentaire, 0, 0, 0)

        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)

        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_enregistrer, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_valider, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_annuler, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)

        sizer.Add(sizer_bouton, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def OnEnregistrer(self, event):
        if self.Validate():
            msgbox = wx.MessageBox(u"Sauvegarder l'inventaire ?", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                date_inventaire = self.datepicker_date_inventaire.GetValue()

                self.inventaire.date = datetime(date_inventaire.GetYear(), date_inventaire.GetMonth()+1, date_inventaire.GetDay())
                self.inventaire.commentaire = self.text_commentaire.GetValue()

                with DATABASE.transaction():
                    self.inventaire.save()

                event.Skip()
                
    def OnValider(self, event):
        if self.Validate():
            msgbox = wx.MessageBox(u"Valider l'inventaire ? Il ne sera plus modifiable.", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                date_inventaire = self.datepicker_date_inventaire.GetValue()

                self.inventaire.date = datetime(date_inventaire.GetYear(), date_inventaire.GetMonth()+1, date_inventaire.GetDay())
                self.inventaire.commentaire = self.text_commentaire.GetValue()

                with DATABASE.transaction():
                    self.inventaire.save()

                event.Skip()

