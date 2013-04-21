#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import wx.lib.agw.genericmessagedialog as GMD
import wx.lib.rcsizer  as rcs

from lib.objectlistview import ObjectListView, ColumnDefn, Filter
from textwrap import fill

from classes.Validators import GenericTextValidator, VALIDATE_INT, VALIDATE_FLOAT
from classes.TextCtrlDescriptive import TextCtrlDescriptive

from model.model import Achat, LigneAchat, Produit, Adherent, DATABASE
from datetime import datetime

###########################################################################
## Class FicheAchat
###########################################################################


class FicheAchat(wx.Dialog):
    """Permet d'éditer un achat. Dialog modal"""
    
    def __init__(self, parent, achat=None, adherent=None):
        wx.Dialog.__init__(self, parent,  style=wx.DEFAULT_DIALOG_STYLE)

        if achat == None:
            if adherent == None:
                #TODO : à modifier quand le système d'identification sera en place
                adherent = Adherent.select().where(Adherent.id == 1).get()

            achat = Achat.create(adherent=adherent)

        self.achat = achat

        self.sizer_infos_staticbox = wx.StaticBox(self, -1, "Informations")

        self.label_credit_restant = wx.StaticText(self, -1, u"Crédit restant")
        self.label_cotisation = wx.StaticText(self, -1, u"Cotisation du mois")
        self.label_cotisation_payee = wx.StaticText(self, -1, u"- Payée le xx-xx-xx")
        self.label_total_achats = wx.StaticText(self, -1, "Total des achats")
        self.label_solde = wx.StaticText(self, -1, u"Solde après achat")
        self.label_credit_restant_valeur = wx.StaticText(self, -1, u"0.00 €")
        self.label_cotisation_valeur = wx.StaticText(self, -1, u"0.00 €")
        self.label_total_achats_valeur = wx.StaticText(self, -1, u"0.00 €", style=wx.ALIGN_RIGHT)
        self.label_cout_supplementaire = wx.StaticText(self, -1, u"Coût supplémentaire")
        self.text_cout_supplementaire = wx.TextCtrl(self, -1, validator=GenericTextValidator(VALIDATE_FLOAT, obligatoire=False))
        self.text_cout_supplementaire_commentaire = TextCtrlDescriptive(self, -1, style=wx.TE_MULTILINE)
        self.label_solde_valeur = wx.StaticText(self, -1, u"0.00 €")

        self.sizer_liste_produits_staticbox = wx.StaticBox(self, -1, "Liste des produits")
        self.label_titre_achat = wx.StaticText(self, -1, "Achat pour ")
        self.search_nom = wx.SearchCtrl(self, -1, "")
        self.liste_produits = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        self.liste_produits.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "ref_GASE", minimumWidth=70),
            ColumnDefn("Nom", "left", -1, "nom", minimumWidth=100),
            ColumnDefn("Prix", "right", -1, "prix_vente_format", minimumWidth=100, isSpaceFilling=True)
        ])
        self.liste_produits.SetEmptyListMsg("Aucun produits")
        self.liste_produits.AutoSizeColumns()

        self.sizer_achat_staticbox = wx.StaticBox(self, -1, "Achat")
        self.liste_lignes_achat = ObjectListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        self.liste_lignes_achat.SetColumns([
            ColumnDefn("Ref GASE", "left", -1, "produit.ref_GASE", minimumWidth=70),
            ColumnDefn("Nom", "left", -1, "produit.nom", minimumWidth=100),
            ColumnDefn("Prix", "left", -1, "produit.prix_vente_format", minimumWidth=100),
            ColumnDefn(u"Quantité", "left", -1, "quantite_format", minimumWidth=70),
            ColumnDefn("Total TTC", "right", -1, "prix_total", stringConverter=u"%.2f €", minimumWidth=70, isSpaceFilling=True)
        ])
        self.liste_lignes_achat.AutoSizeColumns()

        self.liste_lignes_achat.SetEmptyListMsg(u"Produits achetés")
        
        self.bouton_sauvegarder = wx.Button(self, wx.ID_SAVE)
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL)

        self.__set_properties()
        self.__set_tooltips()
        self.__set_values()
        self.__do_layout()

        self.bouton_sauvegarder.Bind(wx.EVT_BUTTON, self.OnSauvegarder)
        self.bouton_annuler.Bind(wx.EVT_BUTTON, self.OnClose)
        self.text_cout_supplementaire.Bind(wx.EVT_TEXT, self.OnChangeCoutSupp)
        self.search_nom.Bind(wx.EVT_TEXT, self.OnFilter)
        self.liste_produits.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnAjoutProduit)
        self.liste_lignes_achat.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnModifProduit)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def __set_properties(self):
        self.label_titre_achat.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_infos_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_liste_produits_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_achat_staticbox.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        
        font_italic = self.label_cotisation.GetFont()
        font_italic.SetStyle(wx.ITALIC)
    
        self.label_cotisation_payee.SetFont(font_italic)
        
        """self.label_credit_restant.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_cotisation.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total_achats.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_solde.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_credit_restant_valeur.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_cotisation_valeur.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_total_achats_valeur.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_solde_valeur.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))"""
        
        self.text_cout_supplementaire.SetMinSize((60,-1))
        self.text_cout_supplementaire_commentaire.SetMinSize((-1, 50))
        self.label_credit_restant.SetMinSize((130, -1))
        self.search_nom.SetMinSize((200, -1))        
        self.search_nom.SetDescriptiveText("Recherche sur le nom")
        
    def __set_tooltips(self):
        self.text_cout_supplementaire_commentaire.SetToolTip(wx.ToolTip(u"Description des coûts supplémentaires"))

    def __set_values(self):
        try:
            produits = Produit.select().where((Produit.retrait == False) |
                                              (Produit.retrait == True and Produit.stock > 0))
            self.liste_produits.SetObjects([p for p in produits])
            self.liste_produits.AutoSizeColumns()
            
            self.liste_lignes_achat.SetObjects([la for la in self.achat.lignes_achat])
            
            credit_restant = self.achat.adherent.solde - self.achat.total
            
            self.label_credit_restant_valeur.SetLabel(u"%.2f €" % credit_restant)

            if credit_restant >= 0:
                self.label_credit_restant_valeur.SetForegroundColour("#00AA00")
            else:
                self.label_credit_restant_valeur.SetForegroundColour("#DD0000")

            cotisation_du_mois = self.achat.adherent.cotisation_du_mois
            
            if cotisation_du_mois:
                self.label_cotisation_valeur.SetLabel("\\")
                self.label_cotisation_payee.SetLabel(u"- %.2f €, payée le %s" % (cotisation_du_mois.montant, cotisation_du_mois.date.strftime("%d-%m-%Y")))
            else:
                self.label_cotisation_valeur.SetLabel(u"%.2f €" % self.achat.adherent.cotisation_type.prix)
                self.label_cotisation_payee.Hide()
            
            print self.achat.cout_supplementaire
            self.text_cout_supplementaire.SetValue("%.2f" % float(self.achat.cout_supplementaire))
            self.text_cout_supplementaire_commentaire.SetValue(self.achat.cout_supplementaire_commentaire)

            self.__update_total()

        except BaseException as ex:
            print ex


    def __do_layout(self): 
        grid_sizer_infos = rcs.RowColSizer()

        grid_sizer_infos.Add(self.label_credit_restant, row=0, col=0)
        grid_sizer_infos.Add(self.label_credit_restant_valeur, flag=wx.ALIGN_RIGHT, row=0, col=1)
        grid_sizer_infos.Add(self.label_cotisation, row=1, col=0)
        grid_sizer_infos.Add(self.label_cotisation_valeur, flag=wx.ALIGN_RIGHT, row=1, col=1)
        grid_sizer_infos.Add(self.label_cotisation_payee, row=2, col=0, colspan=2)
        grid_sizer_infos.Add(self.label_total_achats, row=3, col=0)
        grid_sizer_infos.Add(self.label_total_achats_valeur, flag=wx.ALIGN_RIGHT, row=3, col=1)
        grid_sizer_infos.Add(self.label_cout_supplementaire, flag=wx.ALIGN_CENTER_VERTICAL, row=4, col=0)
        grid_sizer_infos.Add(self.text_cout_supplementaire, flag=wx.ALIGN_RIGHT, row=4, col=1)
        grid_sizer_infos.Add(self.text_cout_supplementaire_commentaire, flag=wx.EXPAND, row=5, col=0, colspan=2) 
        grid_sizer_infos.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), flag=wx.EXPAND, row=6, col=0, colspan=2) 
        grid_sizer_infos.Add(self.label_solde, row=7, col=0)
        grid_sizer_infos.Add(self.label_solde_valeur, flag=wx.ALIGN_RIGHT, row=7, col=1)
        
        sizer_infos = wx.StaticBoxSizer(self.sizer_infos_staticbox, wx.VERTICAL)
        sizer_infos.Add(grid_sizer_infos, 1, wx.ALL|wx.EXPAND, 5)

        sizer_liste_produits = wx.StaticBoxSizer(self.sizer_liste_produits_staticbox, wx.VERTICAL)
        sizer_liste_produits.Add(self.search_nom, 0, wx.BOTTOM, 6)
        sizer_liste_produits.Add(self.liste_produits, 1, wx.EXPAND, 0)
        
        sizer_infos_produits = wx.BoxSizer(wx.HORIZONTAL)
        sizer_infos_produits.Add(sizer_infos, 0, wx.EXPAND|wx.RIGHT, 5)
        sizer_infos_produits.Add(sizer_liste_produits, 1, wx.EXPAND, 0)

        sizer_achat = wx.StaticBoxSizer(self.sizer_achat_staticbox, wx.VERTICAL)
        sizer_achat.Add(self.liste_lignes_achat, 1, wx.EXPAND, 0)

        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add(self.bouton_sauvegarder, 1)
        sizer_boutons.Add((10,10), 1, wx.EXPAND)
        sizer_boutons.Add(self.bouton_annuler, 1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label_titre_achat, 0, wx.BOTTOM|wx.EXPAND, 10)
        sizer.Add(sizer_infos_produits, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer.Add(sizer_achat, 1, wx.EXPAND, 0) 
        sizer.Add(sizer_boutons, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 6)
        
        sizer_dialog = wx.BoxSizer(wx.VERTICAL)
        sizer_dialog.Add(sizer, 1, wx.ALL|wx.EXPAND, 10)
        
        self.SetSizer(sizer_dialog)
        sizer_dialog.Fit(self)

    def __update_total(self):
        solde = self.achat.adherent.solde

        self.label_total_achats_valeur.SetLabel(u"%.2f €" % self.achat.total)
        self.label_solde_valeur.SetLabel(u"%.2f €" % solde)

        if solde >= 0:
            self.label_solde_valeur.SetForegroundColour("#00AA00")
        else:
            self.label_solde_valeur.SetForegroundColour("#DD0000")

        self.Layout()

    def GetAchat(self):
        return self.achat
    
    def OnChangeCoutSupp(self, event):
        try:
            #PAS FINI !!
            if self.text_cout_supplementaire.GetValue() != "":
                self.achat.cout_supplementaire = float(self.text_cout_supplementaire.GetValue())
                self.text_cout_supplementaire.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                self.__update_total()
        except ValueError:
            self.text_cout_supplementaire.SetBackgroundColour('#ffcccc')

    def OnFilter(self, event):
        filtre_texte = Filter.TextSearch(self.liste_produits, text=self.search_nom.GetValue())
        self.liste_produits.SetFilter(filtre_texte)
        self.liste_produits.RepopulateList()

    def OnAjoutProduit(self, event):
        deja_ajoute = False
        produit_selectionne = self.liste_produits.GetSelectedObject()

        for la_liste in self.liste_lignes_achat.GetObjects():
            if la_liste.produit.get_id() == produit_selectionne.get_id():
                deja_ajoute = True
                break

        if deja_ajoute == False:
            la = LigneAchat(achat=self.achat, produit=produit_selectionne)
            
            dlg = DialogChoixQuantite(la)

            if dlg.ShowModal() == wx.ID_OK:
                if dlg.GetQuantite() != 0:
                    la.quantite = dlg.GetQuantite()
                    la.save()
                    self.liste_lignes_achat.AddObject(la)
                    self.liste_lignes_achat.AutoSizeColumns()

                    #Mise à jour du total de l'achat
                    self.__update_total()

            dlg.Destroy()

    def OnModifProduit(self, event):
        la_selectionnee = self.liste_lignes_achat.GetSelectedObject()

        dlg = DialogChoixQuantite(la_selectionnee)

        id_resultat = dlg.ShowModal()

        if id_resultat == wx.ID_OK and dlg.GetQuantite() != 0:
            la_selectionnee.quantite = dlg.GetQuantite()
            la_selectionnee.save()
            self.liste_lignes_achat.RefreshObject(la_selectionnee)
            self.liste_lignes_achat.AutoSizeColumns()
        elif id_resultat == wx.ID_DELETE or dlg.GetQuantite() == 0:
            self.liste_lignes_achat.RemoveObject(la_selectionnee)
            self.liste_lignes_achat.RefreshObject(la_selectionnee)
            la_selectionnee.delete_instance()
            self.liste_lignes_achat.AutoSizeColumns()

        #Mise à jour du total de la achat
        self.__update_total()

        dlg.Destroy()

    def OnSauvegarder(self, event):
        if self.Validate():
            cotisation = self.achat.adherent.paye_cotisation_du_mois()
            cotisation.save()            
                
            self.achat.date = datetime.today()
            if self.text_cout_supplementaire.GetValue():
                self.achat.cout_supplementaire = float(self.text_cout_supplementaire.GetValue())
            else:
                self.achat.cout_supplementaire = 0
            self.achat.cout_supplementaire_commentaire = self.text_cout_supplementaire_commentaire.GetValue()
            self.achat.save()
            DATABASE.commit()
            wx.MessageBox(u"L'achat a été enregistré", "Notification")
            self.EndModal(wx.ID_SAVE)

    def OnClose(self, event):
        dlg = wx.MessageDialog(parent=None, message=u"Voulez vous sauvegarder cet achat ?",
                               caption=u"Sauvegarde de l'achat", style=wx.YES_NO|wx.ICON_QUESTION)
    
        if dlg.ShowModal() == wx.ID_YES:
            self.OnSauvegarder(event)
        else:
            DATABASE.rollback()
            self.EndModal(wx.ID_CANCEL)


###########################################################################
## Class DialogChoixQuantite
###########################################################################


class DialogChoixQuantite(wx.Dialog):
    def __init__(self, ligne_achat):
        wx.Dialog.__init__(self, None, -1, u"Quantité", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.ligne_achat = ligne_achat

        self.label_quantite = wx.StaticText(self, -1, u"Quantité :")
        self.text_quantite = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER, validator=GenericTextValidator(flag=VALIDATE_INT))
        self.label_unite = wx.StaticText(self, -1, "Label unite")
        self.bouton_ok = wx.Button(self, wx.ID_OK, "")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "")

        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnregistrer, self.text_quantite)

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

    def __set_properties(self):
        self.text_quantite.SetMinSize((80, -1))
        self.text_quantite.SetFocus()
        
    def __set_valeurs(self):
        if self.ligne_achat.produit.vrac:
            self.label_unite.SetLabel(self.ligne_achat.produit.unite_vente)
        else:
            self.label_unite.SetLabel(self.ligne_achat.produit.unite_vente +"(s)")
            
        self.text_quantite.SetValue(str(self.ligne_achat.quantite))
            
        if self.ligne_achat.quantite > 0:
            self.bouton_annuler.SetLabel("Supprimer")
            self.bouton_annuler.SetId(wx.ID_DELETE)
            self.bouton_annuler.Bind(wx.EVT_BUTTON, self.OnSupprimer)

    def __do_layout(self):
        sizer_choix = wx.BoxSizer(wx.HORIZONTAL)
        sizer_choix.Add(self.label_quantite, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_choix.Add(self.text_quantite, 0, wx.LEFT|wx.RIGHT, 6)
        sizer_choix.Add(self.label_unite, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)
        sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        sizer_boutons.Add((1, 1), 1, wx.EXPAND, 0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_choix, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(sizer_boutons, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def GetQuantite(self):
        return int(self.text_quantite.GetValue())

    def OnEnregistrer(self, event):
        if self.Validate():
            self.EndModal(wx.ID_OK)

    def OnSupprimer(self, event):
        self.EndModal(wx.ID_DELETE)
