#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from peewee import fn
from model.model import Produit, Categorie, Fournisseur, Tva, DATABASE
from classes.Validators import GenericTextValidator, VALIDATE_INT, VALIDATE_FLOAT

###########################################################################
## Class FicheProduit
###########################################################################


class FicheProduit(wx.Panel):
    def __init__(self, parent, produit=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if produit == None:
            produit = Produit.create()

        self.produit = produit

        self.label_Nom = wx.StaticText(self, -1, "Nom :")
        self.text_Nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_RefGASE = wx.StaticText(self, -1, "Ref GASE :")
        self.label_RefGASEV = wx.StaticText(self, -1, "XX-XXX")
        self.label_Categorie = wx.StaticText(self, -1, u"Catégorie :")
        self.combo_box_Categorie = wx.ComboBox(self, -1, choices=[],
                                               style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_CategorieV = wx.StaticText(self, -1, "XXXXXX")
        self.label_Fournisseur = wx.StaticText(self, -1, "Fournisseur :")
        self.combo_box_Fournisseur = wx.ComboBox(self, -1, choices=[],
                                                 style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_RefFournisseur = wx.StaticText(self, -1, "Ref fourniseur :")
        self.text_RefFournisseur = wx.TextCtrl(self, -1, "")
        self.label_Origine = wx.StaticText(self, -1, "Origine :")
        self.text_Origine = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_TypeVente = wx.StaticText(self, -1, "Type de vente :")
        self.radio_box_TypeVente = wx.RadioBox(self, -1, "",
                                                     choices=[u"Conditionné", "Vrac"],
                                                     majorDimension=2,
                                                     style=wx.RA_SPECIFY_COLS)
        self.label_UniteMesure = wx.StaticText(self, -1, u"Unité de mesure :")
        self.radio_box_UniteMesure = wx.RadioBox(self, -1, "",
                                                 choices=["Poids", "Volume"],
                                                 majorDimension=2,
                                                 style=wx.RA_SPECIFY_COLS)
        self.label_PoidsVolume = wx.StaticText(self, -1, "Poids :")
        self.text_PoidsVolume = wx.TextCtrl(self, -1, "",
                                            validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_GrL = wx.StaticText(self, -1, "grammes")
        self.label_Conditionnement = wx.StaticText(self, -1, u"Conditionnement :")
        self.text_Conditionnement = wx.TextCtrl(self, -1, "",
                                                validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_UniteSacBidon = wx.StaticText(self, -1, u"unité(s)")
        self.label_TVA = wx.StaticText(self, -1, "TVA :")
        self.combo_box_TVA = wx.ComboBox(self, -1, choices=[],
                                         style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_PrixAchat = wx.StaticText(self, -1, "Prix d'achat HT :")
        self.text_PrixAchat = wx.TextCtrl(self, -1, "",
                                          validator=GenericTextValidator(flag=VALIDATE_FLOAT))
        self.label_PrixUniteSacBidon = wx.StaticText(self, -1, u"€ par unité")
        self.label_RetraitProduit = wx.StaticText(self, -1, "Retirer le produit ? :")
        self.checkbox_RetraitProduit = wx.CheckBox(self, -1, "")
        self.label_MotifRetrait = wx.StaticText(self, -1, "Motif du retrait:")
        self.text_MotifRetrait = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.button_ok = wx.Button(self, wx.ID_OK, "Valider")
        self.button_annuler = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_comboboxs()
        self.__set_valeurs()

        self.__set_properties()
        self.__set_tooltips()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.OnChoixCategorie, self.combo_box_Categorie)
        self.Bind(wx.EVT_RADIOBOX, self.OnDefLabelsUnites, self.radio_box_TypeVente)
        self.Bind(wx.EVT_RADIOBOX, self.OnDefLabelsUnites, self.radio_box_UniteMesure)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickRetrait, self.checkbox_RetraitProduit)
        self.Bind(wx.EVT_BUTTON, self.OnEnregistre, self.button_ok)

        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.button_annuler)
        # end wxGlade

    def __set_properties(self):
        self.text_Nom.SetMinSize((300, -1))
        self.text_PoidsVolume.SetMinSize((70, -1))
        self.text_Conditionnement.SetMinSize((70, -1))
        self.combo_box_TVA.SetMinSize((70, -1))
        self.text_PrixAchat.SetMinSize((70, -1))
        self.text_MotifRetrait.SetMinSize((-1, 87))
        self.text_MotifRetrait.Enable(False)
        # end wxGlade

    def __set_tooltips(self):
        #TODO: tooltips à faire
        self.text_Conditionnement.SetToolTip(wx.ToolTip(u"Défini par combien le fournisseur vend ce produit. Exemple : carton de 6, sac ou bidon à l'unité"))

    def __do_layout(self):
        # begin wxGlade: FicheProduit.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(14, 2, 6, 10)
        #grid_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        sizer_PrixAchat = wx.BoxSizer(wx.HORIZONTAL)
        sizer_UnitesParCarton = wx.BoxSizer(wx.HORIZONTAL)
        sizer_PoidsVolume = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Categorie = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer.Add(self.label_Nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Nom, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_RefGASE, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5)
        grid_sizer.Add(self.label_RefGASEV, 0, wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 5)
        grid_sizer.Add(self.label_Categorie, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_Categorie.Add(self.combo_box_Categorie, 1, wx.EXPAND, 0)
        sizer_Categorie.Add(self.label_CategorieV, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(sizer_Categorie, 1, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Fournisseur, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.combo_box_Fournisseur, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_RefFournisseur, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_RefFournisseur, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Origine, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_Origine, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_TypeVente, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.radio_box_TypeVente, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.label_UniteMesure, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.radio_box_UniteMesure, 0, wx.EXPAND, 0)
        grid_sizer.Add(self.label_PoidsVolume, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_PoidsVolume.Add(self.text_PoidsVolume, 0, 0, 0)
        sizer_PoidsVolume.Add(self.label_GrL, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer.Add(sizer_PoidsVolume, 1, wx.EXPAND, 0)
        grid_sizer.Add(self.label_Conditionnement, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_UnitesParCarton.Add(self.text_Conditionnement, 0, 0, 0)
        sizer_UnitesParCarton.Add(self.label_UniteSacBidon, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer.Add(sizer_UnitesParCarton, 1, wx.EXPAND, 0)
        grid_sizer.Add(self.label_TVA, 0, 0, 0)
        grid_sizer.Add(self.combo_box_TVA, 0, 0, 0)
        grid_sizer.Add(self.label_PrixAchat, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_PrixAchat.Add(self.text_PrixAchat, 0, 0, 0)
        sizer_PrixAchat.Add(self.label_PrixUniteSacBidon, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer.Add(sizer_PrixAchat, 1, wx.EXPAND, 0)
        grid_sizer.Add(self.label_RetraitProduit, 0, wx.TOP|wx.BOTTOM, 3)
        grid_sizer.Add(self.checkbox_RetraitProduit, 0, wx.TOP, 4)
        grid_sizer.Add(self.label_MotifRetrait, 0, wx.TOP, 3)
        grid_sizer.Add(self.text_MotifRetrait, 0, wx.EXPAND, 0)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_ok, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.button_annuler, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.Fit()
        self.Layout()
        # end wxGlade

    def __set_comboboxs(self):
        #TODO: Faire système de verification en cas de non existance de fournisseur/categorie/tva
        try:
            categories = [c for c in Categorie.select().order_by(Categorie.nom.asc())]
            for c in categories:
                self.combo_box_Categorie.Append(str(c.get_id()).zfill(2) + " - " + c.nom, c)

            fournisseurs = [f for f in Fournisseur.select().order_by(Fournisseur.nom.asc())]
            for fournisseur in fournisseurs:
                self.combo_box_Fournisseur.Append(fournisseur.nom, fournisseur)

            tvas = [t for t in Tva.select().order_by(Tva.taux.asc())]
            for tva in tvas:
                self.combo_box_TVA.Append(str(tva.taux), tva)

        except BaseException as ex:
            print ex

    def __set_valeurs(self):
        if self.produit.get_id() != None:
            self.text_Nom.SetValue(self.produit.nom)
            self.label_RefGASEV.SetLabel(self.produit.ref_GASE())
            self.combo_box_Categorie.Hide()
            self.label_CategorieV.SetLabel(self.produit.categorie.nom)

            for i in range(len(self.combo_box_Fournisseur.GetItems())):
                if self.produit.fournisseur == self.combo_box_Fournisseur.GetClientData(i):
                    self.combo_box_Fournisseur.Select(i)
                    break

            self.text_RefFournisseur.SetValue(self.produit.ref_fournisseur)
            self.text_Origine.SetValue(self.produit.origine)
            self.radio_box_TypeVente.SetSelection(self.produit.vrac)
            self.radio_box_UniteMesure.SetSelection(self.produit.liquide)

            if self.produit.vrac:
                self.text_PoidsVolume.SetValue(str(float(self.produit.poids_volume) / 1000))
            else:
                self.text_PoidsVolume.SetValue(str(self.produit.poids_volume))

            self.text_Conditionnement.SetValue(str(self.produit.conditionnement))

            for i in range(len(self.combo_box_TVA.GetItems())):
                if self.produit.tva == self.combo_box_TVA.GetClientData(i):
                    self.combo_box_TVA.Select(i)
                    break

            self.text_PrixAchat.SetValue("%.2f" % float(self.produit.prix_achat_HT))
            self.checkbox_RetraitProduit.SetValue(self.produit.retrait)

            if self.produit.retrait:
                self.text_MotifRetrait.Enable()
                self.text_MotifRetrait.SetValue(self.produit.motif_retrait)

            self.OnDefLabelsUnites(None)

        else:
            self.label_CategorieV.Hide()
            self.combo_box_Categorie.Select(0)
            self.OnChoixCategorie(None)
            self.combo_box_Fournisseur.Select(0)
            self.combo_box_TVA.Select(0)

    def OnDefLabelsUnites(self, event):
        if self.radio_box_UniteMesure.GetSelection():
            self.label_PoidsVolume.SetLabel("Volume :")
        else:
            self.label_PoidsVolume.SetLabel("Poids :")

        if self.radio_box_TypeVente.GetSelection():
            if self.radio_box_UniteMesure.GetSelection():
                self.label_GrL.SetLabel("litres")
                self.label_UniteSacBidon.SetLabel("bidon")
                self.label_PrixUniteSacBidon.SetLabel(u"€ par bidon")
            else:
                self.label_GrL.SetLabel("kilos")
                self.label_UniteSacBidon.SetLabel("sac")
                self.label_PrixUniteSacBidon.SetLabel(u"€ par sac")

            self.text_PoidsVolume.SetValidator(GenericTextValidator(flag=VALIDATE_FLOAT))
        else:
            if self.radio_box_UniteMesure.GetSelection():
                self.label_GrL.SetLabel("milli-litres")
            else:
                self.label_GrL.SetLabel("grammes")

            self.text_PoidsVolume.SetValidator(GenericTextValidator(flag=VALIDATE_INT))

            self.label_UniteSacBidon.SetLabel(u"unité(s) par carton")
            self.label_PrixUniteSacBidon.SetLabel(u"€  par unité")

            self.text_Conditionnement.SetValidator(GenericTextValidator(flag=VALIDATE_INT))

    def OnChoixCategorie(self, event):
        self.produit.categorie = self.combo_box_Categorie.GetClientData(self.combo_box_Categorie.GetSelection())

        id_max = Produit.select().where(Produit.categorie == self.produit.categorie).aggregate(fn.Max('id'))

        if id_max == None:
            self.produit.id = 1
        else:
            self.produit.id = id_max + 1

        self.label_RefGASEV.SetLabel(self.produit.ref_GASE())

    def OnClickRetrait(self, event):  # wxGlade: FicheProduit.<event_handler>
        self.text_MotifRetrait.Enable(self.checkbox_RetraitProduit.IsChecked())
        event.Skip()

    def OnEnregistre(self, event):
        if self.Validate():
            self.produit.nom = self.text_Nom.GetValue()
            self.produit.fournisseur = self.combo_box_Fournisseur.GetClientData(self.combo_box_Fournisseur.GetSelection())
            self.produit.ref_fournisseur = self.text_RefFournisseur.GetValue()
            self.produit.origine = self.text_Origine.GetValue()
            self.produit.vrac = self.radio_box_TypeVente.GetSelection()
            self.produit.liquide = self.radio_box_UniteMesure.GetSelection()
            if self.produit.vrac:
                self.produit.poids_volume = int(float(self.text_PoidsVolume.GetValue())*1000)
            else:
                self.produit.poids_volume = self.text_PoidsVolume.GetValue()
            self.produit.conditionnement = self.text_Conditionnement.GetValue()
            self.produit.tva = self.combo_box_TVA.GetClientData(self.combo_box_TVA.GetSelection())
            self.produit.prix_achat_HT = self.text_PrixAchat.GetValue()
            self.produit.retrait = self.checkbox_RetraitProduit.IsChecked()
            self.produit.motif_retrait = self.text_MotifRetrait.GetValue()
            if (self.produit.retrait == False):
                self.produit.a_etiquetter = True
            else:
                self.produit.a_etiquetter = False

            with DATABASE.transaction():
                self.produit.save()

            event.Skip()

    def OnClose(self, event):
        #session.rollback()
        event.Skip()
