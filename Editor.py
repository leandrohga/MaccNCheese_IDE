#
# Copyright (C) 2016  Leandro Aguiar <leandrohgaguiar@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TextViewWindow(Gtk.Window):

	def __init__(self):
		# Create the window
		Gtk.Window.__init__(self, title="Basic Text Editor")
		self.set_default_size(500, 500)
		# Add a base grid
		self.grid = Gtk.Grid()
		self.add(self.grid)
		# Create the toolbar and the text area
		self.create_toolbar()
		self.create_textview()
		# Variables
		self.text_file = None
		self.text_file_name = None

	def create_toolbar(self):
		# Create toolbar and attach it to the grid
		toolbar = Gtk.Toolbar()
		self.grid.attach(toolbar, 0, 0, 3, 1)
		# Open file button
		button_openfile = Gtk.ToolButton()
		button_openfile.set_icon_name("document-open-symbolic")
		toolbar.insert(button_openfile, 0)
		button_openfile.connect("clicked", self.on_openfile_clicked)
		# Save file button
		button_savefile = Gtk.ToolButton()
		button_savefile.set_icon_name("document-save-symbolic")
		toolbar.insert(button_savefile, 1)
		button_savefile.connect("clicked", self.on_savefile_clicked)
		# 'Save file as' button
		button_saveas = Gtk.ToolButton()
		button_saveas.set_icon_name("document-save-as-symbolic")
		toolbar.insert(button_saveas, 2)
		button_saveas.connect("clicked", self.on_saveas_clicked)
		# Separator
		toolbar.insert(Gtk.SeparatorToolItem(), 3)
		# Edit-cut button
		button_editcut = Gtk.ToolButton()
		button_editcut.set_icon_name("edit-cut-symbolic")
		toolbar.insert(button_editcut, 4)
		# Edit-copy file button
		button_editcopy = Gtk.ToolButton()
		button_editcopy.set_icon_name("edit-copy-symbolic")
		toolbar.insert(button_editcopy, 5)
		# Edit-paste file button
		button_editpaste = Gtk.ToolButton()
		button_editpaste.set_icon_name("edit-paste-symbolic")
		toolbar.insert(button_editpaste, 6)
		# Separator
		toolbar.insert(Gtk.SeparatorToolItem(), 7)
		# Help button
		button_helpfaq = Gtk.ToolButton()
		button_helpfaq.set_icon_name("help-faq")
		toolbar.insert(button_helpfaq, 8)

	def create_textview(self):
		# Create a ScrolledWindow
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		self.grid.attach(scrolledwindow, 0, 1, 3, 1)
		# Create the TextView
		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("Please open a file or save this one.")
		scrolledwindow.add(self.textview)
		# Set the justification and wraping
		self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
		self.textview.set_justification(Gtk.Justification.LEFT)

	def on_openfile_clicked(self, widget):
		# Create a file chooser window
		file_chooser = Gtk.FileChooserDialog("Open file", self,
				Gtk.FileChooserAction.OPEN,
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
					Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.add_filters(file_chooser)
		# Run the file chooser window and check response
		response = file_chooser.run()
		# Read the file
		if response == Gtk.ResponseType.OK:
			self.read_text_file(file_chooser.get_filename())
		# Destroy dialog window
		file_chooser.destroy()

	def on_savefile_clicked(self, widget):
		# Check if it is a new file
		if self.text_file_name == None:
			# Ask for a name
			self.on_saveas_clicked(widget)
		else:
			# Save the file with the same name
			self.write_text_file(self.text_file_name)

	def on_saveas_clicked(self, widget):
		# Create a file chooser window
		file_chooser = Gtk.FileChooserDialog("Save file", self,
				Gtk.FileChooserAction.SAVE,
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
					Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		# Check default file name and ask before overwritting
		if self.text_file_name != None:
			file_chooser.set_filename(self.text_file_name)
		else:
			file_chooser.set_current_name("Untitled.mnc")
		file_chooser.set_do_overwrite_confirmation(True)
		# Run the file chooser window and check response
		response = file_chooser.run()
		# Write to the file
		if response == Gtk.ResponseType.OK:
			self.write_text_file(file_chooser.get_filename())
		# Destroy dialog window
		file_chooser.destroy()

	def read_text_file(self, file_name):
		# Open and read the file
		try:
			self.text_file = open(file_name, 'r')
		except IOError:
			print("Could not open the file.")
		else:
			self.text_file_name = file_name
			self.textbuffer.set_text(self.text_file.read())
			# Close the file
			self.text_file.close()
			self.text_file = None

	def write_text_file(self, file_name):
		# Open and write to the file
		try:
			self.text_file = open(file_name, 'w')
		except IOError:
			print("Could not open the file.")
		else:
			self.text_file_name = file_name
			start = self.textbuffer.get_start_iter()
			end = self.textbuffer.get_end_iter()
			self.text_file.write(self.textbuffer.get_text(
					start, end, False))
			# Close the file
			self.text_file.close()
			self.text_file = None

	def add_filters(self, dialog):
		# MaccNCheese files
		filter_mnc = Gtk.FileFilter()
		filter_mnc.set_name("MaccNCheese files")
		filter_mnc.add_pattern("*.mnc")
		dialog.add_filter(filter_mnc)
		# Test files
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)
		# Any file
		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)


if __name__ == "__main__":
	win = TextViewWindow()
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()
