#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
from model.model import Exercice, DATABASE, EXERCICE_EN_COURS
from peewee import DoesNotExist

from classes.Validators import GenericTextValidator
import datetime

###########################################################################
## Class FicheExercice
###########################################################################


class FicheExercice(wx.Panel):
    def __init__(self, parent, exercice=None):
        wx.Panel.__init__(self, parent, style=wx.TAB_TRAVERSAL)

        if exercice == None:
            exercice = Exercice()

        self.exercice = exercice

        self.label_nom = wx.StaticText(self, -1, "Nom")
        self.text_ctrl_nom = wx.TextCtrl(self, -1, "", validator=GenericTextValidator())
        self.label_date_debut = wx.StaticText(self, -1, u"Date de début")
        self.datepicker_date_debut = wx.DatePickerCtrl(self, -1)
        self.label_date_fin = wx.StaticText(self, -1, "Date de fin")
        self.datepicker_date_fin = wx.DatePickerCtrl(self, -1)
        self.bouton_valider = wx.Button(self, wx.ID_OK, "Valider")
        self.bouton_annuler = wx.Button(self, wx.ID_CANCEL, "Annuler")

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnValider, self.bouton_valider)
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateDebutChange, self.datepicker_date_debut)
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateFinChange, self.datepicker_date_fin)
        # end wxGlade

    def __set_properties(self):
        self.text_ctrl_nom.SetMinSize((200, -1))
        self.datepicker_date_debut.SetMinSize((200, -1))
        self.datepicker_date_fin.SetMinSize((200, -1))
        # end wxGlade

    def __set_valeurs(self):
        if self.exercice.get_id():
            self.text_ctrl_nom.SetValue(self.exercice.nom)

            date_temp = wx.DateTime()

            date_temp.Set(self.exercice.date_debut.day, self.exercice.date_debut.month-1, self.exercice.date_debut.year)
            self.datepicker_date_debut.SetValue(date_temp)

            date_temp.Set(self.exercice.date_fin.day, self.exercice.date_fin.month-1, self.exercice.date_fin.year)
            self.datepicker_date_fin.SetValue(date_temp)

            self.OnDateDebutChange(wx.DateEvent(self, self.datepicker_date_debut.GetValue(), wx.EVT_DATE_CHANGED._getEvtType()))
            self.OnDateFinChange(wx.DateEvent(self, self.datepicker_date_fin.GetValue(), wx.EVT_DATE_CHANGED._getEvtType()))

    def __do_layout(self):
        # begin wxGlade: FicheExercice.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_bouton = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(3, 2, 5, 10)
        grid_sizer.Add(self.label_nom, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.text_ctrl_nom, 0, 0, 0)
        grid_sizer.Add(self.label_date_debut, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.datepicker_date_debut, 0, 0, 0)
        grid_sizer.Add(self.label_date_fin, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.datepicker_date_fin, 0, 0, 0)
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
        # end wxGlade

    def GetExercice(self):
        return self.exercice

    def OnDateDebutChange(self, event):
        self.datepicker_date_fin.SetRange(event.GetDate().AddDS(wx.DateSpan_Day()), wx.DateTime())

    def OnDateFinChange(self, event):
        self.datepicker_date_debut.SetRange(wx.DateTime(), event.GetDate().SubtractDS(wx.DateSpan_Day()))

    def OnValider(self, event):
        date_debut = self.datepicker_date_debut.GetValue()
        date_fin = self.datepicker_date_fin.GetValue()

        date_debut_dt = datetime.date(date_debut.GetYear(), date_debut.GetMonth()+1, date_debut.GetDay())
        date_fin_dt = datetime.date(date_fin.GetYear(), date_fin.GetMonth()+1, date_fin.GetDay())

        try:
            exercice = Exercice.select().where(((Exercice.date_debut <= date_fin_dt) & (Exercice.date_fin >= date_debut_dt))).get()
            if exercice == self.exercice:
                raise DoesNotExist

            wx.MessageBox(u"Les dates indiquées chevauchent l'exercice '%s'" % exercice.nom, "Erreur")
        except DoesNotExist:
            if self.Validate():
                self.exercice.nom = self.text_ctrl_nom.GetValue()
                self.exercice.date_debut = date_debut_dt
                self.exercice.date_fin = date_fin_dt

                with DATABASE.transaction():
                    self.exercice.save()

                EXERCICE_EN_COURS = Exercice.en_cours()

                event.Skip()
