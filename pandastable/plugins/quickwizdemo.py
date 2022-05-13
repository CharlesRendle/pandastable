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
from glob import glob
from lib2to3.pgen2.pgen import DFAState
from tkinter import *
import tkinter
from typing import final

import os

from pyparsing import col
try:
    from tkinter.ttk import *
except:
    from ttk import *
from pandastable.plugin import Plugin
from pandastable.app import DataExplore

class QuickWiz(Plugin):
    """Template plugin for DataExplore"""

    #uncomment capabilities list to appear in menu
    capabilities = ['gui']
    requires = ['']
    menuentry = 'QuickWiz Demo'


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
            self.mainwin.title('QuickWiz Demo')
            self.mainwin.geometry('600x600+200+100')

        self.ID='Basic Plugin'

        global notebook
        notebook = Notebook(self.mainwin)
        notebook.pack(fill='both', expand=True)

        # Starting frame from where the user can begin tutorials or open
        # the glossary.
        def start():
            start_frame = Frame(notebook)

            start_button = Button(start_frame, text ="Start", command=self.loadExample)
            start_button.grid(column=0, row=0)

            return start_frame

        start_frame = start()
        notebook.add(start_frame, text='Start')

        def obs():
            obs_frame = Frame(notebook)

            global notebook2
            notebook2 = Notebook(obs_frame)

            obs_intro_frame = Frame(notebook2)
            notebook2.pack(fill='both', expand=True)
            notebook2.add(obs_intro_frame, text='Intro')

            next1 = Button(obs_intro_frame, text ="Next", command=self.next1)
            next1.grid(column=0, row=0)

            return obs_frame
        
        global obs_frame
        obs_frame = obs()

        def obs_capture():
            obs_capture_frame = Frame(notebook2)

            construction = Entry(obs_capture_frame, width=60)
            construction.grid(column=1, row=0)
            construction.insert(END, '|| START CELL: "C9" ')
            construction.insert(END, '|| DIRECTION: "RIGHT" ')
            construction.insert(END, '|| DIRECTION: "DOWN" ')
            construction.insert(END, '|| IGNORE BLANK CELLS ')

            label1 = Label(obs_capture_frame, text='Bag Selectors:')
            label1.grid(column=0, row=3)

            start_cell = Button(obs_capture_frame, text ="Start Cell")
            start_cell.grid(column=0, row=4)
            end_cell = Button(obs_capture_frame, text ="End Cell")
            end_cell.grid(column=1, row=4)
            cell_range = Button(obs_capture_frame, text ="Cell Range")
            cell_range.grid(column=2, row=4)
            direction = Button(obs_capture_frame, text ="Direction")
            direction.grid(column=0, row=5)
            col_fill = Button(obs_capture_frame, text ="Column Fill")
            col_fill.grid(column=1, row=5)
            row_fill = Button(obs_capture_frame, text ="Row Fill")
            row_fill.grid(column=2, row=5)

            label2 = Label(obs_capture_frame, text='Bag Filters:')
            label2.grid(column=0, row=7)

            remove_blanks = Button(obs_capture_frame, text ="Remove Blanks")
            remove_blanks.grid(column=0, row=8)

            next2 = Button(obs_capture_frame, text ="Next", command=self.next2)
            next2.grid(column=3, row=9)

            df = self.getDf()
            #df.style.set_properties(**{'background-color': 'black',
            #               'color': 'green'})
            #rows = [0,1,2]
            #cols = [0,2]
            #color = "red"
            #table.setRowColors(rows, color, cols=cols)
            #table.redraw()
            self.setColours()
            #DataExplore.setColours(self.parent)

            return obs_capture_frame

        global obs_capture_frame
        obs_capture_frame = obs_capture()


        def dims():
            dims_frame = Frame(notebook)

            global notebook3
            notebook3 = Notebook(dims_frame)

            dims_intro_frame = Frame(notebook3)
            notebook3.pack(fill='both', expand=True)
            notebook3.add(dims_intro_frame, text='Intro')

            next3 = Button(dims_intro_frame, text ="Next", command=self.next3)
            next3.grid(column=0, row=0)

            return dims_frame
        
        global dims_frame
        dims_frame = dims()

        def name():
            name_frame = Frame(notebook3)

            construction = Entry(name_frame, width=60)
            construction.grid(column=1, row=0)
            construction.insert(END, '|| START CELL: "B9" ')
            construction.insert(END, '|| DIRECTION: "DOWN" ')
            construction.insert(END, '|| IGNORE BLANK CELLS ')

            label1 = Label(name_frame, text='Bag Selectors:')
            label1.grid(column=0, row=3)

            start_cell = Button(name_frame, text ="Start Cell")
            start_cell.grid(column=0, row=4)
            end_cell = Button(name_frame, text ="End Cell")
            end_cell.grid(column=1, row=4)
            cell_range = Button(name_frame, text ="Cell Range")
            cell_range.grid(column=2, row=4)
            direction = Button(name_frame, text ="Direction")
            direction.grid(column=0, row=5)
            col_fill = Button(name_frame, text ="Column Fill")
            col_fill.grid(column=1, row=5)
            row_fill = Button(name_frame, text ="Row Fill")
            row_fill.grid(column=2, row=5)

            label2 = Label(name_frame, text='Bag Filters:')
            label2.grid(column=0, row=7)

            remove_blanks = Button(name_frame, text ="Remove Blanks")
            remove_blanks.grid(column=0, row=8)

            next4 = Button(name_frame, text ="Next", command=self.next4)
            next4.grid(column=3, row=9)

            return name_frame

        global name_frame
        name_frame = name()

        def group():
            group_frame = Frame(notebook3)

            construction = Entry(group_frame, width=60)
            construction.grid(column=1, row=0)
            construction.insert(END, '|| START CELL: "A9" ')
            construction.insert(END, '|| DIRECTION: "DOWN" ')
            construction.insert(END, '|| IGNORE BLANK CELLS ')

            label1 = Label(group_frame, text='Bag Selectors:')
            label1.grid(column=0, row=3)

            start_cell = Button(group_frame, text ="Start Cell")
            start_cell.grid(column=0, row=4)
            end_cell = Button(group_frame, text ="End Cell")
            end_cell.grid(column=1, row=4)
            cell_range = Button(group_frame, text ="Cell Range")
            cell_range.grid(column=2, row=4)
            direction = Button(group_frame, text ="Direction")
            direction.grid(column=0, row=5)
            col_fill = Button(group_frame, text ="Column Fill")
            col_fill.grid(column=1, row=5)
            row_fill = Button(group_frame, text ="Row Fill")
            row_fill.grid(column=2, row=5)

            label2 = Label(group_frame, text='Bag Filters:')
            label2.grid(column=0, row=7)

            remove_blanks = Button(group_frame, text ="Remove Blanks")
            remove_blanks.grid(column=0, row=8)

            next5 = Button(group_frame, text ="Next", command=self.next5)
            next5.grid(column=3, row=9)

            return group_frame
        
        global group_frame
        group_frame = group()

        def year():
            year_frame = Frame(notebook3)

            construction = Entry(year_frame, width=60)
            construction.grid(column=1, row=0)
            construction.insert(END, '|| START CELL: "E5" ')

            label1 = Label(year_frame, text='Bag Selectors:')
            label1.grid(column=0, row=3)

            start_cell = Button(year_frame, text ="Start Cell")
            start_cell.grid(column=0, row=4)
            end_cell = Button(year_frame, text ="End Cell")
            end_cell.grid(column=1, row=4)
            cell_range = Button(year_frame, text ="Cell Range")
            cell_range.grid(column=2, row=4)
            direction = Button(year_frame, text ="Direction")
            direction.grid(column=0, row=5)
            col_fill = Button(year_frame, text ="Column Fill")
            col_fill.grid(column=1, row=5)
            row_fill = Button(year_frame, text ="Row Fill")
            row_fill.grid(column=2, row=5)

            label2 = Label(year_frame, text='Bag Filters:')
            label2.grid(column=0, row=7)

            remove_blanks = Button(year_frame, text ="Remove Blanks")
            remove_blanks.grid(column=0, row=8)

            next6 = Button(year_frame, text ="Next", command=self.next6)
            next6.grid(column=3, row=9)

            return year_frame
        
        global year_frame
        year_frame = year()

        def assetType():
            asset_frame = Frame(notebook3)

            construction = Entry(asset_frame, width=60)
            construction.grid(column=1, row=0)
            construction.insert(END, '|| START CELL: "C7" ')
            construction.insert(END, '|| END CELL: "E7" ')

            label1 = Label(asset_frame, text='Bag Selectors:')
            label1.grid(column=0, row=3)

            start_cell = Button(asset_frame, text ="Start Cell")
            start_cell.grid(column=0, row=4)
            end_cell = Button(asset_frame, text ="End Cell")
            end_cell.grid(column=1, row=4)
            cell_range = Button(asset_frame, text ="Cell Range")
            cell_range.grid(column=2, row=4)
            direction = Button(asset_frame, text ="Direction")
            direction.grid(column=0, row=5)
            col_fill = Button(asset_frame, text ="Column Fill")
            col_fill.grid(column=1, row=5)
            row_fill = Button(asset_frame, text ="Row Fill")
            row_fill.grid(column=2, row=5)

            label2 = Label(asset_frame, text='Bag Filters:')
            label2.grid(column=0, row=7)

            remove_blanks = Button(asset_frame, text ="Remove Blanks")
            remove_blanks.grid(column=0, row=8)

            next7 = Button(asset_frame, text ="Next", command=self.next7)
            next7.grid(column=3, row=9)

            return asset_frame

        global asset_frame
        asset_frame = assetType()

        def allign():
            allign_frame = Frame(notebook)

            global notebook4
            notebook4 = Notebook(allign_frame)

            allign_intro_frame = Frame(notebook4)
            notebook4.pack(fill='both', expand=True)
            notebook4.add(allign_intro_frame, text='Intro')                      

            next8 = Button(allign_intro_frame, text ="Next", command=self.next8)
            next8.grid(column=0, row=0)

            return allign_frame
        
        global allign_frame
        allign_frame = allign()

        def assign():
            assign_frame = Frame(notebook4)

            relativity_options = ["DIRECTLY", "-", "CLOSEST", "CONSTANT"]
            relativity_variable = StringVar()
            #relativity_variable.set( "DIRECTLY" )
            relativity_variable.set(relativity_options[1])

            direction_options = ["LEFT", "ABOVE", "BELOW", "-", "RIGHT"]               
            direction_variable = StringVar()
            #direction_variable.set("LEFT")
            direction_variable.set(direction_options[3])

            relativity_options2 = ["CLOSEST", "-", "DIRECTLY", "CONSTANT"]
            relativity_variable2 = StringVar()
            #relativity_variable2.set("CLOSEST")
            relativity_variable2.set(relativity_options[1])

            direction_options2 = ["LEFT", "-", "ABOVE", "BELOW", "RIGHT"]               
            direction_variable2 = StringVar()
            #direction_variable2.set("LEFT")
            direction_variable2.set(direction_options[1])

            relativity_options3 = ["CONSTANT", "-", "DIRECTLY", "CLOSEST"]
            relativity_variable3 = StringVar()
            #relativity_variable3.set("CONSTANT")
            relativity_variable3.set(relativity_options[1])

            direction_options3 = ["-", "ABOVE", "BELOW", "LEFT", "RIGHT"]               
            direction_variable3 = StringVar()
            direction_variable3.set(direction_options[4])

            relativity_options4 = ["DIRECTLY", "-", "CLOSEST", "CONSTANT"]
            relativity_variable4 = StringVar()
            #relativity_variable4.set("DIRECTLY")
            relativity_variable4.set(relativity_options[1])

            direction_options4 = ["ABOVE", "-", "BELOW", "LEFT", "RIGHT"]               
            direction_variable4 = StringVar()
            #direction_variable4.set("ABOVE")
            direction_variable4.set(direction_options[1])

            assign_name = Label(assign_frame, text="Name")
            assign_name.grid(column=0, row=0)

            name_relativity = OptionMenu(assign_frame, relativity_variable, *relativity_options)
            name_relativity.grid(column=1, row=1)

            name_direction = OptionMenu(assign_frame, direction_variable, *direction_options)
            name_direction.grid(column=2, row=1)

            assign_group = Label(assign_frame, text="Group")
            assign_group.grid(column=0, row=2)

            group_relativity = OptionMenu(assign_frame, relativity_variable2, *relativity_options2)
            group_relativity.grid(column=1, row=3)

            group_direction = OptionMenu(assign_frame, direction_variable2, *direction_options2)
            group_direction.grid(column=2, row=3)

            assign_year = Label(assign_frame, text="Year")
            assign_year.grid(column=0, row=4)

            name_relativity = OptionMenu(assign_frame, relativity_variable3, *relativity_options3)
            name_relativity.grid(column=1, row=5)

            assign_assets = Label(assign_frame, text="Assets")
            assign_assets.grid(column=0, row=6)

            assets_relativity = OptionMenu(assign_frame, relativity_variable4, *relativity_options4)
            assets_relativity.grid(column=1, row=7)

            assets_direction = OptionMenu(assign_frame, direction_variable4, *direction_options4)
            assets_direction.grid(column=2, row=7)

            finish = Button(assign_frame, text ="Finish", command=self.finish)
            finish.grid(column=3, row=8)

            return assign_frame

        global assign_frame
        assign_frame = assign()     

    def loadExample(self):
        self.modulepath = os.path.dirname(__file__)

        global filename
        filename = os.path.join(self.modulepath, "datasets", "assets.xls")
        DataExplore.importExcel(self.parent, filename=filename)

        notebook.add(obs_frame, text='Observations')
        notebook.select(obs_frame)

    def next1(self):
        notebook2.add(obs_capture_frame, text='Obs Capture')
        notebook2.select(obs_capture_frame)

    def next2(self):
        notebook.add(dims_frame, text='Dimensions')
        notebook.select(dims_frame)

    def next3(self):
        notebook3.add(name_frame, text='Name')
        notebook3.select(name_frame)

    def next4(self):
        notebook3.add(group_frame, text='Group')
        notebook3.select(group_frame)

    def next5(self):
        notebook3.add(year_frame, text='Year')
        notebook3.select(year_frame)

    def next6(self):
        notebook3.add(asset_frame, text='Assets')
        notebook3.select(asset_frame)

    def next7(self):
        notebook.add(allign_frame, text='Allignment')
        notebook.select(allign_frame)

    def next8(self):
        notebook4.add(assign_frame, text='Assignment')
        notebook4.select(assign_frame)

    def getDf(self):
        global table
        table = self.parent.getCurrentTable()
        global df
        df = table.model.df
        return df

    def setColours(self):
        global table
        table = self.parent.getCurrentTable()
        rows = [0,1,2]
        cols = [0,2]
        color = "red"
        table.setRowColors(rows, color, cols=cols)
        table.redraw()
        return

    def finish():
        import databaker

        tabs = framework.loadxlstabs(filename)
        tab = tabs[0]

        observations = tab.excel_ref("C9").expand(RIGHT).expand(DOWN).is_not_blank()

        name = tab.excel_ref("B9").expand(DOWN).is_not_blank()

        group = tab.excel_ref("A9").expand(DOWN).is_not_blank()

        year = "1969"

        asset_type = tab.excel_ref("C7:E7")

        dimensions = [
            HDim(name, "Name", DIRECTLY, LEFT),
            HDIm(group, "Group", CLOSEST, ABOVE),   
            HDimConst("Year", year),
            HDim(asset_type, "Asset Type", DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)

        df = tidy_sheet.topandas()

        return        
    