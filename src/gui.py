import os
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, font
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *

from analyser import DirInfo


APP_FONT = lambda size: ("JetBrainsMono NF",size)

class WimyfoApp(ttk.Window):
    def __init__(self, dirpath=os.getcwd()):
        #==SETUP==
        super().__init__()
        self.dirpath = ttk.StringVar(value=dirpath)
        self.title("WIMyFo")
        self.window_sizes = [["900x290", (700,200)],["1170x660",(1000,500)]]
        self.geometry(self.window_sizes[0][0])
        self.minsize(*self.window_sizes[0][1])
        self.style.theme_use("superhero")   

        #==WIDGETS==
        self.notebook = ttk.Notebook(self)
        self.menu_tab = MenuTab(self, self.notebook)
        self.stats_tab = StatsTab(self, self.notebook)
        self.settings_tab = SettingsTab(self, self.notebook)

        self.display()
        

    def analyse_dir(self):
        self.notebook.select(1)
        self.geometry(self.window_sizes[1][0])
        self.minsize(*self.window_sizes[1][1])

        self.reset_statstab()

        self.stats_tab.dirinfo.update(self.dirpath.get())
        self.stats_tab.add_details()
        self.stats_tab.display(True)

    def reset_statstab(self):
        for label,progbar in list(zip(self.stats_tab.ext_labels_list, self.stats_tab.ext_progbars_list)):
                label.pack_forget()
                progbar.pack_forget()
        for label in self.stats_tab.subdir_labels_list:
            label.pack_forget()
        self.stats_tab.ext_labels_list, self.stats_tab.ext_progbars_list, self.stats_tab.subdir_labels_list = [], [], []

    def display(self):
        self.menu_tab.display()
        self.stats_tab.display(False)
        self.notebook.add(self.menu_tab, text = "Menu")
        self.notebook.add(self.stats_tab, text = "Directory stats")
        self.notebook.add(self.settings_tab, text = "Settings")
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
            bootstyle=OUTLINE,
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
            self.main_window.analyse_dir()
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
        self.subdir_labels_list = []

        # No Folder text
        self.placeholder_label = ttk.Label(self,text="Select a folder first",bootstyle=DANGER, font=APP_FONT(12))
        
        # Folder widgets
        self.maininfo_frame = ttk.LabelFrame(self, text="MAIN", bootstyle=WARNING)
        self.details_frame = ttk.Frame(self)

        self.mainleft_frame = ttk.Frame(self.maininfo_frame)
        self.mainright_frame = ttk.Frame(self.maininfo_frame)

        self.files_frame = ttk.LabelFrame(self.details_frame, text="FILES", bootstyle=INFO)
        self.folders_frame = ttk.LabelFrame(self.details_frame, text="FOLDERS", bootstyle=INFO)

        self.scrollfiles_frame = ScrolledFrame(self.files_frame)
        self.scrollfolders_frame = ScrolledFrame(self.folders_frame)

        # -- mainleft
        self.name_label = ttk.Label(self.mainleft_frame, textvariable=self.dirinfo.name, font=APP_FONT(10))
        self.path_label = ttk.Label(self.mainleft_frame, textvariable=self.dirinfo.path, font=APP_FONT(8))
        self.cat_label = ttk.Label(self.mainleft_frame, textvariable=self.dirinfo.ct_date, font=APP_FONT(8))

        # -- mainright
        self.totalsize_label = ttk.Label(self.mainright_frame, width=25, textvariable=self.dirinfo.total_size , font=APP_FONT(8))
        self.direct_subfolders_label = ttk.Label(
            self.mainright_frame,
            textvariable=self.dirinfo.direct_subdirs_total,
            width=25,
            anchor=W,
            font=APP_FONT(8)
        )
        self.direct_files_label = ttk.Label(
            self.mainright_frame,
            textvariable=self.dirinfo.direct_files_total,
            width=25,
            anchor=W,
            font=APP_FONT(8)
        )

        # -- files
        self.files_label = ttk.Label(
            self.files_frame,
            textvariable=self.dirinfo.files_total,
            width=20,
            justify=LEFT,
            anchor=W,
            font=APP_FONT(12)
        )

        # -- folders
        self.subfolders_label = ttk.Label(
            self.folders_frame,
            textvariable=self.dirinfo.subdirs_total,
            width=20,
            justify=LEFT,
            anchor=W,
            font=APP_FONT(12)
        )

    
    def add_details(self):
        # pb_themes = [DANGER,WARNING,PRIMARY,INFO,SUCCESS,LIGHT]
        # i = 0

        # files progressbars
        for ext,files in self.dirinfo.content_files.items():
            label = ttk.Label(
                self.scrollfiles_frame,
                text=f"{ext}:  {self.get_ext_filetotal(ext)},  {self.get_ext_size(ext)}",
                anchor=W,
                justify=LEFT
            )
            self.ext_labels_list.append(label)
            self.get_ext_percentage(ext)
            progbar = ttk.Progressbar(
                self.scrollfiles_frame,
                # bootstyle=f"striped-{pb_themes[i]}",
                bootstyle="striped-warning",
                mode=DETERMINATE,
                value=self.get_ext_percentage(ext)
            )
            self.ext_progbars_list.append(progbar)
            # i = (i+1) % 6
        
        # subfolders
        previous_path = os.path.realpath(os.path.join(self.main_window.dirpath.get(), ".."))
        pp_label = tk.Button (
            self.scrollfolders_frame,
            text=f"..",
            cursor="hand2",
            command=lambda: self.change_directory(previous_path),
            width=5,
            font=APP_FONT(10)        
        )
        self.subdir_labels_list.append(pp_label)

        for directory in self.dirinfo.content_dirs:
            dirpath = directory.path
            temp_DI = DirInfo()
            temp_DI.update(dirpath)
            label = ttk.Button(
                self.scrollfolders_frame,
                text=f"{self.get_subdir_relpath(directory)} : {temp_DI.convert_bytes(temp_DI.get_total_size())}",
                bootstyle = self.dir_btn_theme_adapter(),
                cursor="hand2",
                command=lambda dirpath = dirpath: self.change_directory(dirpath) # wow what a trick
            )
            self.subdir_labels_list.append(label)
    
    # TODO: make it dynamic (adapt when theme is changed)
    def dir_btn_theme_adapter(self):
        if self.main_window.style.theme.type == "dark":
            return "outline-light"
        return "outline-dark"

    def change_directory(self, new_path):
        self.main_window.dirpath.set(new_path)
        self.main_window.analyse_dir()

    def get_subdir_relpath(self, subdir):
        return subdir.path.replace(self.main_window.dirpath.get(),"")

    def get_ext_percentage(self, file_ext):
        return round(self.dirinfo.content_files[file_ext][1] / self.dirinfo.get_total_size() * 100, 2)

    def get_ext_filetotal(self, file_ext):
        return f"{len(self.dirinfo.content_files[file_ext][0])} file(s)"

    def get_ext_size(self, file_ext):
        size = self.dirinfo.content_files[file_ext][1]
        return self.dirinfo.convert_bytes(size)


    def display(self, folder_selected):
        """folder_selected:
        False = no folder path selected
        True = folder path selected
        """
        if not folder_selected:
            self.pack()
            self.placeholder_label.pack(pady=15)

        else:
            self.placeholder_label.pack_forget()

            self.maininfo_frame.pack(padx=10, pady=10, fill=X)
            self.details_frame.pack(expand=True, fill=BOTH)
            self.mainleft_frame.pack(fill=Y, side=LEFT, padx=5, pady=5)
            self.mainright_frame.pack(fill=Y, side=RIGHT, padx=5, pady=(0,5))

            # self.files_frame.pack(expand=False, fill=BOTH, side=LEFT, padx=10, pady=10) old pack
            # self.folders_frame.pack(fill=BOTH, side=RIGHT, padx=10, pady=10)
            self.files_frame.place(x=10,y=5,relheight=0.95,relwidth=0.63)
            self.folders_frame.place(relx=0.65,y=5,relheight=0.95,relwidth=0.34)
            self.scrollfiles_frame.pack(expand=True,fill=BOTH, padx=5)
            self.scrollfolders_frame.pack(expand=True,fill=BOTH, padx=5)

            self.name_label.pack(fill=X, pady=(0,7))
            self.path_label.pack(fill=X, pady=(5,0))
            self.cat_label.pack(fill=X, pady=5)
            self.totalsize_label.pack(fill=BOTH,expand=True)
            self.direct_files_label.pack(fill=BOTH,expand=True)
            self.direct_subfolders_label.pack(fill=BOTH,expand=True)

            for label,progbar in list(zip(self.ext_labels_list,self.ext_progbars_list)):
                label.pack(pady=(7,0), padx=25, fill=X)
                progbar.pack(pady=(0,5), padx=(20,40) ,fill=X)

            self.subdir_labels_list[0].pack(pady=(10,8), padx=(20,40))
            for i in range(1, len(self.subdir_labels_list)):
                self.subdir_labels_list[i].pack(pady=(10,8), padx=(20,40), fill=X)
            
            self.files_label.pack(side=BOTTOM, pady=10)
            self.subfolders_label.pack(side=BOTTOM, pady=10, padx=15)


