#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import pdfviewer

###########################################################################
## Class PreviewPDF
##########################################################################

class PreviewPDF(wx.Dialog):
    def __init__(self, chemin, pos=wx.DefaultPosition, size=(480,640), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER):
        # begin wxGlade: FicheCategorie.__init__
        #kwds["style"] = wx.DEFAULT_DIALOG_STYLE

        wx.Dialog.__init__(self, None, -1, "", pos, None, style)

        self.panel = wx.Panel(self)
        self.pdf_viewer = pdfviewer.pdfViewer(self.panel, wx.ID_ANY, (0,0), (10,10), 0)
        self.panneau_boutons = pdfviewer.pdfButtonPanel(self.panel, wx.ID_ANY, None, None, 0)
        
        self.pdf_viewer.buttonpanel = self.panneau_boutons
        self.panneau_boutons.viewer = self.pdf_viewer
       
        self.pdf_viewer.LoadFile(chemin)
        
        self.pdf_viewer.SetZoom(1.0)
        
        # begin wxGlade: ChoixQuantiteDialog.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panneau_boutons, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.pdf_viewer, 1, wx.EXPAND|wx.TOP, 5)

        self.panel.SetSizer(sizer)
        sizer.Fit(self.panel)
        
        self.Layout()
        
        self.Maximize()
        # end wxGlade