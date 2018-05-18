# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May  9 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"PlotProfile", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        MainSizer = wx.GridSizer( 0, 2, 0, 0 )
        
        self.InputPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.InputPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        InputSizer = wx.FlexGridSizer( 0, 1, 0, 0 )
        InputSizer.AddGrowableRow( 2 )
        InputSizer.SetFlexibleDirection( wx.BOTH )
        InputSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.SelectFileText = wx.StaticText( self.InputPanel, wx.ID_ANY, u"Select coordinate file:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.SelectFileText.Wrap( -1 )
        InputSizer.Add( self.SelectFileText, 0, wx.ALL, 5 )
        
        self.SelectFilePicker = wx.FilePickerCtrl( self.InputPanel, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.dtp;*.d2p;*.pd;*.pdd;*.pds;*.syn;*.ves", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_OPEN )
        InputSizer.Add( self.SelectFilePicker, 0, wx.ALL, 5 )
        
        ButtonSizer = wx.FlexGridSizer( 2, 2, 0, 0 )
        ButtonSizer.SetFlexibleDirection( wx.BOTH )
        ButtonSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.SpacerLabel = wx.StaticText( self.InputPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.SpacerLabel.Wrap( -1 )
        ButtonSizer.Add( self.SpacerLabel, 0, wx.ALL, 5 )
        
        self.PlotButton = wx.Button( self.InputPanel, wx.ID_ANY, u"Plot!", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.PlotButton, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
        
        self.AboutButton = wx.Button( self.InputPanel, wx.ID_ANY, u"About...", wx.DefaultPosition, wx.DefaultSize, 0 )
        ButtonSizer.Add( self.AboutButton, 1, wx.ALL, 5 )
        
        self.ExitButton = wx.Button( self.InputPanel, wx.ID_ANY, u"Exit", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        ButtonSizer.Add( self.ExitButton, 0, wx.ALL, 5 )
        
        
        InputSizer.Add( ButtonSizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )
        
        
        self.InputPanel.SetSizer( InputSizer )
        self.InputPanel.Layout()
        InputSizer.Fit( self.InputPanel )
        MainSizer.Add( self.InputPanel, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.OptionsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.OptionsPanel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        OptionsSizer = wx.StaticBoxSizer( wx.StaticBox( self.OptionsPanel, wx.ID_ANY, u"Options" ), wx.VERTICAL )
        
        ScaleRadioBoxChoices = [ u"Metric units", u"Pixel units" ]
        self.ScaleRadioBox = wx.RadioBox( OptionsSizer.GetStaticBox(), wx.ID_ANY, u"Scale", wx.DefaultPosition, wx.DefaultSize, ScaleRadioBoxChoices, 1, wx.RA_SPECIFY_COLS )
        self.ScaleRadioBox.SetSelection( 0 )
        self.ScaleRadioBox.SetToolTip( u"Choose whether to use metric scale (as specified in input file)\nor pixel scale" )
        
        OptionsSizer.Add( self.ScaleRadioBox, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.InvertYAxisCheckBox = wx.CheckBox( OptionsSizer.GetStaticBox(), wx.ID_ANY, u"Invert Y axis", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.InvertYAxisCheckBox.SetValue(True) 
        self.InvertYAxisCheckBox.SetToolTip( u"Invert the Y axis, such that origo is in the upper left corner.\nThus, the profile is plotted in the same orientation as that\nin the original image." )
        
        OptionsSizer.Add( self.InvertYAxisCheckBox, 0, wx.ALL, 5 )
        
        self.SimulatedCheckBox = wx.CheckBox( OptionsSizer.GetStaticBox(), wx.ID_ANY, u"Plot Monte Carlo simulated points", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.SimulatedCheckBox.SetToolTip( u"Plot simulated points if available" )
        
        OptionsSizer.Add( self.SimulatedCheckBox, 0, wx.ALL, 5 )
        
        self.RandomCheckBox = wx.CheckBox( OptionsSizer.GetStaticBox(), wx.ID_ANY, u"Plot random points", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.RandomCheckBox.SetToolTip( u"Plot random points if available" )
        
        OptionsSizer.Add( self.RandomCheckBox, 0, wx.ALL, 5 )
        
        self.SaveOptionsButton = wx.Button( OptionsSizer.GetStaticBox(), wx.ID_ANY, u"Save options", wx.DefaultPosition, wx.DefaultSize, 0 )
        OptionsSizer.Add( self.SaveOptionsButton, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        
        self.OptionsPanel.SetSizer( OptionsSizer )
        self.OptionsPanel.Layout()
        OptionsSizer.Fit( self.OptionsPanel )
        MainSizer.Add( self.OptionsPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( MainSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.PlotButton.Bind( wx.EVT_BUTTON, self.OnPlotButton )
        self.AboutButton.Bind( wx.EVT_BUTTON, self.OnAboutButton )
        self.ExitButton.Bind( wx.EVT_BUTTON, self.OnClose )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def OnPlotButton( self, event ):
        event.Skip()
    
    def OnAboutButton( self, event ):
        event.Skip()
    
    def OnClose( self, event ):
        event.Skip()
    

###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        
        fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer3.AddGrowableRow( 2 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        fgSizer4 = wx.FlexGridSizer( 0, 2, 10, 10 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.InitialSpaceSizer = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.InitialSpaceSizer.Wrap( -1 )
        fgSizer4.Add( self.InitialSpaceSizer, 0, wx.ALL, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        fgSizer5 = wx.FlexGridSizer( 1, 3, 0, 0 )
        fgSizer5.AddGrowableCol( 2 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.IconBitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer5.Add( self.IconBitmap, 0, wx.ALL, 5 )
        
        self.SmallSpacer = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.SmallSpacer.Wrap( -1 )
        fgSizer5.Add( self.SmallSpacer, 0, wx.ALL, 5 )
        
        self.TitleLabel = wx.StaticText( self, wx.ID_ANY, u"TitleLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.TitleLabel.Wrap( -1 )
        self.TitleLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        
        fgSizer5.Add( self.TitleLabel, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        fgSizer4.Add( fgSizer5, 1, wx.EXPAND|wx.RIGHT, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.VersionLabel = wx.StaticText( self, wx.ID_ANY, u"VersionLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.VersionLabel.Wrap( -1 )
        self.VersionLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        
        fgSizer4.Add( self.VersionLabel, 0, wx.ALIGN_BOTTOM|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.LastModLabel = wx.StaticText( self, wx.ID_ANY, u"LastModLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LastModLabel.Wrap( -1 )
        fgSizer4.Add( self.LastModLabel, 0, wx.RIGHT|wx.LEFT, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.CopyrightLabel = wx.StaticText( self, wx.ID_ANY, u"CopyrightLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.CopyrightLabel.Wrap( -1 )
        fgSizer4.Add( self.CopyrightLabel, 0, wx.RIGHT|wx.LEFT, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.LicenseLabel = wx.StaticText( self, wx.ID_ANY, u"LicenseLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LicenseLabel.Wrap( -1 )
        fgSizer4.Add( self.LicenseLabel, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        fgSizer6 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer6.AddGrowableCol( 1 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.EmailLabel = wx.StaticText( self, wx.ID_ANY, u"E-mail:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.EmailLabel.Wrap( -1 )
        fgSizer6.Add( self.EmailLabel, 0, wx.ALL, 5 )
        
        self.EmailHyperlink = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"EmailHyperlink", u"http://www.wxformbuilder.org", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        fgSizer6.Add( self.EmailHyperlink, 0, wx.ALL, 5 )
        
        self.WebLabel = wx.StaticText( self, wx.ID_ANY, u"Web:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.WebLabel.Wrap( -1 )
        fgSizer6.Add( self.WebLabel, 0, wx.ALL, 5 )
        
        self.WebHyperlink = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"WebHyperlink", u"http://www.wxformbuilder.org", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        fgSizer6.Add( self.WebHyperlink, 0, wx.ALL, 5 )
        
        
        fgSizer4.Add( fgSizer6, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT, 5 )
        
        
        fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        fgSizer3.Add( fgSizer4, 1, wx.EXPAND, 5 )
        
        self.Staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        fgSizer3.Add( self.Staticline, 0, wx.EXPAND|wx.ALL, 5 )
        
        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
        m_sdbSizer1.Realize();
        
        fgSizer3.Add( m_sdbSizer1, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        self.SetSizer( fgSizer3 )
        self.Layout()
        fgSizer3.Fit( self )
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    

