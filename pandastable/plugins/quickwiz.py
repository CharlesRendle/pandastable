#!/usr/bin/env python
"""
    DataExplore Application plugin example.
    Created Oct 2015
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from __future__ import absolute_import, division, print_function
from copyreg import constructor
from tkinter import *
import tkinter
from typing import final

from pyparsing import col
try:
    from tkinter.ttk import *
except:
    from ttk import *
from pandastable.plugin import Plugin

class QuickWiz(Plugin):
    """Template plugin for DataExplore"""

    #uncomment capabilities list to appear in menu
    capabilities = ['gui']
    requires = ['']
    menuentry = 'QuickWiz'


    def main(self, parent):
        """Customise this or _doFrame for your widgets"""

        if parent==None:
            return
        self.parent = parent
        self.parentframe = None

        self._doFrame()
        #self._doFrame2()
        return

    def _doFrame(self):

        if 'uses_sidepane' in self.capabilities:
            self.table = self.parent.getCurrentTable()
            self.mainwin = Frame(self.table.parentframe)
            self.mainwin.grid(row=6,column=0,columnspan=4,sticky='news')
        else:
            self.mainwin=Toplevel()
            self.mainwin.title('QuickWiz')
            self.mainwin.geometry('600x600+200+100')

        self.ID='Basic Plugin'

        notebook = Notebook(self.mainwin)
        notebook.pack(fill='both', expand=True)

        # Starting frame from where the user can begin tutorials or open
        # the glossary.
        def home():
            return Frame(notebook)

        home_frame = home()

        # Frame for capturing the observations
        def obs():
            obs_frame = Frame(notebook)

            label1 = Label(obs_frame, text='Bag Selectors:')
            label1.grid(column=0, row=3)

            start_cell = Button(obs_frame, text ="Start Cell", command=(lambda: self.startCell(obs_frame)))
            start_cell.grid(column=0, row=4)
            end_cell = Button(obs_frame, text ="End Cell", command=(lambda: self.endCell(obs_frame)))
            end_cell.grid(column=1, row=4)
            cell_range = Button(obs_frame, text ="Cell Range")
            cell_range.grid(column=2, row=4)
            direction = Button(obs_frame, text ="Direction")
            direction.grid(column=0, row=5)
            col_fill = Button(obs_frame, text ="Column Fill")
            col_fill.grid(column=1, row=5)
            row_fill = Button(obs_frame, text ="Row Fill")
            row_fill.grid(column=2, row=5)

            label2 = Label(obs_frame, text='Bag Filters:')
            label2.grid(column=0, row=7)

            remove_blanks = Button(obs_frame, text ="Remove Blanks")
            remove_blanks.grid(column=0, row=8)

            return obs_frame

        obs_frame = obs()


        # Frame for capturing the other data set components
        # Contains another notebook frame from which new components can be added. 
        def dims():
            dims_frame = Frame(notebook)
            return dims_frame

        dims_frame = dims()

        def handleTabChange(event):
        # Function which creates a new tab when the last tab is clicked.
        # This allows the user to add new component selections.
        # Functionality taken from https://stackoverflow.com/questions/71859022/tkinter-notebook-create-new-tabs-by-clicking-on-a-plus-tab-like-every-web-brow
            
            if notebook2.select() == notebook2.tabs()[-1]:
                index = len(notebook2.tabs())-1
                new_dim_frame = Frame(notebook2)
                    
                self.mainwin=Toplevel()
                self.mainwin.title('Add New Component')
                self.mainwin.geometry('300x100+200+100')

                label = Label(self.mainwin, text="New Component Name: ")
                label.grid(column=0, row=0)

                new_component_name = Entry(self.mainwin)
                new_component_name.grid(column=1, row=0)

                def submit():
                    global component_name
                    component_name = new_component_name.get()
                    self.mainwin.destroy()
                    return component_name

                submit_button = Button(self.mainwin, text ="Submit", command=submit)
                submit_button.grid(column=0, row=2, rowspan=2)

                self.mainwin.wait_window(self.mainwin)
                        
                label3 = Label(new_dim_frame, text='Bag Selectors:')
                label3.grid(column=0, row=3)

                start_cell = Button(new_dim_frame, text ="Start Cell")
                start_cell.grid(column=0, row=4)
                end_cell = Button(new_dim_frame, text ="End Cell")
                end_cell.grid(column=1, row=4)
                cell_range = Button(new_dim_frame, text ="Cell Range")
                cell_range.grid(column=2, row=4)
                direction = Button(new_dim_frame, text ="Direction")
                direction.grid(column=0, row=5)
                col_fill = Button(new_dim_frame, text ="Column Fill")
                col_fill.grid(column=1, row=5)
                row_fill = Button(new_dim_frame, text ="Row Fill")
                row_fill.grid(column=2, row=5)

                label4 = Label(new_dim_frame, text='Bag Filters:')
                label4.grid(column=0, row=7)

                remove_blanks = Button(new_dim_frame, text ="Remove Blanks")
                remove_blanks.grid(column=0, row=8)        

                notebook2.insert(index, new_dim_frame, text=component_name)
                notebook2.select(index)

            addAllignment(component_name, len(notebook2.tabs())-1)

        notebook2 = Notebook(dims_frame)
        notebook2.bind("<<NotebookTabChanged>>", handleTabChange)
        notebook2.pack(fill='both', expand=True)

        add_dim_frame = Frame(notebook2)

        # The allignement frame and last step before tranformation takes place.
        def final():
            final_frame = Frame(notebook)

            label7 = Label(final_frame, text="Relativity")
            label7.grid(column=1, row=0)
            label8 = Label(final_frame, text="Direction")
            label8.grid(column=2, row=0)

            finish_button = Button(final_frame, text ="Finish", command=self.transform)
            finish_button.grid(column=2, row=10, rowspan=2)
            
            return final_frame
    
        final_frame = final()

        def addAllignment(component_name, grid_count_y):
            for tab in notebook2.tabs():
                relativity_options = ["-", "DIRECTLY", "CLOSEST", "CONSTANT"]
                relativity_variable = StringVar()
                relativity_variable.set(relativity_options[3])

                direction_options = ["-", "ABOVE", "BELOW", "LEFT", "RIGHT"]               
                direction_variable = StringVar()
                direction_variable.set(direction_options[4])

                label5 = Label(final_frame, text=component_name)
                label5.grid(column=0, row=grid_count_y)

                relativity = OptionMenu(final_frame, relativity_variable, *relativity_options)
                relativity.grid(column=1, row=grid_count_y)

                direction = OptionMenu(final_frame, direction_variable, *direction_options)
                direction.grid(column=2, row=grid_count_y)
            
        notebook.bind("<<handleTabChanged>>",addAllignment)

        notebook.add(home_frame, text='Home')
        notebook.add(obs_frame, text='Observations')
        notebook.add(dims_frame, text='Dimensions')
        notebook.add(final_frame, text='Allignment')

        notebook2.add(add_dim_frame, text="+")

        return

    def _doFrame2(self):

        if 'uses_sidepane' in self.capabilities:
            self.table = self.parent.getCurrentTable()
            self.mainwin = Frame(self.table.parentframe)
            self.mainwin.grid(row=6,column=0,columnspan=4,sticky='news')
        else:
            self.mainwin=Toplevel()
            self.mainwin.title('QuickWiz Page 2')
            self.mainwin.geometry('600x600+200+100')

        self.ID='Basic Plugin'

        notebook = Notebook(self.mainwin)
        notebook.pack(fill="both", expand=True)

        page = Frame(notebook)
        notebook.add(page)

        return

    def _createMenuBar(self):
        """Create the menu bar for the application. """

        self.menu=Menu(self.mainwin)
        self.file_menu={ '01Quit':{'cmd':self.quit}}
        self.file_menu=self.create_pulldown(self.menu,self.file_menu)
        self.menu.add_cascade(label='File',menu=self.file_menu['var'])
        self.mainwin.config(menu=self.menu)
        return

    def quit(self, evt=None):
        """Override this to handle pane closing"""

        self.mainwin.destroy()
        return

    def about(self):
        """About this plugin"""

        txt = "This plugin implements ...\n"+\
               "version: %s" %self.version
        return txt

    def startCell(self, frame):
        start_cell = Label(frame, text="START: ")
        start_cell.grid(column=0, row=0)

        start_cell_input = Entry(frame)
        start_cell_input.grid(column=1, row=0)

        return

    def endCell(self, frame):
        end_cell = Label(frame, text="END: ")
        end_cell.grid(column=0, row=0)

        end_cell_input = Entry(frame)
        end_cell_input.grid(column=1, row=0)

        return

    def transform(self):
        self.table = self.parent.getCurrentTable()
        self.mainwin = Frame(self.table.parentframe)
        self.mainwin.grid(row=6,column=0,columnspan=4,sticky='news')

        l=Label(self.mainwin, text='This is a template plugin')
        l.pack(side=TOP,fill=BOTH)
        b=Button(self.mainwin,text='Close',command=self.quit)
        b.pack(side=TOP,fill=BOTH,pady=2)
        self.mainwin.bind("<Destroy>", self.quit)
        return

