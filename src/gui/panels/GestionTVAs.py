#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Tva
from lib.objectlistview import ObjectListView, ColumnDefn
from gui.panels.FicheTVA import FicheTVA

###########################################################################
## Class GestionTvas
###########################################################################


class GestionTVAs(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GestionTvas.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.sizer_navigation_staticbox = wx.StaticBox(self, -1,
                                                       u"Gestion des taux de TVA")
        self.button_ajout_tva = wx.Button(self, -1,
                                                u"Ajouter un nouveau taux de TVA")
        self.liste_tvas = ObjectListView(self, -1,
                                               style=wx.LC_REPORT |
                                                     wx.SUNKEN_BORDER |
                                                     wx.LC_SINGLE_SEL)

        self.liste_tvas.SetColumns([
            ColumnDefn("Taux", "center", -1, "taux", stringConverter="%s %%", fixedWidth=70),
            ColumnDefn("Nombre de produits avec ce taux", "left", 100,
                       "nombre_produits",
                       stringConverter="%s produit(s)",
                       isSpaceFilling=True)
        ])

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.OnAjoutTVA,
                  self.button_ajout_tva)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnModifTVA,
                  self.liste_tvas)
        # end wxGlade

    def __set_properties(self):
        self.sizer_navigation_staticbox.SetFont(wx.Font(14,
                                                        wx.DEFAULT,
                                                        wx.NORMAL,
                                                        wx.BOLD,
                                                        0, ""))

    def __do_layout(self):
        # begin wxGlade: GestionTvas.__do_layout
        sizer_entete = wx.StaticBoxSizer(self.sizer_navigation_staticbox,
                                         wx.HORIZONTAL)
        sizer_entete.Add((1, 1), 1)
        sizer_entete.Add(self.button_ajout_tva, 0,
                         wx.BOTTOM |
                         wx.TOP |
                         wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_entete, 0,
                  wx.BOTTOM |
                  wx.ALIGN_RIGHT |
                  wx.EXPAND, 10)
        sizer.Add(self.liste_tvas, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste(self):
        try:
            self.liste_tvas.SetObjects([t for t in Tva.select()])
        except BaseException as ex:
            print ex

    def OnAjoutTVA(self, event):
        dialog_tva = wx.Dialog(self, title=u"Nouveau taux de TVA")
        fiche_tva = FicheTVA(dialog_tva)
        dialog_tva.Fit()
        dialog_tva.ShowModal()
        dialog_tva.Destroy()

        if dialog_tva.GetReturnCode() == wx.ID_OK:
            self.liste_tvas.AddObject(fiche_tva.tva)
            self.liste_tvas.AutoSizeColumns()

    def OnModifTVA(self, event):
        tva = self.liste_tvas.GetSelectedObject()

        dialog_tva = wx.Dialog(self,
                                     title=u"TVA à " + str(tva.taux) + u" %")
        FicheTVA(dialog_tva, tva)
        dialog_tva.Fit()
        dialog_tva.ShowModal()
        dialog_tva.Destroy()

        if dialog_tva.GetReturnCode() == wx.ID_OK:
            self.liste_tvas.RefreshObject(
                                  self.liste_tvas.GetSelectedObject())
            self.liste_tvas.AutoSizeColumns()
