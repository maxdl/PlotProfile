import configparser
import os
import os.path
import sys
import wx
from . import plot
from . import gui
from . import options
from . import stringconv
from . import version


class Frame(gui.MainFrame):
    def __init__(self, parent):
        gui.MainFrame.__init__(self, parent)
        self.SetTitle(version.title)
        self.SetIcon(wx.Icon(version.icon, wx.BITMAP_TYPE_ICO))
        self.set_win7_taskbar_icon()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        dt = FileDropTarget(self)
        self.InputPanel.SetDropTarget(dt)
        self.opt = options.OptionData()
        self.configfn = os.path.normpath(os.path.expanduser('~/.%s.cfg' % version.title.lower()))
        self.get_input_dir_from_config()
        self.load_options_from_config()
        self.set_options_in_ui()
        self.Fit()

    @staticmethod
    def set_win7_taskbar_icon():
        """ A hack to make the icon visible in the taskbar in Windows 7.
            From http://stackoverflow.com/a/1552105/674475.
        """
        if sys.platform == "win32":
            import ctypes
            appid = 'PlotProfile'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    def OnPlotButton(self, event):

        def find_in_dict(s, di):
            for key, val in di.items():
                if key.find(s) != -1 and val:
                    return True
            return False

        if not self.SelectFilePicker.GetPath():
            self.show_warning("No file to plot.")
            return
        self.set_options_from_ui()
        exitcode, msg = plot.main(self.input_fn, self.opt)
        if exitcode == 1:
            self.show_error(msg)
        elif exitcode == 2:
            self.show_warning(msg)

    def OnSaveOptionsButton(self, event):
        if self.save_options_to_config():
            self.show_message("Current options saved to '%s'." % self.configfn)

    def OnAboutButton(self, event):
        dlg = AboutDialog(self)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def OnClose(self, event):
        self.save_input_dir_to_config()
        self.Destroy()

