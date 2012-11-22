#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from lib.objectlistview import ObjectListView, ColumnDefn
from gui.panels.FicheAdhesionType import FicheAdhesionType
from model.model import AdhesionType, DATABASE

###########################################################################
## Class GestionAdhesionTypes
###########################################################################


class GestionAdhesionTypes(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        self.bouton_ajout_adhesion_type = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.bouton_supprime_adhesion_type = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))

        self.liste_adhesion_types = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_adhesion_types.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn(u"Prix", "left", 50, "prix", stringConverter=u"%s €", isSpaceFilling=True)
        ])

        self.liste_adhesion_types.SetEmptyListMsg(u"Il n'y a aucun type d'adhésion pour l'instant")

        self.__set_properties()
        self.__remplissage_liste()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutTypeAdhesion, self.bouton_ajout_adhesion_type)
        self.Bind(wx.EVT_BUTTON, self.OnSupprimeTypeAdhesion, self.bouton_supprime_adhesion_type)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionTypeAdhesion, self.liste_adhesion_types)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionTypeAdhesion, self.liste_adhesion_types)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeselectionTypeAdhesion, self.liste_adhesion_types)

    def __set_properties(self):
        self.bouton_ajout_adhesion_type.SetToolTip(wx.ToolTip(u"Ajouter un nouveau type d'adhésion"))
        self.bouton_supprime_adhesion_type.SetToolTip(wx.ToolTip(u"Supprimer le type d'adhésion sélectionné"))
        self.bouton_supprime_adhesion_type.Disable()

    def __remplissage_liste(self):
        try:
            self.liste_adhesion_types.SetObjects([a for a in AdhesionType.select()])
        except BaseException as ex:
            print ex

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_haut = wx.BoxSizer(wx.HORIZONTAL)
        sizer_haut.Add(self.bouton_ajout_adhesion_type, 0, 0, 0)
        sizer_haut.Add(self.bouton_supprime_adhesion_type, 0, 0, 0)
        sizer.Add(sizer_haut, 0, wx.BOTTOM|wx.EXPAND, 10)
        sizer.Add((300, -1))
        sizer.Add(self.liste_adhesion_types, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def OnAjoutTypeAdhesion(self, event):
        dialog_adhesion_type = wx.Dialog(self, title=u"Nouveau type d'adhésion")
        fiche_adhesion_type = FicheAdhesionType(dialog_adhesion_type)
        dialog_adhesion_type.Fit()
        dialog_adhesion_type.ShowModal()
        dialog_adhesion_type.Destroy()

        if dialog_adhesion_type.GetReturnCode() == wx.ID_OK:
            self.liste_adhesion_types.AddObject(fiche_adhesion_type.GetTypeAdhesion())
            self.liste_adhesion_types.AutoSizeColumns()

    def OnSupprimeTypeAdhesion(self, event):
        adhesion_type = self.liste_adhesion_types.GetSelectedObject()

        if adhesion_type.adhesions.count() == 0:
            msgbox = wx.MessageBox(u"Supprimer le type d'adhésion '%s'?" % adhesion_type.nom, "Suppression", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                with DATABASE.transaction():
                    adhesion_type.delete_instance()

                self.liste_adhesion_types.RemoveObject(adhesion_type)

    def OnSelectionTypeAdhesion(self, event):
        adhesion_type = self.liste_adhesion_types.GetSelectedObject()

        if adhesion_type.adhesions.count() == 0:
            self.bouton_supprime_adhesion_type.Enable()
        else:
            self.bouton_supprime_adhesion_type.Disable()

    def OnDeselectionTypeAdhesion(self, event):
        self.bouton_supprime_adhesion_type.Disable()

    def OnEditionTypeAdhesion(self, event):
        adhesion_type = self.liste_adhesion_types.GetSelectedObject()

        dialog_adhesion_type = wx.Dialog(self, title=adhesion_type.nom)
        FicheAdhesionType(dialog_adhesion_type, adhesion_type)
        dialog_adhesion_type.Fit()
        dialog_adhesion_type.ShowModal()
        dialog_adhesion_type.Destroy()

        if dialog_adhesion_type.GetReturnCode() == wx.ID_OK:
            self.liste_adhesion_types.RefreshObject(self.liste_adhesion_types.GetSelectedObject())
            self.liste_adhesion_types.AutoSizeColumns()
