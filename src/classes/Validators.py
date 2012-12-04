#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

'''
Created on 22 nov. 2010

@author: Herve
'''

import wx
import re
import string

VALIDATE_ALPHA = 4
VALIDATE_INT = 8
VALIDATE_FLOAT = 16


class BaseValidator(wx.PyValidator):

    def __init__(self, obligatoire=True, *args, **kwargs):
        wx.PyValidator.__init__(self, *args, **kwargs)
        self.obligatoire = obligatoire

    #def Clone(self):
    #   return BaseValidator()

    def WxErrorDialog(self, msg, txtctrl=None):
        dlg = wx.MessageDialog(None, msg, "Erreur", style=wx.OK|wx.ICON_ERROR|wx.CENTRE)
        dlg.ShowModal()
        dlg.Destroy()
        
        if txtctrl == None:
            txtctrl = self.win

        txtctrl.SetBackgroundColour('#ffcccc')
        txtctrl.SetFocus()
        txtctrl.Refresh()

    def WxClearErrorDialog(self):
        self.win.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.win.Refresh()

    def TransferToWindow(self):
        return True  # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True  # Prevent wxDialog from complaining.


class GenericTextValidator(BaseValidator):

    def __init__(self, flag=None, *args, **kwargs):
        self.flag = flag
        BaseValidator.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return GenericTextValidator(flag=self.flag, obligatoire=self.obligatoire)

    def Validate(self, win):
        self.win = self.GetWindow()
        if self.win.IsEnabled():
            result = False
            self.text = self.win.GetValue()
            if self.flag == VALIDATE_ALPHA:
                if self.ValidateAlpha():
                    result = True
                else:
                    self.WxErrorDialog(u"Seules les lettres sont autorisées")
            elif self.flag == VALIDATE_INT:
                if self.ValidateInt():
                    result = True
                else:
                    self.WxErrorDialog("Nombre entier requis")
            elif self.flag == VALIDATE_FLOAT:
                if self.ValidateFloat():
                    result = True
                else:
                    self.WxErrorDialog("Nombre requis. Format invalide.")
            else:
                result = True

            if self.obligatoire and result:
                if len(self.text) > 0:
                    result = True
                else:
                    result = False
                    self.WxErrorDialog("Champ obligatoire")

            if result:
                self.WxClearErrorDialog()
        else:
            result = True

        return result

    def ValidateAlpha(self):
        return re.search("^[a-z]+$", self.text, re.IGNORECASE)

    def ValidateInt(self):
        try:
            if self.text != "":
                int(self.text)
            return True
        except ValueError:
            return False

    def ValidateFloat(self):
        try:
            if self.text != "":
                float(self.text)
            return True
        except ValueError:
            return False

    def ValidateNotNull(self):
        return re.search("^.+$", self.text)

    def ValidateEmail(self):
        return re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", self.text)

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == VALIDATE_ALPHA and chr(key) in string.letters:
            event.Skip()
            return

        if self.flag == VALIDATE_INT and chr(key) in string.digits:
            event.Skip()
            return

        if self.flag == VALIDATE_FLOAT and chr(key) in string.digits + ".":
            event.Skip()
            return

        if self.flag == None:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return


class EntreListesDatesValidator(BaseValidator):

    def __init__(self, dates_a, dates_b, *args, **kwargs):
        self.dates_a = dates_a
        self.date_b = dates_b
        BaseValidator.__init__(self, *args, **kwargs)

    def Clone(self):
        return EntreListesDatesValidator(dates_a=self.dates_a, dates_b=self.dates_b)

    def Validate(self, win):
        self.win = self.GetWindow()
        if self.win.IsEnabled():
            result = False
            self.date = self.win.GetValue()

            if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", self.text) or len(self.text) == 0:
                result = True
            else:
                result = False
                self.WxErrorDialog(u"Email invalide")

            if self.obligatoire and result:
                if len(self.text) > 0:
                    result = True
                else:
                    result = False
                    self.WxErrorDialog("Champ obligatoire")
            if result:
                self.WxClearErrorDialog()
        else:
            result = True

        return result


class EmailValidator(BaseValidator):

    def __init__(self, *args, **kwargs):
        BaseValidator.__init__(self, *args, **kwargs)

    def Clone(self):
        return EmailValidator(obligatoire=self.obligatoire)

    def Validate(self, win):
        self.win = self.GetWindow()
        if self.win.IsEnabled():
            result = False
            self.text = self.win.GetValue()
            if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", self.text) or len(self.text) == 0:
                result = True
            else:
                result = False
                self.WxErrorDialog(u"Email invalide")

            if self.obligatoire and result:
                if len(self.text) > 0:
                    result = True
                else:
                    result = False
                    self.WxErrorDialog("Champ obligatoire")
            if result:
                self.WxClearErrorDialog()
        else:
            result = True

        return result


class LoginValidator(BaseValidator):

    def __init__(self, liste_logins, longueur_min=5, *args, **kwargs):
        self.liste_logins = liste_logins
        self.longueur_min = longueur_min
        BaseValidator.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return LoginValidator(self.liste_logins, self.longueur_min)

    def Validate(self, win):
        self.win = self.GetWindow()
        if self.win.IsEnabled():
            result = False
            self.text = self.win.GetValue()

            if len(self.text) >= self.longueur_min:
                if self.text not in self.liste_logins:
                    if re.search("^[a-z0-9.\-_]+$", self.text, re.IGNORECASE):
                        result = True
                    else:
                        result = False
                        self.WxErrorDialog("Seules les lettres, les chiffres, et les caractères ._- sont autorisés.")
                else:
                    result = False
                    self.WxErrorDialog("Ce login est déjà utilisé")
            else:
                result = False
                self.WxErrorDialog(u"La longueur minimale du login est de %s caractères." % self.longueur_min)

            if self.obligatoire and result:
                if len(self.text) > 0:
                    result = True
                else:
                    result = False
                    self.WxErrorDialog("Champ obligatoire")

            if result:
                self.WxClearErrorDialog()
        else:
            result = True

        return result

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255 or chr(key) in string.letters + string.digits + ".-_":
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return


class MotDePasseValidator(BaseValidator):

    def __init__(self, txtctrl_confirm, longueur_min=5, *args, **kwargs):
        self.longueur_min = longueur_min
        self.txtctrl_confirm = txtctrl_confirm
        BaseValidator.__init__(self, *args, **kwargs)

    def Clone(self):
        return MotDePasseValidator(txtctrl_confirm=self.txtctrl_confirm, longueur_min=self.longueur_min, obligatoire=self.obligatoire)

    def Validate(self, win):
        self.win = self.GetWindow()

        if self.win.IsEnabled() and len(self.win.GetValue()) > 0:
            result = False
            self.text = self.win.GetValue()
            if len(self.text) < self.longueur_min:
                self.WxErrorDialog(u"Le mot de passe n'est pas assez long (%s caractères minimum)" % self.longueur_min)
            else:
                if self.text != self.txtctrl_confirm.GetValue():
                    self.WxErrorDialog(u"Erreur dans la confirmation du mot de passe.", self.txtctrl_confirm)
                else:
                    result = True

            if self.obligatoire and result:
                if len(self.text) > 0:
                    result = True
                else:
                    result = False
                    self.WxErrorDialog("Champ obligatoire")

            if result:
                self.WxClearErrorDialog()
        else:
            result = True

        return result
