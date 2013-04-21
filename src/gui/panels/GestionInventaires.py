#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Inventaire, LigneInventaire, DATABASE
from lib.objectlistview import ObjectListView, ColumnDefn
from gui.panels.FicheInventaire import FicheInventaire

###########################################################################
## Class GestionInventaires
###########################################################################


class GestionInventaires(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        
        self.sizer_navigation_staticbox = wx.StaticBox(self, -1, "Gestion des inventaires")
        self.bouton_ajout_inventaire = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.bouton_suppression_inventaire = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))
        self.liste_inventaires = ObjectListView(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        def is_valide(value):
            if value:
                return u"Validé"
            else:
                return "En cours de validation"

        self.liste_inventaires.SetColumns([
            ColumnDefn("Date", "left", 200, "date", stringConverter="Inventaire du %d-%m-%Y", minimumWidth=200),
            ColumnDefn("Statut", "left", -1, "is_valide", stringConverter=is_valide),
            ColumnDefn(u"Valeur du stock théorique", "left", 100, "valeur_stock_theorique", stringConverter=u"%.2f €"),
            ColumnDefn(u"Valeur du stock réel", "left", 100, "valeur_stock_reel", stringConverter=u"%.2f €", isSpaceFilling=True)
        ])

        def rowFormatterLI(listItem, commande):
            if commande.is_valide == 0:
                #C5CBFF
                listItem.SetBackgroundColour("#FBFCC8")
            elif commande.is_valide == 1:
                #FFA3A2
                listItem.SetBackgroundColour("#E3FFCB")

        self.liste_inventaires.rowFormatter = rowFormatterLI

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutInventaire, self.bouton_ajout_inventaire)
        self.Bind(wx.EVT_BUTTON, self.OnSuppressionInventaire, self.bouton_suppression_inventaire)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionInventaire, self.liste_inventaires)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionInventaire, self.liste_inventaires)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelectionInventaire, self.liste_inventaires)
        # end wxGlade

    def __set_properties(self):
        self.sizer_navigation_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.bouton_ajout_inventaire.SetToolTip(wx.ToolTip(u"Faire un nouvel inventaire"))
        self.bouton_suppression_inventaire.SetToolTip(wx.ToolTip(u"Supprimer l'inventaire sélectionné"))
        self.bouton_suppression_inventaire.Disable()

    def __do_layout(self):
        sizer_entete = wx.StaticBoxSizer(self.sizer_navigation_staticbox, wx.HORIZONTAL)
        sizer_entete.Add(self.bouton_ajout_inventaire, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)
        sizer_entete.Add((10, 10))
        sizer_entete.Add(self.bouton_suppression_inventaire, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_entete, 0, wx.BOTTOM | wx.ALIGN_RIGHT | wx.EXPAND, 10)
        sizer.Add(self.liste_inventaires, 1, wx.EXPAND)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def __remplissage_liste(self):
        try:
            self.liste_inventaires.SetObjects([i for i in Inventaire.select()])
        except BaseException as ex:
            print ex

    def OnSelectionInventaire(self, event):
        if self.liste_inventaires.GetSelectedObject():
            self.bouton_suppression_inventaire.Enable()
        else:
            self.bouton_suppression_inventaire.Disable()

    def OnAjoutInventaire(self, event):
        self.Hide()
        
        fiche_inventaire = FicheInventaire(self.GetParent())

        sizer = self.GetParent().GetSizer()
        sizer.Add(fiche_inventaire, 1, wx.EXPAND)
        self.GetParent().SetSizer(sizer)
        self.GetParent().Layout()
                
    def OnSuppressionInventaire(self, event):
        inventaire = self.liste_inventaires.GetSelectedObject()

        msgbox = wx.MessageBox(u"Supprimer l'inventaire du %s ?" % inventaire.date.strftime("%d/%m/%y"), "Suppression", wx.YES_NO | wx.ICON_QUESTION)

        if msgbox == wx.YES:
            with DATABASE.transaction():
                inventaire.delete_instance(recursive=True)

            self.liste_inventaires.RemoveObject(inventaire)

    def OnEditionInventaire(self, event):
        inventaire = self.liste_inventaires.GetSelectedObject()
        
        self.Hide()
        
        fiche_inventaire = FicheInventaire(self.GetParent(), inventaire=inventaire)

        sizer = self.GetParent().GetSizer()
        sizer.Add(fiche_inventaire, 1, wx.EXPAND)
        self.GetParent().SetSizer(sizer)
        self.GetParent().Layout()

        '''if dialog_inventaire.GetReturnCode() == wx.ID_OK:
            self.liste_inventaires.RefreshObject(self.liste_inventaires.GetSelectedObject())
            self.liste_inventaires.AutoSizeColumns()'''
