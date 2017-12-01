#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
try:
	from .common import *
except ImportError:
	from common import *


class Prefs(Gtk.Dialog):

	def __init__(self, parent):

		Gtk.Dialog.__init__(
			self, 'Preferences', parent, 0,
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
				Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_border_width(10)
		self.set_icon_name('grive-utils')
		self.connect('response', self.on_response)
		box = self.get_content_area()
		box.set_spacing(10)
		listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
		box.pack_start(listbox, True, True, 0)

		self.build(listbox)

		self.show_all()

	def build(self, listbox):

		self.interval = Gtk.SpinButton.new_with_range(0, 43200, 1)
		self.interval.set_value(CONFIG.getint('DEFAULT', 'Interval'))
		listbox.insert(
			self.get_row(
				'Check Google Drive every', self.interval, 'minutes'), -1)
		self.uprate = Gtk.SpinButton.new_with_range(0, 1048576, 1)
		self.uprate.set_value(CONFIG.getint('DEFAULT', 'UpRate'))
		listbox.insert(
			self.get_row(
				'Upload rate', self.uprate, 'kbps'), -1)
		self.downrate = Gtk.SpinButton.new_with_range(0, 1048576, 1)
		self.downrate.set_value(CONFIG.getint('DEFAULT', 'DownRate'))
		listbox.insert(
			self.get_row(
				'Download rate', self.downrate, 'kbps'), -1)
		self.notify = Gtk.Switch()
		self.notify.set_active(CONFIG.getboolean('DEFAULT', 'Notify'))
		listbox.insert(
			self.get_row(
				'Show notifications', self.notify), -1)
		self.light_panel = Gtk.Switch()
		self.light_panel.set_active(CONFIG.getboolean('DEFAULT', 'LightPanel'))
		listbox.insert(
			self.get_row(
				'Light panel theme', self.light_panel), -1)

	def get_row(self, label, widget, unit=None):

		row = Gtk.ListBoxRow(activatable=False)
		hbox = Gtk.Box(
			orientation=Gtk.Orientation.HORIZONTAL, spacing=10, border_width=10)
		row.add(hbox)
		hbox.pack_start(Gtk.Label(label), False, False, 0)
		if unit:
			hbox.pack_end(Gtk.Label(unit), False, False, 0)
		hbox.pack_end(widget, False, False, 0)
		return row

	def on_response(self, dialog, response):

		if response == Gtk.ResponseType.OK:
			CONFIG['DEFAULT']['Interval'] = str(self.interval.get_value_as_int())
			CONFIG['DEFAULT']['UpRate'] = str(self.uprate.get_value_as_int())
			CONFIG['DEFAULT']['DownRate'] = str(self.downrate.get_value_as_int())
			CONFIG['DEFAULT']['Notify'] = str(
				self.notify.get_active()).casefold()
			CONFIG['DEFAULT']['LightPanel'] = str(
				self.light_panel.get_active()).casefold()
			save_config()


class Fatal(Gtk.Dialog):

	def __init__(self, parent, title, message):

		Gtk.Dialog.__init__(
			self, title, parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_border_width(10)
		self.set_icon_name('grive-utils')
		box = self.get_content_area()
		box.set_spacing(10)
		label = Gtk.Label(message)
		box.pack_start(label, True, True, 0)
		self.show_all()


if __name__ == '__main__':
	Prefs(None).run()
