import wx

class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "LabelBook Demo")

        # Possible values for Tab placement are INB_TOP, INB_BOTTOM, INB_RIGHT, INB_LEFT

        solid = wx.EmptyBitmap(200,50,-1)
        croix = wx.Bitmap("../../icons/16x16/ajouter.ico")
        dc = wx.MemoryDC()
        dc.SelectObject(solid)
        """solidbrush = wx.Brush(wx.Colour(75,75,75),wx.SOLID)
        solidpen = wx.Pen(wx.Colour(75,75,75),wx.SOLID)
        dc.SetBrush(solidbrush)
        dc.SetPen(solidpen)
        dc.DrawRectangle(0, 0, 200, 50)
        dc.SetTextForeground(wx.Colour(255, 255, 255))"""
        dc.DrawText("Coucou", 0,  0)
        dc.SelectObject(wx.NullBitmap)

        """self.checked = wx.Image('buttonchecked.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        dc = wx.MemoryDC()
        dc.SelectObject(self.checked)
        dc.SetTextForeground(wx.Colour(200, 255, 0))
        dc.DrawText(line.rstrip(), 30,  17)
        dc.SelectObject(wx.NullBitmap)"""

        self.b = wx.BitmapButton(self, 800, solid)


# our normal wxApp-derived class, as usual

app = wx.PySimpleApp()

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()