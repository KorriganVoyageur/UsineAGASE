#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Adhesion, DATABASE
from lib.objectlistview import ObjectListView, ColumnDefn
from gui.panels.FicheAdhesion import FicheAdhesion

###########################################################################
## Class GestionAdhesions
###########################################################################


class GestionAdhesions(wx.Panel):
    def __init__(self, parent, adherent=None):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        
        self.adherent = adherent

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

    def __do_layout(self):
        sizer_entete = wx.BoxSizer(wx.HORIZONTAL)
        sizer_entete.Add(self.bouton_ajout_adhesion, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)
        sizer_entete.Add((10, 10))
        sizer_entete.Add(self.bouton_supprime_adhesion, 0, wx.BOTTOM | wx.TOP | wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_entete, 0, wx.BOTTOM | wx.ALIGN_RIGHT | wx.EXPAND, 10)
        sizer.Add(self.liste_adhesions, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def __remplissage_liste(self):
        try:
            if self.adherent:
                self.liste_adhesions.SetObjects([a for a in self.adherent.adhesions])
            else:
                self.liste_adhesions.SetObjects([a for a in Adhesion.select()])
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
