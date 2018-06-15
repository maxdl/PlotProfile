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
        self.input_fn = ''
        self.batch_input_dir = ''
        self.configfn = os.path.normpath(os.path.expanduser('~/.%s.cfg' % version.title.lower()))
        self.get_input_dir_from_config()
        self.load_options_from_config()
        self.set_options_in_ui()
        self.SelectFilePicker.SetInitialDirectory(os.getcwd())
        self.InputDirPicker.SetInitialDirectory(os.getcwd())
        self.OutputDirPicker.SetInitialDirectory(os.getcwd())
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

    def OnPlotSelectedButton(self, event):
        if not self.SelectFilePicker.GetPath():
            self.show_warning("No file to plot.")
            return
        self.do_plot(batch_mode=False)

    def OnPlotNextButton(self, event):
        if not self.SelectFilePicker.GetPath():
            self.show_warning("No file to plot.")
            return
        folder, current_file = os.path.split(self.SelectFilePicker.GetPath())
        fileli = sorted([f for f in os.listdir(folder)
                         if os.path.splitext(f)[1] in options.extensions])
        next_file = fileli[(fileli.index(current_file) + 1) % len(fileli)]
        self.SelectFilePicker.SetPath(os.path.join(folder, next_file))
        self.do_plot(batch_mode=False)

    def OnBatchPlotButton(self, event):
        if not self.InputDirPicker.GetPath():
            self.show_warning("No input folder selected.")
            return
        self.do_plot(batch_mode=True)

    def OnOutputFormatChoice(self, event):
        use_png = "png" in self.OutputFormatChoice.GetStringSelection()
        self.OutputBackgroundLabel.Enable(use_png)
        self.OutputBackgroundChoice.Enable(use_png)
        self.OutputResolutionLabel.Enable(use_png)
        self.OutputResolutionSpinCtrl.Enable(use_png)

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

    def do_plot(self, batch_mode=False):

        def plot_file(fn):
            nonlocal n_err
            exitcode, exitmsg = plot.main(fn, self.opt, batch_mode)
            if exitcode == 1:
                self.show_error(exitmsg)
                n_err += 1
            elif exitcode == 2:
                self.show_warning(exitmsg)

        self.get_options_from_ui()
        n_err = 0
        if batch_mode:
            fileli = sorted([os.path.join(self.batch_input_dir, f)
                             for f in os.listdir(self.batch_input_dir)
                             if os.path.splitext(f)[1] in options.extensions])
            if not os.path.isabs(self.opt.batch_output_dir):
                self.opt.batch_output_dir = os.path.abspath(os.path.join(self.batch_input_dir,
                                                                         self.opt.batch_output_dir))
            if not os.path.exists(self.opt.batch_output_dir):
                os.mkdir(self.opt.batch_output_dir)
            for n, f in enumerate(fileli):
                self.StatusBar.SetStatusText("Batch plotting: %d %% done (processing %s)"
                                             % (n / len(fileli) * 100, os.path.basename(f)))
                plot_file(f)
                self.Update()
            self.StatusBar.SetStatusText("Batch plotting done.")
            msg = "%d plot(s) saved to %s." % (len(fileli) - n_err, self.opt.batch_output_dir)
            if n_err > 0:
                msg = msg + "\n%d file(s) generated errors and could not be plotted." % n_err
            self.show_message(msg)
            self.StatusBar.SetStatusText("")
        else:
            plot_file(self.input_fn)

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

        self.get_options_from_ui()
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
        set_option('output_format')
        set_option('output_background')
        set_option('output_resolution')
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

        def check_int_option(opt, min, max):
            try:
                setattr(self.opt, opt, int(getattr(self.opt, opt)))
                if not min <= int(getattr(self.opt, opt)) <= max:
                    raise ValueError
            except ValueError:
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
        check_str_option('output_format', ('eps', 'png', 'pdf', 'svg'))
        check_str_option('output_background', ('transparent', 'white'))
        check_int_option('output_resolution', min=1, max=1200)

    def set_options_in_ui(self):
        if self.opt.scale == 'metric':
            self.ScaleRadioBox.SetStringSelection('Metric units')
        else:
            self.ScaleRadioBox.SetStringSelection('Pixel units')
        self.InvertYAxisCheckBox.SetValue(self.opt.invert_y_axis)
        self.InvertYAxisCheckBox.SetValue(self.opt.invert_y_axis)
        self.SimulatedCheckBox.SetValue(self.opt.plot_simulated_points)
        self.RandomCheckBox.SetValue(self.opt.plot_random_points)
        self.ClusterCheckBox.SetValue(self.opt.plot_cluster_convex_hulls)
        if self.opt.output_format == 'eps':
            self.OutputFormatChoice.SetStringSelection('Encapsulated Postscript (.eps)')
        if self.opt.output_format == 'png':
            self.OutputFormatChoice.SetStringSelection('Portable Network Graphics (.png)')
        if self.opt.output_format == 'pdf':
            self.OutputFormatChoice.SetStringSelection('Portable Document Format (.pdf)')
        if self.opt.output_format == 'svg':
            self.OutputFormatChoice.SetStringSelection('Scalable Vector Graphics (.svg)')
        self.OutputBackgroundChoice.SetStringSelection(self.opt.output_background.capitalize())
        self.OutputResolutionSpinCtrl.SetValue(self.opt.output_resolution)
        use_png = "png" in self.OutputFormatChoice.GetStringSelection()
        self.OutputBackgroundLabel.Enable(use_png)
        self.OutputBackgroundChoice.Enable(use_png)
        self.OutputResolutionLabel.Enable(use_png)
        self.OutputResolutionSpinCtrl.Enable(use_png)

    def get_options_from_ui(self):
        self.input_fn = self.SelectFilePicker.GetPath()
        if self.ScaleRadioBox.GetStringSelection() == 'Metric units':
            self.opt.scale = 'metric'
        else:
            self.opt.scale = 'pixel'
        self.opt.invert_y_axis = self.InvertYAxisCheckBox.GetValue()
        self.opt.plot_simulated_points = self.SimulatedCheckBox.GetValue()
        self.opt.plot_random_points = self.RandomCheckBox.GetValue()
        self.opt.plot_cluster_convex_hulls = self.ClusterCheckBox.GetValue()
        if self.OutputFormatChoice.GetStringSelection() == 'Encapsulated Postscript (.eps)':
            self.opt.output_format = 'eps'
        if self.OutputFormatChoice.GetStringSelection() == 'Portable Network Graphics (.png)':
            self.opt.output_format = 'png'
        if self.OutputFormatChoice.GetStringSelection() == 'Portable Document Format (.pdf)':
            self.opt.output_format = 'pdf'
        if self.OutputFormatChoice.GetStringSelection() == 'Scalable Vector Graphics (.svg)':
            self.opt.output_format = 'svg'
        self.batch_input_dir = self.InputDirPicker.GetPath()
        self.opt.batch_output_dir = self.OutputDirPicker.GetPath()
        self.opt.output_background = self.OutputBackgroundChoice.GetStringSelection().lower()
        self.opt.output_resolution = self.OutputResolutionSpinCtrl.GetValue()

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

