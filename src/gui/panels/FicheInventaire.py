#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Inventaire, LigneInventaire, Fournisseur, Produit, DATABASE

from lib.objectlistview import ObjectListView, ColumnDefn, CellEditor, Filter
from datetime import date
from wx.lib.buttons import GenBitmapTextButton


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
## Class DialogAjoutProduit
###########################################################################

class DialogAjoutProduit(wx.Dialog):
    def __init__(self, inventaire):
        wx.Dialog.__init__(self, None, -1, title=u"Ajouter un produit", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.inventaire = inventaire

        self.liste_produits = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL)

        self.liste_produits.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "ref_GASE", fixedWidth=90),
            ColumnDefn("Nom", "left", -1, "nom"),
            ColumnDefn("Fournisseur", "left", -1, "fournisseur.nom", minimumWidth=100)
        ])

        self.liste_produits.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onClickProduit)

        self.__set_properties()
        self.__remplissage_liste()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        pass
    
    def __remplissage_liste(self):
        try:
            self.liste_produits.SetObjects([p for p in self.inventaire.produits_absents])
            
            #On dimentionne le dialog selon la largeur des colonnes
            largeur = 0
            for num_colonne in range(3) :
                largeur += self.liste_produits.GetColumnWidth(num_colonne)
             
            self.liste_produits.SetMinSize((largeur+20,300))
            
        except BaseException as ex:
            print ex

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.liste_produits, 1, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    """def GetValue(self):
        return int(self.text_ctrl_quantite.GetValue())"""

    def onClickProduit(self, event):
        pass


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

        self.sizer_inventaire_staticbox = wx.StaticBox(self, -1, "Liste des produits")
        self.label_titre_inventaire = wx.StaticText(self, -1, "Inventaire du ")
        self.label_fournisseur = wx.StaticText(self, -1, "Fournisseur :")
        self.combo_box_fournisseur = wx.ComboBox(self, -1,
                                                 choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.label_recherche_nom = wx.StaticText(self, -1, "Recherche sur le nom :")
        self.text_recherche_nom = wx.TextCtrl(self, -1, "")
        self.label_commentaire = wx.StaticText(self, -1, "Commentaire")
        self.text_commentaire = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.bouton_ajout_produit = GenBitmapTextButton(self, -1, wx.Bitmap("../icons/16x16/ajouter.ico"), u" Ajouter un produit non listé")
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

            if self.inventaire.pret_a_valider():
                self.bouton_valider.Enable()
            
                
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
            ColumnDefn(u"Différence", "u_", -1,
                       "stock_difference", minimumWidth=80)
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

        self.combo_box_fournisseur.Bind(wx.EVT_COMBOBOX, self.onFilter)
        self.text_recherche_nom.Bind(wx.EVT_TEXT, self.onFilter)
        self.bouton_ajout_produit.Bind(wx.EVT_BUTTON, self.onAjoutProduit)
        self.liste_lignes_inventaire.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onModifStock)
        self.bouton_enregistrer.Bind(wx.EVT_BUTTON, self.OnEnregistrer)
        self.bouton_valider.Bind(wx.EVT_BUTTON, self.OnValider)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def __set_properties(self):
        self.label_titre_inventaire.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.text_commentaire.SetMinSize((400, 200))
        self.label_fournisseur.SetMinSize((200, -1))
        self.combo_box_fournisseur.SetMinSize((200, -1))
        self.label_recherche_nom.SetMinSize((200, -1))
        self.text_recherche_nom.SetMinSize((200, -1))
        self.sizer_inventaire_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __set_valeurs(self):
        self.label_titre_inventaire.SetLabel("Inventaire du %s" % self.inventaire.date.strftime("%d/%m/%y"))
        self.text_commentaire.SetValue(self.inventaire.commentaire)
        if not self.inventaire.pret_a_valider():
            self.bouton_valider.Disable()
        
    def __remplissage_liste(self):
        try:
            self.liste_lignes_inventaire.SetObjects([li for li in self.inventaire.lignes_inventaire])
            
            self.combo_box_fournisseur.Append("Tous", 0)

            fournisseurs = [f for f in Fournisseur.select().order_by(Fournisseur.nom.asc())]

            for fournisseur in fournisseurs:
                self.combo_box_fournisseur.Append(fournisseur.nom, fournisseur.get_id())

            self.combo_box_fournisseur.Select(0)
        except BaseException as ex:
            print ex
            
    def __do_layout(self):
        # begin wxGlade: FicheInventaire.__do_layout
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)

        grid_sizer = wx.FlexGridSizer(3, 2, 5, 10)
        grid_sizer.Add(self.label_commentaire, 0, wx.ALIGN_TOP, 0)
        grid_sizer.Add(self.text_commentaire, 1, 0, 0)
        grid_sizer.Add(self.label_fournisseur, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.combo_box_fournisseur, 0, 0, 0)
        grid_sizer.Add(self.label_recherche_nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_recherche_nom, 0, 0, 0)

        sizer_inventaire = wx.StaticBoxSizer(self.sizer_inventaire_staticbox, wx.VERTICAL)
        sizer_inventaire.Add(self.liste_lignes_inventaire, 1, wx.ALL|wx.EXPAND, 0)
        sizer_inventaire.Add(self.bouton_ajout_produit, 0, wx.TOP, 10)

        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_enregistrer, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_valider, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_annuler, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_titre_inventaire, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(sizer_inventaire, 1, wx.ALL|wx.EXPAND, 10)
        sizer.Add(sizer_bouton, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()   

    def onAjoutProduit(self, event):
        dlg = DialogAjoutProduit(self.inventaire)

        id_resultat = dlg.ShowModal()

        if id_resultat == wx.ID_OK:
            print "ok"
        elif id_resultat == wx.ID_DELETE:
            print "delete"

        dlg.Destroy()

    def onModifStock(self, event):
        self.liste_lignes_inventaire.StartCellEdit(self.liste_lignes_inventaire.GetFocusedRow(), 4)

    def OnEnregistrer(self, event):
        if self.Validate():
            msgbox = wx.MessageBox(u"Sauvegarder l'inventaire ?", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                self.inventaire.date = date.today()

                with DATABASE.transaction():
                    self.inventaire.save()

                event.Skip()
                
    def OnValider(self, event):
        if self.Validate() and self.inventaire.pret_a_valider():
            msgbox = wx.MessageBox(u"Valider l'inventaire ? Il ne sera plus modifiable.", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                self.inventaire.is_valide = True
                self.inventaire.date = date.today()

                with DATABASE.transaction():
                    self.inventaire.save()

                event.Skip()

    def onDestroy(self, event):
        dlg = wx.MessageDialog(parent=None, message=u"Voulez vous sauvegarder l'inventaire ?",
                               caption=u"Sauvegarde de la inventaire", style=wx.YES_NO|wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.inventaire.date = date.today()
            self.inventaire.save()
            DATABASE.commit()
        else:
            DATABASE.rollback()

        dlg.Destroy()

        event.Skip()
        
    def onFilter(self, event):
        filtre_texte = Filter.TextSearch(self.liste_lignes_inventaire, text=self.text_recherche_nom.GetValue())

        pk_fournisseur = self.combo_box_fournisseur.GetClientData(self.combo_box_fournisseur.GetSelection())

        if pk_fournisseur != 0:
            filtre_fournisseur = Filter.Predicate(lambda x: x.produit.fournisseur.get_id() == pk_fournisseur)
            self.liste_lignes_inventaire.SetFilter(Filter.Chain(filtre_texte, filtre_fournisseur))
        else:
            self.liste_lignes_inventaire.SetFilter(filtre_texte)

        self.liste_lignes_inventaire.RepopulateList()
        event.Skip()

