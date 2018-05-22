#!/usr/bin/env python3
import matplotlib.pyplot as plt


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
        self.mcli = []
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
            if s.split(' ')[0].upper() == 'INPUT_FILE':
                self.src_coord_file = s.lstrip('INPUT_FILE ')
            elif s.split(' ')[0].upper() == 'IMAGE':
                self.src_img = s.split(' ')[1]
            elif s.split(' ')[0].upper() == 'PROFILE_ID':
                try:
                    self.id = int(s.split(' ')[1])
                except (IndexError, ValueError):
                    self.id = 0  # This is not really used so we silently suppress errors
            elif s.split(' ')[0].upper() == 'COMMENT':
                try:
                    self.comment = s.split(' ', 1)[1]
                except IndexError:
                    self.comment = ''
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
            elif s.upper() == "POSTSYNAPTIC_PROFILE":
                self.pospro = s.split(' ', 1)[1]
            elif s.upper() == "PRESYNAPTIC_PROFILE":
                self.prepro = s.split(' ', 1)[1]
            elif s.split(" ")[0].upper() == "PROFILE_TYPE":
                try:
                    self.profile_type = s.split(" ", 1)[1]
                except IndexError:
                    self.profile_type = ''
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
            elif s.split(' ')[0].upper() == 'MONTE_CARLO':
                self.mcli.append(self.get_coords(li))
            elif s.upper() == 'GRID':
                # Retrieve coordinates to dummy variable as they will not be used
                __ = self.get_coords(li)
                raise ProfileError("Grid found; however, grids are no longer supported.")
            elif s[0] != "#":  # unless specifically commented out
                raise ProfileError("Unrecognized string '" + s + "' in input file")

    def plot(self):
        plt.clf()
        plt.title(self.src_coord_file, size='small')
        if self.opt.scale == 'metric':
            axis_label = self.metric_unit
        else:
            axis_label = 'pixels'
        plt.ylabel(axis_label)
        plt.xlabel(axis_label)
        if self.posm:
            x, y = zip(*self.posm)
            plt.plot(x, y, 'b-')
        if self.prsm:
            x, y = zip(*self.prsm)
            plt.plot(x, y, 'g-')
        if self.path:
            x, y = zip(*self.path)
            plt.plot(x, y, 'b-')
        if self.posloc:
            plt.plot(self.posloc[0], self.posloc[1], 'Pg')
        for psd in self.psdli:
            x, y = zip(*psd)
            plt.plot(x, y, 'm-')
        for v in self.vesli:
            x, y = zip(*v)
            plt.plot(x, y, 'g-')
        for hole in self.holeli:
            x, y = zip(*hole)
            plt.plot(x, y, 'r-')
        if self.opt.plot_cluster_convex_hulls:
            for cluster in self.clusterli:
                x, y = zip(*cluster)
                plt.plot(x, y, 'k-', alpha=0.5)
        if self.pli:
            x, y = zip(*self.pli)
            plt.plot(x, y, 'ko', markersize=3)
        if self.spli:
            x, y = zip(*self.spli)
            plt.plot(x, y, 'ko', markersize=2)
        if self.lpli:
            x, y = zip(*self.lpli)
            plt.plot(x, y, 'go', markersize=4)
        if self.opt.plot_random_points and self.randomli:
            x, y = zip(*self.randomli)
            plt.plot(x, y, 'y+', alpha=0.5, markersize=3)
        if self.opt.plot_simulated_points:
            for mc in self.mcli:
                x, y = zip(*mc)
                plt.plot(x, y, "co", alpha=0.5, markersize=1)
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

