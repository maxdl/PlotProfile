#!/usr/bin/env python3

extensions = ['.dtp', '.d2p', '.pd', '.pdd', '.pds', '.syn', '.ves']


class OptionData(object):
	def __init__(self):
		self.input_dir = ''
		self.scale = 'metric'
		self.invert_y_axis = True
		self.plot_simulated_points = False
		self.plot_random_points = False
		self.plot_cluster_convex_hulls = False
		self.batch_output_dir = ''
		self.output_format = 'pdf'
		self.output_background = 'transparent'
		self.output_resolution = 300
