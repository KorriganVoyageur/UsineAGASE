#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import wx
import re

from model.model import Parametre

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

from classes.ConnectionSMTP import ConnectionSMTP, SMTPRecipientsRefused

###########################################################################
## Class EnvoiEmail
###########################################################################


class EnvoiEmail(object):

    def __init__(self):
        self.destinataire = ""
        self.sujet = ""
        self.message = ""
        self.piece_jointe = None

    def SetDestinataire(self, value):
        if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", value):
            self.destinataire = value
        else:
            self.destinataire = ""

    def SetSujet(self, value):
        self.sujet = value

    def SetMessage(self, value):
        self.message = value

    def SetPieceJointe(self, value):
        if os.path.exists(value):
            try:
                self.piece_jointe = MIMEBase('application', 'octet-stream')
                self.piece_jointe.set_payload(open(value, 'rb').read())
                Encoders.encode_base64(self.piece_jointe)
                self.piece_jointe.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(value))
            except BaseException as ex:
                print ex
                self.piece_jointe = None
        else:
            self.piece_jointe = None

    def Envoi(self, silencieux=True):

        msg = MIMEMultipart()

        msg['From'] = Parametre.get(nom="SMTP_login")
        msg['To'] = self.destinataire
        msg['Subject'] = self.sujet

        msg.attach(MIMEText(self.message))

        if self.piece_jointe:
            msg.attach(self.piece_jointe)

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
                                 msg.as_string())

                serveur.close()

                if not silencieux:
                    wx.MessageBox(u"L'email a bien �t� envoy�", u"Email envoy�", wx.ICON_INFORMATION)

                return True

            except SMTPRecipientsRefused:
                if not silencieux:
                    wx.MessageBox(u"L'adresse email du destinataire est invalide", "Erreur", wx.ICON_ERROR)

                return False

            except Exception as ex:
                if not silencieux:
                    wx.MessageBox(u"Probl�me lors de l'envoi de l'email\n\n %s" % ex, "Erreur", wx.ICON_ERROR)

                return False
        else:
            if not silencieux:
                wx.MessageBox(u"Probl�me de connection internet", "Erreur", wx.ICON_ERROR|wx.CENTER)

                return False