class SettingsTab(tk.Frame):
    def __init__(self, main_window, parent):
        super().__init__(parent)
        self.main_window = main_window
        self.light_themes = ["cosmo","flatly","journal","litera","lumen","minty","pulse","sandstone","united",
                             "yeti","morph","simplex","cerculean"]
        self.dark_themes = ["solar","superhero","darkly","cyborg","vapor"]

        self.main_frame = ttk.Labelframe(self, text="SELECT THEMES")
        self.themes_frame = ScrolledFrame(self.main_frame)

        self.light_frame = ttk.Frame(self.themes_frame)
        self.dark_frame = ttk.Frame(self.themes_frame)

        self.light_label = ttk.Label(self.light_frame, text="Light themes", font=APP_FONT(9))
        # self.sep = ttk.Separator(self.themes_frame)
        self.dark_label = ttk.Label(self.dark_frame, text="Dark themes", font=APP_FONT(9))


        self.display()


    def change_theme(self, new_theme):
        return lambda: self.main_window.style.theme_use(new_theme)


    def display(self):
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER, relheight=0.8, relwidth=0.7 )
        self.themes_frame.pack(fill=BOTH, expand=True)
        self.light_frame.pack(side=LEFT,fill=BOTH,expand=True)
        self.dark_frame.pack(side=LEFT,fill=BOTH,expand=True)

        self.light_label.pack(anchor=CENTER, pady=(20,25))
        for theme in self.light_themes:
            theme_label = ttk.Button(self.light_frame, text=theme, width=10, cursor="hand2", command=self.change_theme(theme)).pack(anchor=CENTER,pady=7)
        # self.sep.pack()
        self.dark_label.pack(anchor=CENTER, pady=(20,25))
        for theme in self.dark_themes:
            theme_label = ttk.Button(self.dark_frame, text=theme, width=10, cursor="hand2", command=self.change_theme(theme)).pack(anchor=CENTER,pady=7)
        # self.tree_view.pack()




if __name__ == "__main__":
    wimyfo = WimyfoApp()
    wimyfo.mainloop()