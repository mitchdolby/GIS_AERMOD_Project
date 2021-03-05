import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import Image, ImageTk

from src.mapWindow import MapWindow
from src.dataprep import GISextract


class DataTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)

        self.rd_list = None

        # Create Open, Import button and File Dialog
        self.createTopButtonAndDialog()

        # Create File setting frame
        self.createSettings()

        # Create Verify inputs button
        self.button_open = ttk.Button(self)
        self.button_open.configure(text="Verify inputs in this page", padding=10, default=tk.ACTIVE,
                                   command=self.btnVerify)
        self.button_open.grid(row=3, column=1, sticky=tk.S)

    def createTopButtonAndDialog(self):
        # Open Button
        self.button_open = ttk.Button(self)
        self.button_open.configure(text="Open", padding=10, default=tk.ACTIVE, command=self.btnOpen)
        self.button_open.grid(row=0, column=0, sticky=tk.W)

        # Import Button
        self.button_import = ttk.Button(self)
        self.button_import.configure(text="Import", padding=10, default=tk.ACTIVE, command=self.btnImport)
        self.button_import.grid(row=0, column=1, sticky=tk.W)

        # File dialog
        self.entry_file = tk.Text(self, height=1, width=80)
        self.entry_file.grid(row=1, column=0, columnspan=4, sticky=tk.W)

    # Define Open button function
    def btnOpen(self):
        # Choose shp file
        self.path = tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                                  filetypes=(("shp files", "*.shp"), ("all files", "*.*"))
                                                  )

        # Clear the textbox string
        self.entry_file.delete('1.0', tk.END)

        # Set the path of shp file in entry_file text box
        self.entry_file.insert(tk.E, self.path)

    # Define Import button function
    def btnImport(self):
        # Extract GIS data
        self.rd_list = GISextract(self.path)

        # Build file setting's drop down menus
        self.buildDropDownMenuSetting()

    # Setting Dropdown menu of File setting frame
    def buildDropDownMenuSetting(self):
        # Get the list of columns of GeoPandas Dataframe of imported GIS data
        columns = self.rd_list.columns.tolist()

        # Set list of choices for each dropdown menu in the File setting frame
        self.combo_roadID["values"] = columns
        self.combo_roadTp["values"] = columns
        self.combo_numLane["values"] = columns
        self.combo_laneWid["values"] = columns

        # For Geometry dropdown menu, set geometry in the top if there exists 'geometry' column
        if 'geometry' in columns:
            columns.remove('geometry')
            columns.insert(0, 'geometry')
            self.combo_geom["values"] = columns
            self.combo_geom.current(0)
        else:
            self.combo_geom["values"] = columns

    # Create setting frames
    def createSettings(self):
        self.createFileSetting()
        self.createProjectionSetting()
        self.createBoundarySetting()

    # Create File setting frame
    def createFileSetting(self):
        # Label Frame
        self.labelFrame_File = tk.LabelFrame(self, text="1. Choose Columns from Shape File", width=400, height=200,
                                             font=(None, 15, "bold"))
        self.labelFrame_File.grid(row=2, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        # Road Unique ID label
        self.label_roadID = tk.Label(self.labelFrame_File, text="Road Unique ID")
        self.label_roadID.grid(row=0, column=0)

        # Road Unique ID Combobox
        self.combo_roadID = ttk.Combobox(self.labelFrame_File, state='readonly')
        self.combo_roadID.grid(row=0, column=1)

        # Road Type label
        self.label_roadTp = tk.Label(self.labelFrame_File, text="Road Type")
        self.label_roadTp.grid(row=1, column=0)

        # Road Type Combobox
        self.combo_roadTp = ttk.Combobox(self.labelFrame_File, state='readonly')
        self.combo_roadTp.grid(row=1, column=1)

        # Number of lanes
        self.label_numLane = tk.Label(self.labelFrame_File, text="Number of Lanes")
        self.label_numLane.grid(row=2, column=0)

        # Number of lanes ID Combobox
        self.combo_numLane = ttk.Combobox(self.labelFrame_File, state='readonly')
        self.combo_numLane.grid(row=2, column=1)

        # Lane width
        self.label_laneWid = tk.Label(self.labelFrame_File, text="Lane Width")
        self.label_laneWid.grid(row=3, column=0)

        # Lane width Combobox
        self.combo_laneWid = ttk.Combobox(self.labelFrame_File, state='readonly')
        self.combo_laneWid.grid(row=3, column=1)

        # Shoulder Label
        self.label_shoulder = tk.Label(self.labelFrame_File, text="Shoulder(m)")
        self.label_shoulder.grid(row=0, column=2)

        # Shoulder textbox
        self.txt_shoulder_var = tk.StringVar()
        self.txt_shoulder = tk.Entry(self.labelFrame_File, textvariable=self.txt_shoulder_var, width=10)
        self.txt_shoulder.grid(row=0, column=3, sticky=tk.W)

        # Geometry Label
        self.label_geom = tk.Label(self.labelFrame_File, text="Geometry")
        self.label_geom.grid(row=1, column=2)

        # Geometry Combobox
        self.combo_geom = ttk.Combobox(self.labelFrame_File, state='readonly')
        self.combo_geom.grid(row=1, column=3)

    # Create Projection setting frame
    def createProjectionSetting(self):
        # Label Frame
        self.labelFrame_Projection = tk.LabelFrame(self, text="2. Origin and Destination", font=(None, 15, "bold"),
                                                   width=400, height=200)
        self.labelFrame_Projection.grid(row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

        # Control ESPG text form: limit length = 4
        def limitESPGinput():
            if len(self.txt_fromproj_var.get()) > 4:
                self.txt_fromproj_var.set(self.txt_fromproj_var.get()[:3])
                self.txt_fromproj.insert(tk.E, self.txt_fromproj_var)

        # Original ESPG
        label_from_proj = tk.Label(self.labelFrame_Projection, text="Origin ESPG (4-digits)")
        label_from_proj.grid(row=0, column=0)

        self.txt_fromproj_var = tk.StringVar()
        self.txt_fromproj = tk.Entry(self.labelFrame_Projection, textvariable=self.txt_fromproj_var, width=4)
        self.txt_fromproj.grid(row=0, column=1)

        # Dest ESPG
        label_to_proj = tk.Label(self.labelFrame_Projection, text="Destination ESPG (4-digits)")
        label_to_proj.grid(row=1, column=0)

        self.txt_toproj_var = tk.StringVar()
        self.txt_toproj = tk.Entry(self.labelFrame_Projection, textvariable=self.txt_toproj_var, width=4)
        self.txt_toproj.grid(row=1, column=1)

        # Control ESPG text form: limit length = 4
        def limitESPGinput(entry, txtbox):
            if len(entry.get()) > 4:
                entry.set(entry.get()[:3])
                txtbox.insert(tk.E, entry)

        self.txt_toproj_var.trace("w", lambda *args: limitESPGinput(self.txt_toproj_var, self.txt_toproj))

        # CheckBox whether meter or feet
        label_chkUnit = tk.Label(self.labelFrame_Projection, text="Unit of destination ESPG")
        label_chkUnit.grid(row=2, column=0)

        # Control meter feet checkbox
        def controlChkUnit():
            # If m or f checked, disable the other
            if self.chk_m:
                self.chk_f.config(state=tk.DISABLED)
            elif self.chk_f:
                self.chk_m.config(state=tk.DISABLED)
            else:
                self.chk_m.config(state=tk.NORMAL)
                self.chk_f.config(state=tk.NORMAL)

            # self.chk_m.config(state=tk.DISABLED if not self.bln_f else tk.NORMAL)
            # self.chk_f.config(state=tk.DISABLED if not self.bln_m else tk.NORMAL)

        # Meter checkbox
        self.bln_m = tk.BooleanVar(False)
        self.chk_m = tk.Checkbutton(self.labelFrame_Projection, variable=self.bln_m, command=controlChkUnit, text="m")
        self.chk_m.grid(row=2, column=1)

        # Feet checkbox
        self.bln_f = tk.BooleanVar(False)
        self.chk_f = tk.Checkbutton(self.labelFrame_Projection, variable=self.bln_f, command=controlChkUnit, text="ft")
        self.chk_f.grid(row=3, column=1)

    # Create Boundary setting frame
    def createBoundarySetting(self):
        # Label Frame
        labelFrame_Boundary = tk.LabelFrame(self, text="3. Locate boundary and reference point", width=500,
                                            height=200, font=(None, 15, "bold"))
        labelFrame_Boundary.grid(row=3, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        # Locate from graph button
        button_locateGraph = ttk.Button(labelFrame_Boundary)
        button_locateGraph.configure(text="Locate from graph", padding=10, default=tk.ACTIVE,
                                     command=self.btnLocateGraph)
        button_locateGraph.grid(row=0, column=7, sticky=tk.E)

        # y high text box
        label_yHigh = tk.Label(labelFrame_Boundary, text="Y high")
        label_yHigh.grid(row=0, column=3, sticky=tk.E)

        self.txt_yHigh_var = tk.StringVar()
        txt_yHigh = tk.Entry(labelFrame_Boundary, textvariable=self.txt_yHigh_var, width=10)
        txt_yHigh.grid(row=0, column=4, sticky=tk.W)

        # x left text box
        label_xLeft = tk.Label(labelFrame_Boundary, text="X left")
        label_xLeft.grid(row=2, column=0, rowspan=2, sticky=tk.E)

        self.txt_xLeft_var = tk.StringVar()
        txt_xLeft = tk.Entry(labelFrame_Boundary, textvariable=self.txt_xLeft_var, width=10)
        txt_xLeft.grid(row=2, column=1, rowspan=2, sticky=tk.W)

        # X right text box
        label_xRight = tk.Label(labelFrame_Boundary, text="X right")
        label_xRight.grid(row=2, column=6, rowspan=2, sticky=tk.E)

        self.txt_xRight_var = tk.StringVar()
        txt_xRight = tk.Entry(labelFrame_Boundary, textvariable=self.txt_xRight_var, width=10)
        txt_xRight.grid(row=2, column=7, rowspan=2, sticky=tk.W)

        # Y low text box
        label_yLow = tk.Label(labelFrame_Boundary, text="Y low")
        label_yLow.grid(row=5, column=3, rowspan=2, sticky=tk.E)

        self.txt_yLow_var = tk.StringVar()
        txt_yLow = tk.Entry(labelFrame_Boundary, textvariable=self.txt_yLow_var, width=10)
        txt_yLow.grid(row=5, column=4, rowspan=2, sticky=tk.W)

        # Reference point x text box
        label_xRef = tk.Label(labelFrame_Boundary, text="Reference x")
        label_xRef.grid(row=2, column=3, sticky=tk.E)

        self.txt_xRef_var = tk.StringVar()
        txt_xRef = tk.Entry(labelFrame_Boundary, textvariable=self.txt_xRef_var, width=10)
        txt_xRef.grid(row=2, column=4, sticky=tk.W)

        # Reference point y text box
        label_yRef = tk.Label(labelFrame_Boundary, text="Reference y")
        label_yRef.grid(row=3, column=3, sticky=tk.E)

        self.txt_yRef_var = tk.StringVar()
        txt_yRef = tk.Entry(labelFrame_Boundary, textvariable=self.txt_yRef_var, width=10)
        txt_yRef.grid(row=3, column=4, sticky=tk.W)

        # Empty labels
        label_emp1 = tk.Label(labelFrame_Boundary, text="   ")
        label_emp1.grid(row=1, column=0, sticky=tk.E)

        label_emp2 = tk.Label(labelFrame_Boundary, text="   ")
        label_emp2.grid(row=0, column=2, sticky=tk.E)

        label_emp3 = tk.Label(labelFrame_Boundary, text="   ")
        label_emp3.grid(row=0, column=5, sticky=tk.E)

        label_emp4 = tk.Label(labelFrame_Boundary, text="   ")
        label_emp4.grid(row=4, column=0, sticky=tk.E)

    # Open GIS plot window
    def btnLocateGraph(self):

        # Check if GIS data rd_list is null or not
        if self.rd_list is None:
            tk.messagebox.showerror("Error", "rd_list is null")
            return

        # Open GIS plot window
        locateGraphWindow = tk.Toplevel(self)
        locateGraphWindow.title("Locate boundary and reference point")
        locateGraphWindow.geometry("800x600")

        # Set GIS plot window with pop-up-window
        self.buildMapWindow(locateGraphWindow)

        locateGraphWindow.mainloop()

    # Build GIS plot window
    def buildMapWindow(self, window):
        # Set mapWindow frame with pop up window
        mapWin = MapWindow(self.rd_list, window)
        tk.Grid.rowconfigure(mapWin, 0, weight=1)
        tk.Grid.columnconfigure(mapWin, 0, weight=1)

    # Verify inputs button
    def btnVerify(self):
        # Check input values
        pass

    # Check input values when verify inputs button pressed
    def checkErrBtnVerify(self):
        pass


# Road tab class
class RoadTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)

        # Create Line frame
        self.createLineFrame()

        # Create AREA frame
        self.createAreaFrame()

        # Create VOLUME frame
        self.createVolFrame()

    def createLineFrame(self):
        # Outer Label Frame
        labelFrame_OutLine = tk.LabelFrame(self, text="Line (LINE, RLINE, RLINEXT)", width=400, height=200,
                                           font=(None, 15, "bold"))
        labelFrame_OutLine.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        # Inner Frame
        # frame_InLine = tk.Frame(labelFrame_OutLine, borderwidth=2, highlightcolor='red', width=400, height=200)
        frame_InLine = tk.Frame(labelFrame_OutLine, highlightbackground="red", highlightcolor="black",
                                highlightthickness=1, width=100, height=100, bd=0)
        frame_InLine.grid(row=0, column=0)

        str = "Line includes LINE, RLINE and RLINEXT. The geometries of line sources are defined with coordinates of two end points and line width."
        label_emp1 = tk.Label(frame_InLine, text=str, wraplength=150)
        label_emp1.grid(row=0, column=0)

        # Control line example button
        def btnLineExample():
            lineGraphicWin = tk.Toplevel(self)
            canvas = tk.Canvas(lineGraphicWin, width=300, height=300)
            canvas.grid()

            img = Image.open('C:\\Users\\Shiro\\Desktop\\0120.jpg')
            my_image = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor=tk.NW, image=my_image)

            tk.Grid.rowconfigure(lineGraphicWin, 0, weight=1)
            tk.Grid.columnconfigure(lineGraphicWin, 0, weight=1)

        # Place LIne's graphic example button
        self.button_lineExample = ttk.Button(frame_InLine)
        self.button_lineExample.configure(text="Graphic example", padding=10, default=tk.ACTIVE, command=btnLineExample)
        self.button_lineExample.grid(row=1, column=0)

        # Place LINE columns button
        self.button_lineCols = ttk.Button(frame_InLine)
        self.button_lineCols.configure(text="LINE columns", padding=10, default=tk.ACTIVE, command=btnLineExample)
        self.button_lineCols.grid(row=2, column=0)

        # Place Generate Line button
        self.button_generateLine = ttk.Button(labelFrame_OutLine)
        self.button_generateLine.configure(text="Generate Line", padding=10, default=tk.ACTIVE, command=btnLineExample)
        self.button_generateLine.grid(row=1, column=0)

        # Place Visualize Line button
        self.button_visualizeLine = ttk.Button(labelFrame_OutLine)
        self.button_visualizeLine.configure(text="Visualize Line", padding=10, default=tk.ACTIVE,
                                            command=btnLineExample)
        self.button_visualizeLine.grid(row=2, column=0)

    # Create AREA frame
    def createAreaFrame(self):
        # Outer Label Frame
        labelFrame_OutArea = tk.LabelFrame(self, text="AREA", width=400, height=200,
                                           font=(None, 15, "bold"))
        labelFrame_OutArea.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

    # Create AREA frame
    def createVolFrame(self):
        # Outer Label Frame
        labelFrame_OutVol = tk.LabelFrame(self, text="VOLUME", width=400, height=200,
                                          font=(None, 15, "bold"))
        labelFrame_OutVol.grid(row=0, column=2, sticky=tk.W + tk.E + tk.N + tk.S)


def main():
    root = tk.Tk()
    root.title("GIS TO AERMOD Tool")
    root.geometry("700x400")

    nb = ttk.Notebook(root, width=800, height=600)

    # Add Data tab
    data_tab = DataTab(master=nb)
    nb.add(data_tab, text='Data', padding=5)

    # Add Road tab
    road_tab = RoadTab(master=nb)
    nb.add(road_tab, text='Road', padding=5)

    nb.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()