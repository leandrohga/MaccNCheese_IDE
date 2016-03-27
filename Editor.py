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
		# Separator
		toolbar.insert(Gtk.SeparatorToolItem(), 2)
		# Edit-cut button
		button_editcut = Gtk.ToolButton()
		button_editcut.set_icon_name("edit-cut-symbolic")
		toolbar.insert(button_editcut, 3)
		# Edit-copy file button
		button_editcopy = Gtk.ToolButton()
		button_editcopy.set_icon_name("edit-copy-symbolic")
		toolbar.insert(button_editcopy, 4)
		# Edit-paste file button
		button_editpaste = Gtk.ToolButton()
		button_editpaste.set_icon_name("edit-paste-symbolic")
		toolbar.insert(button_editpaste, 5)
		# Separator
		toolbar.insert(Gtk.SeparatorToolItem(), 6)
		# Help button
		button_helpfaq = Gtk.ToolButton()
		button_helpfaq.set_icon_name("help-faq")
		toolbar.insert(button_helpfaq, 7)

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
		# Run the file chooser window and check response
		response = file_chooser.run()
		if response == Gtk.ResponseType.OK:
			# Open and read the file
			# TODO: make sure the file was openned, check for errors
			self.text_file = open(file_chooser.get_filename(), 'r')
			self.textbuffer.set_text(self.text_file.read())
			# Close the file
			self.text_file.close()
			self.text_file = None
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")
		# Destroy dialog window

		file_chooser.destroy()


if __name__ == "__main__":
	win = TextViewWindow()
	win.connect("delete-event", Gtk.main_quit)
	win.show_all()
	Gtk.main()
