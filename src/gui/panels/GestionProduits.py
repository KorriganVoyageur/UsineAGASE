#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import os
from lib import desktop

from lib.objectlistview import ObjectListView, ColumnDefn, Filter

from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from datetime import datetime

from model.model import Produit, Fournisseur, DATABASE
from gui.panels.FicheProduit import FicheProduit

###########################################################################
## Class GestionProduits
###########################################################################


class GestionProduits(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GestionProduits.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.sizer_navigation_staticbox = wx.StaticBox(self, -1, "Gestion des produits")
        self.label_Fournisseur = wx.StaticText(self, -1, "Fournisseur :")
        self.combo_box_Fournisseur = wx.ComboBox(self, -1,
                                                 choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_RechercheNom = wx.StaticText(self, -1, "Recherche sur le nom :")
        self.text_ctrl_RechercheNom = wx.TextCtrl(self, -1, "")
        self.button_AjoutProduit = wx.Button(self, -1, "Ajouter un nouveau produit")
        self.button_ImpressionEtiquettes = wx.Button(self, -1,
                                                     u"Imprimer les étiquettes des produits cochés")
        self.liste_produits = ObjectListView(self, -1,
                                             style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)



        self.liste_produits.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "ref_GASE",
                       checkStateGetter="a_etiquetter", fixedWidth=90),
            ColumnDefn("Nom", "left", -1, "nom"),
            ColumnDefn("Fournisseur", "left", -1, "fournisseur.nom", minimumWidth=100),
            ColumnDefn("Prix de vente", "left", -1,
                       "prix_vente_format", minimumWidth=120),
            ColumnDefn("Stock", "left", 100,
                       "stock_format",
                       stringConverter="%s",
                       isSpaceFilling=True, minimumWidth=100)
        ])

        def RFListeProduits(listItem, produit):
            if produit.retrait:
                listItem.SetTextColour("#AAAAAA")
            else:
                listItem.SetTextColour("#000000")

        self.liste_produits.rowFormatter = RFListeProduits

        self.__set_properties()
        self.__do_layout()
        self.__remplissage_liste()
        self.liste_produits.SetSortColumn(0, True)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnEditionProduit, self.liste_produits)
        self.Bind(wx.EVT_COMBOBOX, self.OnFilter, self.combo_box_Fournisseur)
        self.Bind(wx.EVT_TEXT, self.OnFilter, self.text_ctrl_RechercheNom)
        self.Bind(wx.EVT_BUTTON, self.OnAjoutProduit, self.button_AjoutProduit)
        self.Bind(wx.EVT_BUTTON, self.OnImpressionEtiquettes, self.button_ImpressionEtiquettes)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GestionProduits.__set_properties
        self.sizer_navigation_staticbox.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_Fournisseur.SetMinSize((200, -1))
        self.label_Fournisseur.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.combo_box_Fournisseur.SetMinSize((200, -1))
        self.label_RechercheNom.SetMinSize((200, -1))
        self.label_RechercheNom.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_ctrl_RechercheNom.SetMinSize((200, -1))
        # end wxGlade

    def __do_layout(self):
        grid_sizer = wx.FlexGridSizer(2, 2, 4, 0)
        grid_sizer.Add(self.label_Fournisseur, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.combo_box_Fournisseur, 0, 0, 0)
        grid_sizer.Add(self.label_RechercheNom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_ctrl_RechercheNom, 0, 0, 0)

        sizer_boutons = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons.Add(self.button_AjoutProduit, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND, 5)
        sizer_boutons.Add(self.button_ImpressionEtiquettes, 0, wx.TOP|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5)

        sizer_header = wx.StaticBoxSizer(self.sizer_navigation_staticbox, wx.HORIZONTAL)
        sizer_header.Add(grid_sizer, 0, wx.TOP, 5)
        sizer_header.Add((20, 20), 1, wx.TOP|wx.EXPAND, 5)
        sizer_header.Add(sizer_boutons, 0, wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_header, 0, wx.EXPAND, 0)
        sizer.Add(self.liste_produits, 1, wx.TOP|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def __remplissage_liste(self):
        try:
            self.liste_produits.SetObjects([p for p in Produit.select()])
            self.combo_box_Fournisseur.Append("Tous", 0)

            fournisseurs = [f for f in Fournisseur.select().order_by(Fournisseur.nom.asc())]

            for fournisseur in fournisseurs:
                self.combo_box_Fournisseur.Append(fournisseur.nom, fournisseur.get_id())

            self.combo_box_Fournisseur.Select(0)

        except BaseException as ex:
            print ex

    def OnAjoutProduit(self, event):
        dialog_produit = wx.Dialog(self, title=u"Nouveau produit")
        fiche_produit = FicheProduit(dialog_produit)
        dialog_produit.Fit()
        dialog_produit.ShowModal()
        dialog_produit.Destroy()

        if dialog_produit.GetReturnCode() == wx.ID_OK:
            self.liste_produits.AddObject(fiche_produit.produit)
            self.liste_produits.AutoSizeColumns()

    def OnEditionProduit(self, event):
        produit = self.liste_produits.GetSelectedObject()

        dialog_produit = wx.Dialog(self, title=u"Produit : " + produit.nom)
        FicheProduit(dialog_produit, produit)
        dialog_produit.Fit()
        dialog_produit.ShowModal()
        dialog_produit.Destroy()

        if dialog_produit.GetReturnCode() == wx.ID_OK:
            self.liste_produits.RefreshObject(self.liste_produits.GetSelectedObject())
            self.liste_produits.AutoSizeColumns()

    def OnImpressionEtiquettes(self, event):
        lst = []
        ligne_etiquettes = []
        tableau_etiquettes = []
        tableau_style = []
        hauteurs_lignes = []

        tableau_style.append(('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
        tableau_style.append(('TOPPADDING', (0, 0), (-1, -1), 0))
        tableau_style.append(('BOTTOMPADDING', (0, 0), (-1, -1), 0))
        tableau_style.append(('LEFTPADDING', (0, 0), (-1, -1), 2))
        tableau_style.append(('RIGHTPADDING', (0, 0), (-1, -1), 2))
        tableau_style.append(('BOX', (0, 0), (-1, -1), 2, colors.black))
        tableau_style.append(('INNERGRID', (0, 0), (-1, -1), 2, colors.black))

        n_produit = 0

        ref_style = ParagraphStyle('RefProduit', alignment=TA_CENTER, leading=16, fontName='Helvetica-Bold', fontSize=14)
        nom_style = ParagraphStyle('NomProduit', alignment=TA_CENTER, leading=16, fontName='Helvetica-Bold', fontSize=12)
        prix_style = ParagraphStyle('PrixProduit', alignment=TA_CENTER, leading=16, fontName='Helvetica-Bold', fontSize=14)

        liste_produits_etiquettes = []

        for produit in self.liste_produits.GetObjects():
            if produit.a_etiquetter:
                n_produit += 1

                if n_produit%2 == 0:
                    x = 3
                else:
                    x = 0

                y = (n_produit-1)/2

                ligne_etiquettes.append(Paragraph(produit.ref_GASE(), ref_style))
                ligne_etiquettes.append(Paragraph(produit.nom, nom_style))

                ligne_etiquettes.append(Paragraph(produit.prix_vente_format(), prix_style))

                tableau_style.append(('BACKGROUND',
                                      (x, y), (x+2, y),
                                      produit.fournisseur.couleur))

                if n_produit%2 == 0:
                    tableau_etiquettes.append(ligne_etiquettes)
                    hauteurs_lignes.append(2*cm)
                    ligne_etiquettes = []

                produit.a_etiquetter = False
                liste_produits_etiquettes.append(produit)

        #Si aucun produit n'est selectionnee on ne continue pas
        if n_produit > 0:
            if n_produit%2 != 0:
                ligne_etiquettes.append("")
                ligne_etiquettes.append("")
                ligne_etiquettes.append("")
                tableau_etiquettes.append(ligne_etiquettes)
                hauteurs_lignes.append(2*cm)

            table_etiquettes = Table(tableau_etiquettes,
                                     colWidths=[2*cm, 5.5*cm, 2*cm, 2*cm, 5.5*cm, 2*cm],
                                     rowHeights=hauteurs_lignes)
            table_etiquettes.setStyle(TableStyle(tableau_style))

            lst.append(table_etiquettes)

            #Création des répertoires si ils n'existent pas
            rep = os.path.dirname(os.getcwd() + "/Etiquettes/")

            if not os.path.exists(rep):
                os.makedirs(rep)

            date_jour = datetime.now()

            chemin_fichier = os.path.join(rep, "Etiquettes - " + date_jour.strftime("%d-%m-%Y %H-%M-%S") + ".pdf")

            doc = SimpleDocTemplate(chemin_fichier, title="Etiquettes - " + date_jour.strftime("%d-%m-%Y %H-%M-%S"), pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=1.5*cm, rightMargin=1.5*cm)

            doc.build(lst)

            #session.commit()
            self.liste_produits.RefreshObjects(self.liste_produits.GetObjects())

            '''preview_pdf = PreviewPDF(chemin_fichier)
            preview_pdf.ShowModal()
            preview_pdf.Destroy()'''

            desktop.open(chemin_fichier)

            try:
                for p in liste_produits_etiquettes:
                    p.save()

                DATABASE.commit()
            except:
                DATABASE.rollback()

    def OnFilter(self, event):
        filtre_texte = Filter.TextSearch(self.liste_produits, text=self.text_ctrl_RechercheNom.GetValue())

        pk_fournisseur = self.combo_box_Fournisseur.GetClientData(self.combo_box_Fournisseur.GetSelection())

        if pk_fournisseur != 0:
            filtre_fournisseur = Filter.Predicate(lambda x: x.fournisseur.get_id() == pk_fournisseur)
            self.liste_produits.SetFilter(Filter.Chain(filtre_texte, filtre_fournisseur))
        else:
            self.liste_produits.SetFilter(filtre_texte)

        self.liste_produits.RepopulateList()
        event.Skip()