#
#   utilities
#
    def save_input_dir_to_config(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.configfn)
        except (configparser.ParsingError, configparser.MissingSectionHeaderError):
            pass  # Silently suppress parsing errors at this stage
        if 'Previous session' not in config.sections():
            config['Previous session'] = {}
        config['Previous session']['input_dir'] = os.getcwd()
        try:
            with open(self.configfn, 'w') as f:
                config.write(f)
        except IOError:
            self.show_error("Configuration file\n(%s)\ncould not be saved."
                             % self.configfn)

    def get_input_dir_from_config(self):
        config = configparser.ConfigParser()
        if not os.path.exists(self.configfn):
            return
        try:
            config.read(self.configfn)
        except (configparser.ParsingError, configparser.MissingSectionHeaderError):
            pass    # Silently suppress parsing errors at this stage
        try:
            inputdir = config['Previous session']['input_dir']
        except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
            self.show_warning("Configuration file '%s' is invalid.\n Using "
                              "current working directory." % self.configfn)
            return
        try:
            if not os.path.isdir(inputdir):
                raise IOError
            os.chdir(inputdir)
        except (IOError, TypeError):
            self.show_warning("Invalid input directory' %s' in configuration "
                              "file '%s'.\n Using current working directory."
                              % (inputdir, self.configfn))

    def save_options_to_config(self):

        def set_option(option):
            nonlocal config
            config['Options'][option] = str(getattr(self.opt, option))

        self.set_options_from_ui()
        config = configparser.ConfigParser()
        try:
            config.read(self.configfn)
        except (configparser.ParsingError, configparser.MissingSectionHeaderError):
            pass  # Silently suppress parsing errors at this stage
        if 'Options' not in config.sections():
            config['Options'] = {}
        set_option('scale')
        set_option('invert_y_axis')
        set_option('plot_simulated_points')
        set_option('plot_random_points')
        set_option('plot_cluster_convex_hulls')
        try:
            with open(self.configfn, 'w') as f:
                config.write(f)
        except IOError:
            self.show_warning("Configuration file\n(%s)\ncould not be saved." % self.configfn)
        return True

    def load_options_from_config(self):

        def show_invalid_option_warning(invalid_opt):
            self.show_warning("Invalid value '%s' for option '%s' in "
                              "configuration file '%s'.\nUsing default value."
                              % (getattr(self.opt, invalid_opt), invalid_opt,
                                 self.configfn))

        def check_str_option(opt, valid_strings=()):
            if getattr(self.opt, opt) not in valid_strings:
                show_invalid_option_warning(opt)
                setattr(self.opt, opt, getattr(defaults, opt))

        def check_bool_option(opt):
            try:
                setattr(self.opt, opt, stringconv.str_to_bool(getattr(self.opt, opt)))
            except ValueError:
                show_invalid_option_warning(opt)
                setattr(self.opt, opt, getattr(defaults, opt))

        config = configparser.ConfigParser()
        if not os.path.exists(self.configfn):
            return
        try:
            config.read(self.configfn)
        except (configparser.ParsingError, configparser.MissingSectionHeaderError):
            return     # Silently suppress parsing errors at this stage
        if 'Options' not in config.sections():
            return     # No options present in config file; silently use defaults
        defaults = options.OptionData()
        for option in config.options('Options'):
            if '.' in option:
                option_dict, option_key = option.split('.', 1)
                option_key = option_key.replace("_", " ")
                try:
                    getattr(self.opt,
                            option_dict)[option_key] = config.get('Options', option)
                except AttributeError:
                    pass   # So, attribute is invalid, but continue silently
            else:
                setattr(self.opt, option, config.get('Options', option))
        check_str_option('scale', ('metric', 'pixel'))
        check_bool_option('invert_y_axis')
        check_bool_option('plot_simulated_points')
        check_bool_option('plot_random_points')
        check_bool_option('plot_cluster_convex_hulls')

    def set_options_in_ui(self):
        if self.opt.scale == 'metric units':
            self.ScaleRadioBox.SetStringSelection('Metric units')
        else:
            self.ScaleRadioBox.SetStringSelection('Pixel units')
        self.InvertYAxisCheckBox.SetValue(self.opt.invert_y_axis)
        self.InvertYAxisCheckBox.SetValue(self.opt.invert_y_axis)
        self.SimulatedCheckBox.SetValue(self.opt.plot_simulated_points)
        self.RandomCheckBox.SetValue(self.opt.plot_random_points)
        self.ClusterCheckBox.SetValue(self.opt.plot_cluster_convex_hulls)

    def set_options_from_ui(self):
        self.input_fn = self.SelectFilePicker.GetPath()
        if self.ScaleRadioBox.GetStringSelection() == 'Metric units':
            self.opt.scale = 'metric'
        else:
            self.opt.scale = 'pixel'
        self.opt.invert_y_axis = self.InvertYAxisCheckBox.GetValue()
        self.opt.plot_simulated_points = self.SimulatedCheckBox.GetValue()
        self.opt.plot_random_points = self.RandomCheckBox.GetValue()
        self.opt.plot_cluster_convex_hulls = self.ClusterCheckBox.GetValue()

    def show_message(self, s):
        dlg = wx.MessageDialog(self, s, version.title, wx.OK | wx.ICON_INFORMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def show_warning(self, s):
        dlg = wx.MessageDialog(self, s, version.title, wx.OK | wx.ICON_EXCLAMATION)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()

    def show_error(self, s):
        dlg = wx.MessageDialog(self, s, version.title, wx.OK | wx.ICON_ERROR)
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()


class FileDropTarget(wx.FileDropTarget):

    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, x, y, fli):
        if len(fli) > 1:
            self.parent.show_error('Only one file can be plotted at a time.')
        elif os.path.isdir(fli[0]):
            self.parent.show_error('Folders cannot be selected.')
        elif os.path.splitext(fli[0])[1] not in ('.dtp', '.d2p', '.pd', '.pdd', '.pds', '.syn',
                                                 '.ves'):
            self.parent.show_error('File extension not recognized.')
        else:
            self.parent.inputfn = fli[0]
            self.parent.SelectFilePicker.SetPath(fli[0])
        return True


class AboutDialog(gui.AboutDialog):

    def __init__(self, parent):
        gui.AboutDialog.__init__(self, parent)
        self.TitleLabel.SetLabel(version.title)
        self.IconBitmap.SetBitmap(wx.Bitmap(version.icon, wx.BITMAP_TYPE_ANY))
        self.VersionLabel.SetLabel("Version %s" % version.version)
        self.LastModLabel.SetLabel("Last modified %s %s, %s." % version.date)
        self.CopyrightLabel.SetLabel("Copyright %s %s." % (version.date[2], version.author))
        self.LicenseLabel.SetLabel("Released under the terms of the MIT"
                                   " license.")
        self.EmailHyperlink.SetLabel("%s" % version.email)
        self.EmailHyperlink.SetURL("mailto://%s" % version.email)
        self.WebHyperlink.SetLabel("http://%s" % version.homepage)
        self.WebHyperlink.SetURL("http://%s" % version.homepage)
        self.SetIcon(wx.Icon(version.icon, wx.BITMAP_TYPE_ICO))
        self.Fit()

    def OnClose(self, event):
        self.Destroy()


