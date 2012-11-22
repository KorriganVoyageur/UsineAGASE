#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Adhesion, AdhesionType, Exercice, DATABASE
from datetime import datetime

###########################################################################
## Class FicheAdhesion
###########################################################################


class FicheAdhesion(wx.Panel):
    def __init__(self, parent, adhesion=None, adherent=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)
        
        if adhesion:
            self.adhesion = adhesion
        else:
            self.adhesion = Adhesion(adherent=adherent)

        self.label_adherent = wx.StaticText(self, -1, u"Adhérent :")
        self.label_adherent_v = wx.StaticText(self, -1, "")
        self.label_date_debut = wx.StaticText(self, -1, u"Date de début")
        self.datepicker_date_adhesion = wx.DatePickerCtrl(self, -1)
        self.label_type = wx.StaticText(self, -1, u"Type d'adhésion")
        self.combo_box_adhesion_type = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_cheque = wx.StaticText(self, -1, u"N° chèque")
        self.text_ctrl_cheque = wx.TextCtrl(self, -1, "")
        self.bouton_valider = wx.Button(self, wx.ID_OK, "Valider")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__set_combobox_types_adhesion()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnValider, self.bouton_valider)
        # end wxGlade

    def __set_properties(self):
        self.text_ctrl_cheque.SetMinSize((150, -1))

    def __set_combobox_types_adhesion(self):
        try:
            adhesion_types = [a for a in AdhesionType.select().order_by(AdhesionType.prix.asc())]
            for adhesion_type in adhesion_types:
                self.combo_box_adhesion_type.Append(adhesion_type.nom + u" - %s €" % adhesion_type.prix, adhesion_type)

            self.combo_box_adhesion_type.Select(0)

        except BaseException as ex:
            print ex

    def __set_valeurs(self):
        self.label_adherent_v.SetLabel(self.adhesion.adherent.nom_prenom)

        if self.adhesion.get_id() != None:
            for i in range(len(self.combo_box_adhesion_type.GetItems())):
                if self.adhesion.adhesion_type == self.combo_box_adhesion_type.GetClientData(i):
                    self.combo_box_adhesion_type.Select(i)
                    break

            date = wx.DateTime()

            date.Set(self.adhesion.date.day, self.adhesion.date.month-1, self.adhesion.date.year)
            self.datepicker_date_adhesion.SetValue(date)
            self.text_ctrl_cheque.SetValue(self.adhesion.cheque)
        '''else:
            date_debut = wx.DateTime()
            date_fin = wx.DateTime()
    
            #TODO:verif exercice
            exercice_en_cours = Exercice.en_cours()
    
            date_debut.Set(exercice_en_cours.date_debut.day, exercice_en_cours.date_debut.month-1, exercice_en_cours.date_debut.year)
            date_fin.Set(exercice_en_cours.date_fin.day, exercice_en_cours.date_fin.month-1, exercice_en_cours.date_fin.year)
    
            self.datepicker_date_adhesion.SetRange(date_debut, date_fin)'''

    def __do_layout(self):
        # begin wxGlade: FicheAdhesion.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(5, 2, 5, 10)
        grid_sizer.Add(self.label_adherent, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5)
        grid_sizer.Add(self.label_adherent_v, 0, wx.BOTTOM, 5)
        grid_sizer.Add(self.label_date_debut, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.datepicker_date_adhesion, 0, 0, 0)
        grid_sizer.Add(self.label_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.combo_box_adhesion_type, 0, 0, 0)
        grid_sizer.Add((1, 1), 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add((1, 1), 0, 0, 0)
        grid_sizer.Add(self.label_cheque, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_ctrl_cheque, 0, 0, 0)
        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_valider, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer_bouton.Add(self.bouton_annuler, 0, 0, 0)
        sizer_bouton.Add((20, 20), 1, 0, 0)
        sizer.Add(sizer_bouton, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def OnValider(self, event):
        if self.Validate():
            msgbox = wx.MessageBox(u"Sauvegarder l'adhésion ?", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION)

            if msgbox == wx.YES:
                date_adhesion = self.datepicker_date_adhesion.GetValue()

                self.adhesion.date = datetime(date_adhesion.GetYear(), date_adhesion.GetMonth()+1, date_adhesion.GetDay())
                self.adhesion.adhesion_type = self.combo_box_adhesion_type.GetClientData(self.combo_box_adhesion_type.GetSelection())
                self.adhesion.montant = self.adhesion.adhesion_type.prix
                self.adhesion.cheque = self.text_ctrl_cheque.GetValue()
                
                with DATABASE.transaction():
                    self.adhesion.save()

                event.Skip()
