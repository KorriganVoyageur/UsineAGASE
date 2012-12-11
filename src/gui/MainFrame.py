#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx

from panels.GestionAsso import GestionAsso
from panels.GestionAchats import GestionAchats
from panels.ParametresLogiciel import ParametresLogiciel
from panels.GestionCategories import GestionCategories
from panels.GestionCommandes import GestionCommandes
from panels.GestionFournisseurs import GestionFournisseurs
from panels.GestionInventaires import GestionInventaires
from panels.GestionProduits import GestionProduits
from panels.GestionTVAs import GestionTVAs


###########################################################################
## Class MainFrame
###########################################################################


class MainFrame(wx.Frame):

    def __init__(self, parent, title, droits=0):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=title, pos=wx.DefaultPosition,
                          size=wx.Size(980, 700),
                          style=wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.panel = wx.Panel(self)

        self.panel_boutons = wx.Panel(self.panel, wx.ID_ANY,
                                      wx.DefaultPosition, wx.DefaultSize,
                                      wx.TAB_TRAVERSAL)

        self.static_box_boutons = wx.StaticBox(self.panel_boutons, wx.ID_ANY, u"Menu")
        self.static_box_boutons.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

        sizer_boutons = wx.StaticBoxSizer(self.static_box_boutons, wx.VERTICAL)

        if droits==1:
            self.bouton_nouvel_achat = wx.Button(self.panel_boutons, 1000,
                                                 u"Nouvel achat",
                                                 wx.DefaultPosition, wx.DefaultSize,
                                                 wx.BU_LEFT|wx.NO_BORDER)
            sizer_boutons.Add(self.bouton_nouvel_achat, 0, wx.ALL|wx.EXPAND, 5)

            self.bouton_historique_achats = wx.Button(self.panel_boutons, 1001,
                                                      u"Historique des achats",
                                                      wx.DefaultPosition, wx.DefaultSize,
                                                      wx.BU_LEFT|wx.NO_BORDER)
            sizer_boutons.Add(self.bouton_historique_achats, 0, wx.ALL|wx.EXPAND, 5)

            self.bouton_mes_infos = wx.Button(self.panel_boutons, 1002,
                                              u"Mes infos",
                                              wx.DefaultPosition, wx.DefaultSize,
                                              wx.BU_LEFT|wx.NO_BORDER)
            sizer_boutons.Add(self.bouton_mes_infos, 0, wx.ALL|wx.EXPAND, 5)

            self.m_staticline3 = wx.StaticLine(self.panel_boutons,
                                               wx.ID_ANY, wx.DefaultPosition,
                                               wx.DefaultSize, wx.LI_HORIZONTAL)
            sizer_boutons.Add(self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5)

        self.bouton_gestion_association = wx.Button(self.panel_boutons, 1003,
                                                    u"Gestion de l'association",
                                                    wx.DefaultPosition, wx.DefaultSize,
                                                    wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_gestion_association, 0, wx.ALL|wx.EXPAND, 5)

        self.bouton_parametres_logiciel = wx.Button(self.panel_boutons, 1004,
                                                    u"Paramètres du logiciel",
                                                    wx.DefaultPosition, wx.DefaultSize,
                                                    wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_parametres_logiciel, 0, wx.ALL|wx.EXPAND, 5)

        self.m_staticline2 = wx.StaticLine(self.panel_boutons,
                                           wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_boutons.Add(self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5)

        self.bouton_gestion_categories = wx.Button(self.panel_boutons, 1005,
                                                   u"Gestion des catégories",
                                                   wx.DefaultPosition, wx.DefaultSize,
                                                   wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_gestion_categories, 0, wx.ALL|wx.EXPAND, 5)

        self.bouton_gestion_tvas = wx.Button(self.panel_boutons, 1009,
                                                   u"Gestion des taux de TVA",
                                                   wx.DefaultPosition, wx.DefaultSize,
                                                   wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_gestion_tvas, 0, wx.ALL|wx.EXPAND, 5)

        self.bouton_gestion_fournisseurs = wx.Button(self.panel_boutons, 1006,
                                                     u"Gestion des fournisseurs",
                                                     wx.DefaultPosition, wx.DefaultSize,
                                                     wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_gestion_fournisseurs, 0, wx.ALL|wx.EXPAND, 5)

        self.bouton_gestion_produits = wx.Button(self.panel_boutons, 1007,
                                                 u"Gestion des produits",
                                                 wx.DefaultPosition, wx.DefaultSize,
                                                 wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_gestion_produits, 0, wx.ALL|wx.EXPAND, 5)

        self.m_staticline1 = wx.StaticLine(self.panel_boutons,
                                           wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_boutons.Add(self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5)

        self.bouton_suivi_commandes = wx.Button(self.panel_boutons, 1008,
                                                u"Gestion des commandes",
                                                wx.DefaultPosition, wx.DefaultSize,
                                                wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_suivi_commandes, 0, wx.ALL|wx.EXPAND, 5)
        
        self.m_staticline3 = wx.StaticLine(self.panel_boutons,
                                           wx.ID_ANY, wx.DefaultPosition,
                                           wx.DefaultSize, wx.LI_HORIZONTAL)
        sizer_boutons.Add(self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5)

        self.bouton_gestion_inventaires = wx.Button(self.panel_boutons, 1010,
                                                   u"Gestion des inventaires",
                                                   wx.DefaultPosition, wx.DefaultSize,
                                                   wx.BU_LEFT|wx.NO_BORDER)
        sizer_boutons.Add(self.bouton_gestion_inventaires, 0, wx.ALL|wx.EXPAND, 5)

        self.panel_boutons.SetSizer(sizer_boutons)
        self.panel_boutons.Layout()
        sizer_boutons.Fit(self.panel_boutons)

        self.panel_principal = wx.Panel(self.panel, 10, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        #self.panel_principal =  wx.ScrolledWindow(self.panel, style=wx.HSCROLL|wx.VSCROLL)
        #self.panel_principal.SetScrollRate( 5, 5 )

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(self.panel_boutons, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.panel_principal, 1, wx.ALL|wx.EXPAND, 5)

        self.panel.SetSizer(sizer)
        self.panel.Layout()
        sizer.Fit(self.panel)

        self.Maximize()

        # Connect Events
        if droits == 1:
            self.bouton_nouvel_achat.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
            self.bouton_historique_achats.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
            self.bouton_mes_infos.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)

        self.bouton_gestion_association.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
        self.bouton_parametres_logiciel.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)

        self.bouton_gestion_categories.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
        self.bouton_gestion_tvas.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
        self.bouton_gestion_fournisseurs.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
        self.bouton_gestion_produits.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
        self.bouton_suivi_commandes.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)
        self.bouton_gestion_inventaires.Bind(wx.EVT_BUTTON, self.OnBoutonMenu)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnBoutonMenu(self, event):
        event_id = event.GetId()

        global PARAMETRES_ASSOCIATION

        if event_id == 1000:
            pass
            #self.SetPanelPrincipal(GestionCategories(self))
        elif event_id == 1001:
            pass
            self.SetPanelPrincipal(GestionAchats)
        elif event_id == 1003:
            self.SetPanelPrincipal(GestionAsso)
        elif event_id == 1004:
            self.SetPanelPrincipal(ParametresLogiciel)
        elif event_id == 1005:
            self.SetPanelPrincipal(GestionCategories)
        elif event_id == 1009:
            self.SetPanelPrincipal(GestionTVAs)
        elif event_id == 1006:
            self.SetPanelPrincipal(GestionFournisseurs)
        elif event_id == 1007:
            self.SetPanelPrincipal(GestionProduits)
        elif event_id == 1008:
            self.SetPanelPrincipal(GestionCommandes)
        elif event_id == 1010:
            self.SetPanelPrincipal(GestionInventaires)

        event.Skip()

    def SetPanelPrincipal(self, panel, session_close=True, **args):
        wx.BeginBusyCursor()
        self.Freeze()

        self.panel_principal.DestroyChildren()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel(self.panel_principal, **args), 1, wx.EXPAND)
        self.panel_principal.SetSizer(sizer)
        self.panel_principal.Fit()
        self.panel.Layout()

        self.Thaw()
        wx.EndBusyCursor()
