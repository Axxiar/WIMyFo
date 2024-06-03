import os
import os.path as path
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, font
from ttkbootstrap.constants import *
from datetime import date

APP_FONT = lambda size: ("JetBrainsMono NF",size)
#     print(dir_content,"\n\n",f"dirs: {total_dir_number}\n", f"files: {total_file_number}")

# TKINTER CLASSES
class WimyfoApp(ttk.Window):
    def __init__(self, dirpath=os.getcwd()):
        #==SETUP==
        super().__init__(themename="superhero")
        self.dirpath = ttk.StringVar(value=dirpath)
        self.title("WIMyFo")
        self.window_sizes = [["900x290", (700,200)],["1170x660",(700,500)]]
        self.geometry(self.window_sizes[0][0])
        self.minsize(*self.window_sizes[0][1])

        #==WIDGETS==
        self.notebook = ttk.Notebook(self)
        self.menu_tab = MenuTab(self, self.notebook)
        self.stats_tab = StatsTab(self, self.notebook)

        self.display()
        

    def change_tab(self):
        self.notebook.select(1)
        self.geometry(self.window_sizes[1][0])
        self.minsize(*self.window_sizes[1][1])
        self.stats_tab.dirinfo.update(self.dirpath.get())
        self.stats_tab.add_details()
        self.stats_tab.display(True)


    def display(self):
        self.menu_tab.display()
        self.stats_tab.display(False)
        self.notebook.add(self.menu_tab, text = "Menu")
        self.notebook.add(self.stats_tab, text = "Directory stats")
        self.notebook.pack(expand=True,fill=BOTH)


class MenuTab(ttk.Frame):
    def __init__(self, main_window, parent):
        super().__init__(parent)
        self.main_window = main_window # to track main window

        self.menu_label = ttk.Label(self, text="Select a folder",font=APP_FONT(14))
        self.interactive_frame = ttk.Frame(self)
        self.dir_entry = ttk.Entry(
            self.interactive_frame,
            width=70,
            bootstyle=LIGHT,
            textvariable=self.main_window.dirpath
        )

        self.browse_btn = ttk.Button(
            self.interactive_frame, 
            text="Browse",
            bootstyle="outline-primary",
            cursor="hand2",
            command=self.askdir
        )
        self.continue_btn = ttk.Button(
            self,
            text="Continue",
            bootstyle="success",
            cursor="hand2",
            command=self.valid_choosen_dir
        )
    
    def askdir(self):
        dp = filedialog.askdirectory(
            title="Select a directory",
            initialdir=self.main_window.dirpath.get(),
            mustexist=True
        )
        self.main_window.dirpath.set(dp)

    
    def valid_choosen_dir(self):
        if os.path.isdir(self.main_window.dirpath.get()):
            self.main_window.change_tab()
        else:
            raise Exception("not a dir")

    def display(self):
        self.pack()
        self.menu_label.pack(pady=20)
        self.interactive_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.dir_entry.pack(side=LEFT,padx=5)
        self.browse_btn.pack(side=RIGHT,padx=5)
        self.continue_btn.pack(side=BOTTOM,pady=(5,20))


