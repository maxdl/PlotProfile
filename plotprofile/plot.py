#!/usr/bin/env python3
import matplotlib.pyplot as plt
import os.path


class Profile(object):
    def __init__(self, input_fn, opt):
        self.input_fn = input_fn
        self.opt = opt
        self.src_coord_file = ""
        self.src_img = ""
        self.id = ""
        self.pixelwidth = 0
        self.metric_unit = ""
        self.pospro = ""
        self.prepro = ""
        self.profile_type = ""
        self.posm = []
        self.prsm = []
        self.posloc = []
        self.path = []
        self.pli = []
        self.spli = []
        self.lpli = []
        self.randomli = []
        self.psdli = []
        self.vesli = []
        self.clusterli = []
        self.s_clusterli = []
        self.l_clusterli = []
        self.mcli = []
        self.s_mcli = []
        self.l_mcli = []
        self.holeli = []
        self.warning = ''

    def to_metric_units(self, p):
        return [p[0] * self.pixelwidth, p[1] * self.pixelwidth]

    def get_coords(self, strli, type='point'):
        if not strli:
            return []
        pointli = []
        s = strli.pop(0).replace('\n', '').replace(' ', '').strip()
        while s != 'END':
            try:
                p = [float(s.split(',')[0]), float(s.split(',')[1])]
                if pointli and (p == pointli[-1]):
                    raise ProfileError("Duplicate coordinates: discarding second instance\n")
                else:
                    if self.opt.scale == 'metric':
                        p = self.to_metric_units(p)
                    pointli.append(p)
            except ValueError:
                if s[0] != '#':
                    raise ProfileError("'%s' not valid coordinates" % s)
                else:
                    pass
            s = strli.pop(0).replace('\n', '').strip()
        # For some reason, sometimes the end nodes have the same coordinates;
        # in that case, delete the last end node to avoid division by zero
        if (len(pointli) > 1) and (pointli[0] == pointli[-1]):
            del pointli[-1]
        if type == 'closed_path':
            pointli.append(pointli[0])
        return pointli

    def parse(self):
        """ Parse self data from input file 
        """
        li = read_file(self.input_fn)
        if not li:
            raise ProfileError("Could not open input file")
        while li:
            s = li.pop(0).replace('\n', '').strip()
            if s.split(' ')[0].upper() in ('PROFILE_ID', 'COMMENT', 'PROFILE_TYPE',
                                           'PRESYNAPTIC_PROFILE', 'POSTSYNAPTIC_PROFILE'):
                pass       # These are valid entries but not used here, so just skip
            elif s.split(' ')[0].upper() == 'INPUT_FILE':
                self.src_coord_file = s.lstrip('INPUT_FILE ')
            elif s.split(' ')[0].upper() == 'IMAGE':
                self.src_img = s.split(' ')[1]
            elif s.split(' ')[0].upper() == 'PIXELWIDTH':
                try:
                    self.pixelwidth = float(s.split(' ')[1])
                    self.metric_unit = s.split(' ')[2]
                except (IndexError, ValueError):
                    raise ProfileError("PIXELWIDTH is not a valid number")
            elif s.split(' ')[0].upper() == 'POSLOC':
                try:
                    x, y = s.split(' ', 1)[1].split(', ')
                    self.posloc = self.to_metric_units([float(x), float(y)])
                except (IndexError, ValueError):
                    raise ProfileError(self, "POSLOC not valid")
            elif s.upper() == "POSTSYNAPTIC_ELEMENT":
                self.posm = self.get_coords(li, 'open_path')
            elif s.upper() == "PRESYNAPTIC_ELEMENT":
                self.prsm = self.get_coords(li, 'open_path')
            elif s.upper() == "PATH":
                self.path = self.get_coords(li, 'open_path')
            elif s.upper() in ("PLASMA_MEMBRANE", "PROFILE_BORDER"):
                self.path = self.get_coords(li, 'closed_path')
                self.path.append(self.path[0])
            elif s.upper() in ("POSTSYNAPTIC_DENSITY", "PSD_OR_ACTIVE_ZONE", "PSD"):
                self.psdli.append(self.get_coords(li))
            elif s.upper() == "VESICLE":
                self.vesli.append(self.get_coords(li, 'closed_path'))
                self.vesli[-1].append(self.vesli[-1][0])
            elif s.upper() in ("PROFILE_HOLE", "HOLE"):
                self.holeli.append(self.get_coords(li, 'closed_path'))
                self.holeli[-1].append(self.holeli[-1][0])
            elif s.upper() in ("POINTS", "PARTICLES"):
                self.pli = self.get_coords(li, 'point')
            elif s.upper() == "SMALL_PARTICLES":
                self.spli = self.get_coords(li, 'point')
            elif s.upper() == "LARGE_PARTICLES":
                self.lpli = self.get_coords(li, 'point')
            elif s.upper() == "RANDOM_POINTS":
                self.randomli = self.get_coords(li)
            elif s.split(' ')[0].upper() == 'CLUSTER_CONVEX_HULL':
                self.clusterli.append(self.get_coords(li, 'closed_path'))
            elif s.split(' ')[0].upper() == 'CLUSTER_CONVEX_HULL_SMALL':
                self.s_clusterli.append(self.get_coords(li, 'closed_path'))
            elif s.split(' ')[0].upper() == 'CLUSTER_CONVEX_HULL_LARGE':
                self.l_clusterli.append(self.get_coords(li, 'closed_path'))
            elif s.split(' ')[0].upper() == 'MONTE_CARLO':
                self.mcli.append(self.get_coords(li))
            elif s.split(' ')[0].upper() == 'MONTE_CARLO_SMALL':
                self.s_mcli.append(self.get_coords(li))
            elif s.split(' ')[0].upper() == 'MONTE_CARLO_LARGE':
                self.l_mcli.append(self.get_coords(li))
            elif s.upper() == 'GRID':
                # Retrieve coordinates to dummy variable as they will not be used
                raise ProfileError("Grid found; however, grids are no longer supported.")
            elif s[0] != "#":  # unless specifically commented out
                raise ProfileError("Unrecognized string '" + s + "' in input file")

    def plot(self):
        def plot_component(li, core_properties, **args):
            if not li:
                return
            x, y = zip(*li)
            plt.plot(x, y, core_properties, **args)

        plt.clf()
        plt.title(os.path.basename(self.input_fn), size='small')
        if self.opt.scale == 'metric':
            axis_label = self.metric_unit
        else:
            axis_label = 'pixels'
        plt.ylabel(axis_label)
        plt.xlabel(axis_label)
        plot_component(self.posm, 'b-')
        plot_component(self.prsm, 'g-')
        plot_component(self.path, 'b-')
        if self.posloc:
            plot_component([self.posloc], 'Pg')
        for psd in self.psdli:
            plot_component(psd, 'm-')
        for v in self.vesli:
            plot_component(v, 'g-')
        for hole in self.holeli:
            plot_component(hole, 'r-')
        if self.opt.plot_cluster_convex_hulls:
            for cluster in self.clusterli:
                plot_component(cluster, 'k-', alpha=0.5)
            for cluster in self.s_clusterli:
                plot_component(cluster, 'k-', alpha=0.5)
            for cluster in self.l_clusterli:
                plot_component(cluster, 'k-', alpha=0.5)
        plot_component(self.pli, 'ko', markersize=3)
        plot_component(self.spli, 'ko', markersize=2)
        plot_component(self.lpli, 'go', markersize=4)
        if self.opt.plot_random_points:
            plot_component(self.randomli, 'y+', alpha=0.5, markersize=3)
        if self.opt.plot_simulated_points:
            for mc in self.mcli:
                plot_component(mc, 'co', alpha=0.2, markersize=1)
            for mc in self.s_mcli:
                plot_component(mc, 'ko', alpha=0.1, markersize=1)
            for mc in self.l_mcli:
                plot_component(mc, 'go', alpha=0.1, markersize=4)
        if self.opt.invert_y_axis:
            plt.gca().invert_yaxis()
        plt.show()


class ProfileError(Exception):
    def __init__(self, msg):
        self.msg = msg + "."


def read_file(fname):
    """Open file fname and read its lines into a list"""
    try:
        f = open(fname, 'r')
        try:
            s = f.readlines()
        finally:
            f.close()
    except IOError:
        raise ProfileError("File not found or unreadable")
    return s


def main(input_fn, opt):
    try:
        profile = Profile(input_fn, opt)
        profile.parse()
        profile.plot()
    except ProfileError as err:
        return 1, err.msg
    return 0, ""

