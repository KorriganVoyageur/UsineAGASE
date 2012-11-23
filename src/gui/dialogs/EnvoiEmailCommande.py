#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from datetime import datetime
import wx

from model.model import Parametre

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.header import Header
from email import Encoders

from classes.ConnectionSMTP import ConnectionSMTP, SMTPRecipientsRefused

###########################################################################
## Class EnvoiEmail
###########################################################################


class EnvoiEmailCommande(wx.Dialog):
    def __init__(self, parent, commande):
        wx.Dialog.__init__(self, parent, -1, "Nouvelle commande")

        self.commande = commande

        self.panel = wx.Panel(self)

        self.label_destinataire = wx.StaticText(self.panel, -1, "Destinataire :")
        self.label_destinataire_v = wx.StaticText(self.panel, -1, "XXXX")
        self.label_sujet = wx.StaticText(self.panel, -1, "Sujet :")
        self.tc_sujet = wx.TextCtrl(self.panel, -1, "Commande pour le GASE")
        self.tc_message = wx.TextCtrl(self.panel, -1, "", style=wx.TE_MULTILINE)
        self.bouton_envoyer = wx.Button(self.panel, wx.ID_OK, "Envoyer")
        self.bouton_annuler = wx.Button(self.panel, wx.ID_CLOSE, "Annuler")

        self.__set_properties()
        self.__set_valeurs()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnEnvoyer, self.bouton_envoyer)
        self.Bind(wx.EVT_BUTTON, self.OnAnnuler, self.bouton_annuler)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: EnvoiEmail.__set_properties
        self.tc_message.SetMinSize((400, 200))
        # end wxGlade

    def __set_valeurs(self):
        # begin wxGlade: EnvoiEmail.__set_properties
        self.label_destinataire_v.SetLabel(self.commande.fournisseur.nom + " <%s>" % self.commande.fournisseur.email)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: EnvoiEmail.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(2, 2, 5, 10)
        grid_sizer.Add(self.label_destinataire, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.label_destinataire_v, 0, 0, 0)
        grid_sizer.Add(self.label_sujet, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer.Add(self.tc_sujet, 0, wx.EXPAND, 0)

        sizer.Add(grid_sizer, 0, wx.ALL|wx.EXPAND, 5)

        sizer.Add(self.tc_message, 1, wx.ALL|wx.EXPAND, 5)

        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.bouton_envoyer, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)
        sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        sizer_boutons.Add((20, 20), 1, 0, 0)

        sizer.Add(sizer_boutons, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 10)

        self.panel.SetSizer(sizer)
        sizer.Fit(self)
        # end wxGlade

    def OnEnvoyer(self, event):
        dlg = wx.MessageDialog(parent=None, message=u"Voulez vous vraiment envoyer le bon de commande par email ?",
                               caption=u"Demande de confirmation", style=wx.OK|wx.CANCEL|wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_OK:
            print self.commande.fournisseur.email
            destinataire = "herve.garnier@no-log.org"
            sujet = self.tc_sujet.GetValue()
            message = self.tc_message.GetValue()

            self.commande.genere_PDF("dernier_bon_imprime.pdf")
            fichier_nom = "Bon de commande du %s.pdf" % datetime.today().strftime("%d-%m-%Y")

            piece_jointe = MIMEBase('application', 'octet-stream')
            piece_jointe.set_payload(open("dernier_bon_imprime.pdf", 'rb').read())
            Encoders.encode_base64(piece_jointe)
            piece_jointe.add_header('Content-Disposition', 'attachment; filename="%s"' % fichier_nom)

            mail = MIMEMultipart()

            mail['From'] = Parametre.get(nom="SMTP_login")
            mail['To'] = destinataire
            mail['Subject'] = "%s" % Header(sujet, 'utf-8')

            mail.attach(MIMEText(message, 'plain', 'UTF-8'))

            mail.attach(piece_jointe)

            smtp = ConnectionSMTP()

            if smtp.TestConnectionInternet():
                try:
                    smtp.SetServeur(Parametre.get(nom="SMTP_serveur"),
                                    int(Parametre.get(nom="SMTP_serveurport")),
                                    Parametre.get(nom="SMTP_serveursecurite"))
    
                    smtp.SetLogin(Parametre.get(nom="SMTP_login"),
                                  Parametre.get(nom="SMTP_motdepasse"))
    
                    serveur = smtp.ConnectionServeur()
                    serveur.sendmail(Parametre.get(nom="SMTP_login"),
                                     self.destinataire,
                                     mail.as_string())
    
                    serveur.close()

                    wx.MessageBox(u"L'email a bien été envoyé", u"Email envoyé", wx.ICON_INFORMATION)
                    event.Skip()

                except SMTPRecipientsRefused:
                    wx.MessageBox(u"L'adresse email du destinataire est invalide", "Erreur", wx.ICON_ERROR)

                except Exception as ex:
                    wx.MessageBox(u"Problème lors de l'envoi de l'email\n\n %s" % ex, "Erreur", wx.ICON_ERROR)
            else:
                    wx.MessageBox(u"Problème de connection internet", "Erreur", wx.ICON_ERROR|wx.CENTER)

    def OnAnnuler(self, event):
        dlg = wx.MessageDialog(parent=None, message=u"Annuler l'envoi du bon de commande par email ?",
                               caption=u"Demande de confirmation", style=wx.OK|wx.CANCEL|wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_OK:
            event.Skip()
