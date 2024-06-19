import os
import ttkbootstrap as ttk
from datetime import date


class DirInfo():
    """
    A class that countains tkinter variables storing infos on provided directory path
    """
    def __init__(self):
        self.name = ttk.StringVar(value="None")
        self.path = ttk.StringVar(value="None")
        self.content_dirs, self.content_files = None,None
        self.total_size = ttk.StringVar(value="None")
        self.ct_date = ttk.StringVar(value="None")
        self.direct_subdirs_total = ttk.StringVar(value="None")
        self.direct_files_total = ttk.StringVar(value="None")
        self.subdirs_total = ttk.StringVar(value="None")
        self.files_total = ttk.StringVar(value="None")

    def update(self, pth: str):
        """Updates the tkinter variables based on arg 'pth'
        """
        #----- Folder Name -----------------------
        self.name.set(f"Name: {os.path.basename(pth)}")
        #----- Folder Path -----------------------
        self.path.set(f"Path: {pth}")
        #----- Folder Content --------------------
        self.content_dirs, self.content_files = self.get_dir_content(pth)
        #----- Folder Size -----------------------
        self.total_size.set(f"Total size: {self.convert_bytes(self.get_total_size())}")
        #----- Date Creation ---------------------
        self.ct_date.set(f"Creation date: {date.fromtimestamp(os.path.getctime(pth))}")
        #----- Number of direct subdirectory -----
        self.direct_subdirs_total.set(f"Direct subfolders: {self.get_direct_subdirs_total(pth)}")
        #----- Number of direct file -------------
        self.direct_files_total.set(f"Direct files: {self.get_direct_files_total(pth)}")
        #----- Total of all subdirectory ---------
        self.subdirs_total.set(f"Subfolders total: {len(self.content_dirs)}")
        #----- Total of all files ----------------
        self.files_total.set(f"Files total: {self.get_files_total()}")
        #-----------------------------------------
        

    def get_direct_files_total(self, pth: str):
        return len(list(filter(lambda file: file.is_file(), os.scandir(pth))))
    
    def get_direct_subdirs_total(self, pth: str):
        return len(list(filter(lambda file: file.is_dir(), os.scandir(pth))))

    def get_files_total(self):
        ft = 0
        for _,filenames in self.content_files.items():
            ft += len(filenames[0])
        return ft
    
    def get_total_size(self):
        ts = 0
        for _,size in self.content_files.values():
            ts += size
        return ts

    def convert_bytes(self, size: int) -> str:
        size_str = ""
        if size < 1024:
            size_str = f"{size}B"
        elif size < 1_048_576:
            size_str = f"{round(size/1024,2)}KB"
        elif size < 134_217_728:
            size_str = f"{round(size/1_048_576,2)}MB"
        else:
            size_str = f"{round(size/134_217_728,2)}GB"
        return size_str

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
            """Recursive get_dir_content"""
            for file in os.scandir(pth):
                if file.is_junction():
                    continue
                if file.is_dir() and file.name[0] != '.':
                    dirs.append(file)
                    rec_gdc(os.path.join(pth,file.name), dirs, ext_dict)

                elif file.is_file():
                    _, ext = os.path.splitext(file.name)
                    if ext == "":
                        ext = file.name
                    if ext in ext_dict:
                        ext_dict[ext][0].append(file)
                        ext_dict[ext][1] += file.stat().st_size
                    else:
                        ext_dict[ext] = [[file],file.stat().st_size]
        
        rec_gdc(starting_pth, dirs, ext_dict)
        ordered_ext_dict = dict(zip(ext_dict.keys(), sorted(ext_dict.values(), key=lambda l: l[1], reverse=True)))
        return dirs, ordered_ext_dict