class StatsTab(tk.Frame):
    def __init__(self, main_window, parent):
        super().__init__(parent)
        self.main_window = main_window
        self.dirinfo = DirInfo()
        self.ext_progbars_list = []
        self.ext_labels_list = []

        # No Folder text
        self.placeholder_label = ttk.Label(self,text="Select a folder first",bootstyle=DANGER, font=APP_FONT(12))
        
        # Folder widgets
        self.maininfo_frame = ttk.LabelFrame(self, text=self.dirinfo.name.get(), bootstyle=WARNING)
        self.details_frame = ttk.Frame(self)

        self.files_frame = ttk.LabelFrame(self.details_frame, text="FILES", bootstyle=INFO)
        self.folders_frame = ttk.LabelFrame(self.details_frame, text="FOLDERS", bootstyle=INFO)

        self.mainleft_frame = ttk.Frame(self.maininfo_frame)
        self.mainright_frame = ttk.Frame(self.maininfo_frame, bootstyle=DANGER)


        # -- mainleft
        self.path_label = ttk.Label(
            self.mainleft_frame,
            textvariable=self.dirinfo.path
        )
        self.cat_label = ttk.Label(
            self.mainleft_frame,
            textvariable=self.dirinfo.ct_date,
        )

        # -- mainright
        self.totalsize_label = ttk.Label(self.mainright_frame, width=20, text="Total Size: None")
        self.subfolders_label = ttk.Label(
            self.mainright_frame,
            textvariable=self.dirinfo.subdirs_total,
            width=20,
            anchor=W
        )
        self.files_label = ttk.Label(
            self.mainright_frame,
            textvariable=self.dirinfo.files_total,
            width=20,
            anchor=W
        )

    
    def add_details(self):
        for ext,files in self.dirinfo.content_files.items():
            label = ttk.Label(self.files_frame, text=ext)
            progbar = ttk.Progressbar(self.files_frame, bootstyle="warning-striped", mode=DETERMINATE, value=50)
            self.ext_progbars_list.append(progbar)
            self.ext_labels_list.append(label)
            print(f"Stat for {ext}:", end="\n\t")
            for file in files[0]:
                print(file, end=", ")
            print()


    def display(self, folder_selected):
        """folder_selected:
        False = no folder path selected
        True = folder path selected
        """
        if not folder_selected:
            self.pack()
            self.placeholder_label.pack()
        else:
            self.placeholder_label.pack_forget()

            self.maininfo_frame.pack(padx=10, pady=10, fill=X)
            self.details_frame.pack(expand=True, fill=BOTH)
            self.files_frame.pack(expand=True, fill=BOTH, side=LEFT, padx=10, pady=10)
            self.folders_frame.pack(expand=True, fill=BOTH, side=RIGHT, padx=10, pady=10)
            self.mainleft_frame.pack(fill=Y, side=LEFT, padx=5, pady=5)
            self.mainright_frame.pack(fill=Y, side=RIGHT, padx=5, pady=(0,5))

            self.path_label.pack()
            self.cat_label.pack(side=LEFT)
            self.totalsize_label.pack()
            self.files_label.pack()
            self.subfolders_label.pack()

            for label,progbar in list(zip(self.ext_labels_list,self.ext_progbars_list)):
                label.pack(pady=(5,0))
                progbar.pack(pady=(0,5), padx=20 ,fill=X)


# SCRIPT CLASSES
class DirInfo():
    """ A class countaining ttk variables storing infos on provided directory path
    """
    def __init__(self):
        self.name = ttk.StringVar(value="None")
        self.path = ttk.StringVar(value="None")
        self.content_dirs, self.content_files = None,None
        self.ct_date = ttk.StringVar(value="None")
        self.subdirs_total = ttk.StringVar(value="None")
        self.files_total = ttk.StringVar(value="None")

    def update(self, pth: str):
        #----- Folder Name -----------------------
        self.name.set(os.path.basename(pth))
        self.path.set(f"Path: {pth}")
        #----- Folder Content --------------------
        self.content_dirs, self.content_files = self.get_dir_content(pth)
        #----- Date Creation ---------------------
        self.ct_date.set(f"Creation date: {date.fromtimestamp(os.path.getctime(pth))}")
        #----- Number of direct subdirectory -----
        self.subdirs_total.set(f"Subfolders total: {len(self.content_dirs)}")
        #----- Total of file ---------------------
        self.files_total.set(f"Files total: {self.get_files_total()}")
        #-----------------------------------------

    def get_files_total(self):
        ft = 0
        for ext,filenames in self.content_files.items():
            if ext != "dir":
                ft += len(filenames[0])
        return ft

    def get_dir_content(self, starting_pth: str):
        """Gets info about specified directory path. Return a dict where keys are file extensions & values are list of files with key's extension.
            Directories are also listed with 'dir' as key.

            pth - the aboslute or relative path to retrieve info from

            Return     : {extension:[[DirEntry file1, DirEntry file2], total_size_of_extension]}
            Return type: dict(str:list[list[DirEntry],int])
        """
        dirs = []
        ext_dict = {}
        
        def rec_gdc(pth: str, dirs: list, ext_dict: dict):
            """recursive get_dir_content"""
            for file in os.scandir(pth):
                if file.is_dir() and file.name[0] != '.':
                    dirs.append(file.name)
                    rec_gdc(path.join(pth,file.name), dirs, ext_dict)

                elif file.is_file():
                    _, ext = path.splitext(file.name)
                    if ext == "":
                        ext = file.name
                    if ext in ext_dict:
                        ext_dict[ext][0].append(file)
                        ext_dict[ext][1] += file.stat().st_size
                    else:
                        ext_dict[ext] = [[file],file.stat().st_size]
        
        rec_gdc(starting_pth, dirs, ext_dict)
        return dirs,ext_dict


if __name__ == "__main__":
    wimyfo = WimyfoApp()
    wimyfo.mainloop()

#     # Content retrieving
#     dir_content = get_dir_content(userpath)
    
#     # Stats extraction
#     total_dir_number = len(dir_content["dir"])
#     total_file_number = 0
#     for ext,filenames in dir_content.items():
#         if ext != "dir":
#             total_file_number += len(filenames)