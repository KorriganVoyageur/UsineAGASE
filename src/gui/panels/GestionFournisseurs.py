#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import os
from lib import desktop

from lib.objectlistview import ObjectListView, ColumnDefn

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors

from model.model import Fournisseur
from gui.panels.FicheFournisseur import FicheFournisseur

###########################################################################
## Class GestionFournisseurs
##########################################################################


class GestionFournisseurs(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GestionFournisseurs.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.sizer_navigation_staticbox = wx.StaticBox(self, -1, "Gestion des fournisseurs")
        self.button_ajout_fournisseur = wx.Button(self, -1, "Ajouter un nouveau fournisseur")
        self.button_tableau_fournisseur = wx.Button(self, -1, u"Générer la liste des fournisseurs")
        self.liste_fournisseurs = ObjectListView(self, -1,
                                                 style=wx.LC_REPORT|
                                                 wx.SUNKEN_BORDER|
                                                 wx.LC_SINGLE_SEL)

        self.liste_fournisseurs.SetColumns([
            ColumnDefn("Nom", "left", -1, "nom", imageGetter=self.IconeCouleurDef),
            ColumnDefn("Code postal", "center", -1, "code_postal", fixedWidth=90),
            ColumnDefn("Ville", "left", -1, "ville"),
            ColumnDefn(u"Tel fixe", "left", -1, "telephone_fixe", minimumWidth=100),
            ColumnDefn(u"Tel portable", "left", 100, "telephone_portable",
                       isSpaceFilling=True, minimumWidth=100)
        ])

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()

        self.Bind(wx.EVT_BUTTON, self.onAjoutFournisseur, self.button_ajout_fournisseur)
        self.Bind(wx.EVT_BUTTON, self.onGenereTableauFournisseur, self.button_tableau_fournisseur)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onModifFournisseur, self.liste_fournisseurs)
        # end wxGlade

    def __set_properties(self):
        self.sizer_navigation_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):
        sizer_entete = wx.StaticBoxSizer(self.sizer_navigation_staticbox, wx.HORIZONTAL)
        sizer_entete.Add(self.button_tableau_fournisseur, 0, wx.BOTTOM|wx.TOP|wx.ALIGN_LEFT, 5)
        sizer_entete.Add((1, 1), 1)
        sizer_entete.Add(self.button_ajout_fournisseur, 0, wx.BOTTOM|wx.TOP|wx.ALIGN_RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_entete, 0, wx.BOTTOM|wx.EXPAND, 10)
        sizer.Add(self.liste_fournisseurs, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def __remplissage_liste(self):
        try:
            self.liste_fournisseurs.SetObjects([f for f in Fournisseur.select()])
        except BaseException as ex:
            print ex

    def IconeCouleurDef(self, fournisseur):
        return self.liste_fournisseurs.AddImages(self.IconeCouleur16(fournisseur.couleur), self.IconeCouleur32(fournisseur.couleur))

    def IconeCouleur16(self, couleurHex):
        couleur_data = wx.Colour()
        couleur_data.SetFromString(couleurHex)
        return wx.EmptyBitmapRGBA(16, 16, couleur_data.Red(), couleur_data.Green(), couleur_data.Blue(), couleur_data.Alpha())

    def IconeCouleur32(self, couleurHex):
        couleur_data = wx.Colour()
        couleur_data.SetFromString(couleurHex)
        return wx.EmptyBitmapRGBA(32, 32, couleur_data.Red(), couleur_data.Green(), couleur_data.Blue(), couleur_data.Alpha())

    def OnAjoutFournisseur(self, event):
        dialog_fournisseur = wx.Dialog(self, title=u"Nouveau fournisseur")
        fiche_fournisseur = FicheFournisseur(dialog_fournisseur)
        dialog_fournisseur.Fit()
        dialog_fournisseur.ShowModal()
        dialog_fournisseur.Destroy()

        if dialog_fournisseur.GetReturnCode() == wx.ID_OK:
            self.liste_fournisseurs.AddObject(fiche_fournisseur.fournisseur)
            self.liste_fournisseurs.AutoSizeColumns()

    def OnModifFournisseur(self, event):
        fournisseur = self.liste_fournisseurs.GetSelectedObject()

        dialog_fournisseur = wx.Dialog(self, title=u"Fournisseur : " + fournisseur.nom)
        FicheFournisseur(dialog_fournisseur, fournisseur)
        dialog_fournisseur.Fit()
        dialog_fournisseur.ShowModal()
        dialog_fournisseur.Destroy()

        if dialog_fournisseur.GetReturnCode() == wx.ID_OK:
            self.liste_fournisseurs.RefreshObject(self.liste_fournisseurs.GetSelectedObject())
            self.liste_fournisseurs.AutoSizeColumns()

    def OnGenereTableauFournisseur(self, event):
        lst = []
        tableau = []
        tableau_style = []
        hauteurs_lignes = []

        tableau_style.append(('FONTSIZE', (0, 0), (-1, -1), 16))
        tableau_style.append(('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'))
        tableau_style.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
        tableau_style.append(('TOPPADDING', (0, 0), (-1, -1), 0))
        tableau_style.append(('BOTTOMPADDING', (0, 0), (-1, -1), 0))
        tableau_style.append(('LEADING', (0, 0), (-1, -1), 20))

        for fournisseur in self.liste_fournisseurs.GetObjects():
            tableau.append([fournisseur.nom])
            i = len(tableau)-1
            tableau_style.append(('BACKGROUND', (0, i), (1, i), fournisseur.couleur))
            tableau_style.append(('BOX', (0, i), (1, i), 1, colors.black))
            tableau_style.append(('INNERGRID', (0, i), (1, i), 1, colors.black))
            hauteurs_lignes.append(1*cm)

            #Ajout du blanc
            tableau.append([""])
            i = len(tableau)-1
            tableau_style.append(('BACKGROUND', (0, i), (1, i), colors.white))
            hauteurs_lignes.append(0.5*cm)

        tableau_fournisseurs = Table(tableau, rowHeights=hauteurs_lignes)
        tableau_fournisseurs.setStyle(TableStyle(tableau_style))

        titre_style = ParagraphStyle('Titre', alignment=TA_CENTER, leading=40,
                                     fontName='Helvetica-Bold', fontSize=20)

        lst.append(Paragraph(u"Liste des fournisseurs", titre_style))
        lst.append(tableau_fournisseurs)

        rep = os.path.dirname(os.getcwd() + "/Fournisseurs/")

        if not os.path.exists(rep):
            os.makedirs(rep)

        chemin_fichier = os.path.join(rep, "Liste des fournisseurs.pdf")

        doc = SimpleDocTemplate(chemin_fichier, title="Liste des fournisseurs",
                                pagesize=A4,
                                topMargin=2*cm,
                                bottomMargin=2*cm,
                                leftMargin=1.5*cm,
                                rightMargin=1.5*cm)

        doc.build(lst)

        '''pdfviewer = PreviewPDF(os.path.join(dir, "Liste des fournisseurs.pdf"))
        pdfviewer.ShowModal()
        pdfviewer.Destroy()   '''

        desktop.open(chemin_fichier)
