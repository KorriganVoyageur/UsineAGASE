#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Inventaire, DATABASE
from gui.dialogs.ChoixQuantite import ChoixQuantite
from classes.Validators import GenericTextValidator, VALIDATE_INT

from lib.objectlistview import ObjectListView, ColumnDefn, CellEditor, EVT_CELL_EDIT_STARTING
from datetime import datetime


class StockIntEditor(CellEditor.BaseCellTextEditor):
    """This is a text editor for integers for use in an ObjectListView"""

    def GetValue(self):
        "Get the value from the editor"
        s = wx.TextCtrl.GetValue(self).strip()
        try:
            return int(s)
        except ValueError:
            return None

    def SetValue(self, value):
        "Put a new value into the editor"
        try:
            value = repr(int(value.split()[0]))
        except:
            pass
            
        wx.TextCtrl.SetValue(self, value)


class StockFloatEditor(CellEditor.BaseCellTextEditor):
    """This is a text editor for floats for use in an ObjectListView"""

    def GetValue(self):
        "Get the value from the editor"
        s = wx.TextCtrl.GetValue(self).strip()
        try:
            return float(s)
        except ValueError:
            return None

    def SetValue(self, value):
        "Put a new value into the editor"
        try:
            value = repr(float(value.split()[0]))
        except:
            pass
            
        wx.TextCtrl.SetValue(self, value)

###########################################################################
## Class FicheInventaire
###########################################################################


class FicheInventaire(wx.Panel):
    def __init__(self, parent, inventaire=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)
        
        if inventaire:
            self.inventaire = inventaire
        else:
            inventaire = Inventaire.create()
            inventaire.initialisation()
            
        self.inventaire = inventaire

        self.label_date = wx.StaticText(self, -1, u"Date de l'inventaire :")
        self.label_date_v = wx.StaticText(self, -1, "")
        self.label_commentaire = wx.StaticText(self, -1, "Commentaire")
        self.text_commentaire = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.liste_lignes_inventaire = ObjectListView(self, -1,
                                                      style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL)

        def update_stock_reel(li, valeur):
            if valeur<0:
                valeur = 0

            if li.produit.vrac:
                li.stock_reel = valeur *  1000
            else:
                li.stock_reel = valeur
                
            li.save()
                
        def editor_stock_reel(olv, rowIndex, subItemIndex):
            if olv.GetObjectAt(rowIndex).produit.vrac:
                return StockFloatEditor(olv, subItemIndex, validator=CellEditor.NumericValidator("0123456789.,"))
            else:
                return StockIntEditor(olv, subItemIndex, validator=CellEditor.NumericValidator("0123456789"))
            
        
        self.liste_lignes_inventaire.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "produit.ref_GASE", fixedWidth=90),
            ColumnDefn("Nom", "left", -1, "produit.nom",  minimumWidth=100),
            ColumnDefn("Fournisseur", "left", -1, "produit.fournisseur.nom", minimumWidth=100),
            ColumnDefn(u"Stock théorique", "left", -1,
                       "stock_theorique_format",
                       stringConverter="%s", minimumWidth=80),
            ColumnDefn(u"Stock réel", "left", -1,
                       "stock_reel_format", isEditable=True,
                       cellEditorCreator = editor_stock_reel,
                       valueSetter=update_stock_reel, minimumWidth=80),
            ColumnDefn(u"Différence", "left", -1,
                       "stock_difference", isSpaceFilling=True, minimumWidth=80)
        ])

        def RFLignesInventaire(listItem, ligne_inventaire):
            if ligne_inventaire.stock_reel:
                listItem.SetBackgroundColour("#E3FFCB")
            else:
                listItem.SetBackgroundColour("#FFD3D3")
                
        #self.liste_lignes_inventaire.rowFormatter = RFLignesInventaire

        self.bouton_enregistrer = wx.Button(self, wx.ID_SAVE, "Enregistrer")
        self.bouton_valider = wx.Button(self, wx.ID_OK, u"Valider l'inventaire")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__set_valeurs()
        self.__remplissage_liste()
        self.__do_layout()

        self.liste_lignes_inventaire.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onModifStock)

        self.bouton_enregistrer.Bind(wx.EVT_BUTTON, self.OnEnregistrer)
        self.bouton_valider.Bind(wx.EVT_BUTTON, self.OnValider)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def __set_properties(self):
        self.text_commentaire.SetMinSize((400, 200))

    def __set_valeurs(self):
        self.label_date_v.SetLabel(self.inventaire.date.strftime("%d/%m/%y"))
        self.text_commentaire.SetValue(self.inventaire.commentaire)
        
    def __remplissage_liste(self):
        try:
            self.liste_lignes_inventaire.SetObjects([li for li in self.inventaire.lignes_inventaire])
        except BaseException as ex:
            print ex
            
    def __do_layout(self):
        # begin wxGlade: FicheInventaire.__do_layout
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)

        grid_sizer = wx.FlexGridSizer(5, 2, 5, 10)
        grid_sizer.Add(self.label_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.label_date_v, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.label_commentaire, 0, wx.ALIGN_TOP, 0)
        grid_sizer.Add(self.text_commentaire, 1, 0, 0)

        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_enregistrer, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_valider, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_annuler, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(self.liste_lignes_inventaire, 1, wx.ALL|wx.EXPAND, 10)
        sizer.Add(sizer_bouton, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()   

    def onModifStock(self, event):
        self.liste_lignes_inventaire.StartCellEdit(self.liste_lignes_inventaire.GetFocusedRow(), 4)

    def OnEnregistrer(self, event):
        if self.Validate():
            msgbox = wx.MessageBox(u"Sauvegarder l'inventaire ?", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                with DATABASE.transaction():
                    self.inventaire.save()

                event.Skip()
                
    def OnValider(self, event):
        if self.Validate():
            msgbox = wx.MessageBox(u"Valider l'inventaire ? Il ne sera plus modifiable.", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                self.inventaire.is_valide = True

                with DATABASE.transaction():
                    self.inventaire.save()

                event.Skip()

    def onDestroy(self, event):
        dlg = wx.MessageDialog(parent=None, message=u"Voulez vous sauvegarder l'inventaire ?",
                               caption=u"Sauvegarde de la inventaire", style=wx.YES_NO|wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.inventaire.save()
            DATABASE.commit()
        else:
            DATABASE.rollback()

        dlg.Destroy()

        event.Skip()
