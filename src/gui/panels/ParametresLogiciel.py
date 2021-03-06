#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sun Nov 21 17:24:59 2010

import wx

from gui.panels.ConfigSMTP import ConfigSMTP

class ParametresLogiciel(wx.Panel):
    def __init__(self, parent):
        # begin wxGlade: panel_GestionAsso.__init__
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL)
        
        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook_p1 = wx.Panel(self.notebook, -1)

        self.sizer_staticbox = wx.StaticBox(self, -1, u"Paramètres du logiciel")
        
        self.panel_config_smtp = ConfigSMTP(self.notebook_p1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        self.sizer_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):
        # begin wxGlade: panel_GestionAsso.__do_layout
        sizer = wx.StaticBoxSizer(self.sizer_staticbox, wx.HORIZONTAL)

        sizer_p1 = wx.BoxSizer(wx.VERTICAL)
        
        sizer_p1.Add(self.panel_config_smtp, 1, wx.ALL, 5)
        self.notebook_p1.SetSizer(sizer_p1)
        
        self.notebook.AddPage(self.notebook_p1, u"Envoi d'emails")

        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade