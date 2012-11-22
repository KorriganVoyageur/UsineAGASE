#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import CotisationType, DATABASE
from lib.objectlistview import ObjectListView, ColumnDefn

from gui.panels.FicheCotisationType import FicheCotisationType

###########################################################################
## Class GestionCotisationTypes
###########################################################################


class GestionCotisationTypes(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)

        self.bouton_ajout_cotisation_type = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"))
        self.bouton_supprime_cotisation_type = wx.BitmapButton(self, -1, wx.Bitmap("../icons/16x16/enlever.ico"))

        self.liste_cotisation_types = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_cotisation_types.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn(u"Prix", "left", 50, "prix", stringConverter=u"%s €", isSpaceFilling=True)
        ])

        self.liste_cotisation_types.SetEmptyListMsg(u"Il n'y a aucun type de cotisation pour l'instant")

        self.__set_properties()
        self.__remplissage_liste()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutTypeCotisation, self.bouton_ajout_cotisation_type)
        self.Bind(wx.EVT_BUTTON, self.OnSupprimeTypeCotisation, self.bouton_supprime_cotisation_type)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionTypeCotisation, self.liste_cotisation_types)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectionTypeCotisation, self.liste_cotisation_types)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeselectionTypeCotisation, self.liste_cotisation_types)
        # end wxGlade

    def __set_properties(self):
        self.bouton_ajout_cotisation_type.SetToolTip(wx.ToolTip(u"Ajouter un nouveau type de cotisation"))
        self.bouton_supprime_cotisation_type.SetToolTip(wx.ToolTip(u"Supprimer le type de cotisation sélectionné"))
        self.bouton_supprime_cotisation_type.Disable()

    def __remplissage_liste(self):
        try:
            self.liste_cotisation_types.SetObjects([c for c in CotisationType.select()])
        except BaseException as ex:
            print ex

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_haut = wx.BoxSizer(wx.HORIZONTAL)
        sizer_haut.Add(self.bouton_ajout_cotisation_type, 0, 0, 0)
        sizer_haut.Add(self.bouton_supprime_cotisation_type, 0, 0, 0)
        sizer.Add(sizer_haut, 0, wx.BOTTOM|wx.EXPAND, 10)
        sizer.Add((300, -1))
        sizer.Add(self.liste_cotisation_types, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def OnSelectionTypeCotisation(self, event):
        cotisation_type = self.liste_cotisation_types.GetSelectedObject()

        if cotisation_type.adherents.count() == 0:
            self.bouton_supprime_cotisation_type.Enable()
        else:
            self.bouton_supprime_cotisation_type.Disable()

    def OnDeselectionTypeCotisation(self, event):
        self.bouton_supprime_cotisation_type.Disable()

    def OnAjoutTypeCotisation(self, event):
        dialog_cotisation_type = wx.Dialog(self, title=u"Nouveau type de cotisation")
        fiche_cotisation_type = FicheCotisationType(dialog_cotisation_type)
        dialog_cotisation_type.Fit()
        dialog_cotisation_type.ShowModal()
        dialog_cotisation_type.Destroy()

        if dialog_cotisation_type.GetReturnCode() == wx.ID_OK:
            self.liste_cotisation_types.AddObject(fiche_cotisation_type.GetTypeCotisation())
            self.liste_cotisation_types.AutoSizeColumns()

    def OnSupprimeTypeCotisation(self, event):
        cotisation_type = self.liste_cotisation_types.GetSelectedObject()

        if cotisation_type.adherents.count() == 0:
            msgbox = wx.MessageBox(u"Supprimer le type de cotisation '%s'?" % cotisation_type.nom, "Suppression", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                with DATABASE.transaction():
                    cotisation_type.delete_instance()

                self.liste_cotisation_types.RemoveObject(cotisation_type)

    def OnEditionTypeCotisation(self, event):
        cotisation_type = self.liste_cotisation_types.GetSelectedObject()

        dialog_cotisation_type = wx.Dialog(self, title=cotisation_type.nom)
        FicheCotisationType(dialog_cotisation_type, cotisation_type)
        dialog_cotisation_type.Fit()
        dialog_cotisation_type.ShowModal()
        dialog_cotisation_type.Destroy()

        if dialog_cotisation_type.GetReturnCode() == wx.ID_OK:
            self.liste_cotisation_types.RefreshObject(self.liste_cotisation_types.GetSelectedObject())
            self.liste_cotisation_types.AutoSizeColumns()
