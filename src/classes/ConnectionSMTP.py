#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import smtplib
import urllib2

from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused

###########################################################################
## Class ConnectionSMTP
###########################################################################


class ConnectionSMTP(object):
    
    def __init__(self, serveur="", port=0, type_securite=0, login="", mot_de_passe=""):
        self.serveur = serveur
        self.port = port
        self.type_securite = type_securite
        self.login= login
        self.mot_de_passe = mot_de_passe
    
    def SetServeur(self, serveur, port, type_securite=0):
        self.serveur = serveur
        self.port = port
        self.type_securite = type_securite
    
    def SetLogin(self, login, mot_de_passe):
        self.login= login
        self.mot_de_passe = mot_de_passe        
    
    #Permet de tester la connection internet
    def TestConnectionInternet(self):
        try:
            urllib2.urlopen("http://www.google.com/")
            return True
        except:
            return False
        
    def ConnectionServeur(self):
        if self.type_securite == 2:
            server = smtplib.SMTP_SSL(self.serveur, self.port)
        else:
            server = smtplib.SMTP(self.serveur, self.port)
            
        server.ehlo()

        if self.type_securite == 1:
            server.starttls()
            server.ehlo()

        server.login(self.login, self.mot_de_passe)
        
        return server