import os
import ttkbootstrap as ttk
from datetime import date


class DirInfo():
    """
    A class that countains tkinter variables storing infos on provided directory path

    Attributes:
            name: (ttk.StringVar)
                Name of the folder
            
            path: (ttk.StringVar)
                Path of the folder

            content_dirs: (ttk.StringVar)
                Content of the folder and its subfolders returned by get_dir_content

            total_size: (ttk.StringVar)
                Total occupied size by the folder

            ct_date: (ttk.StringVar)
                Creation date of the folder
            
            direct_subdirs_total: (ttk.StringVar)
                Number of direct subdirectory (subdirs that are directly in current folder and not themselves in a subfolder)

            direct_files_total: (ttk.StringVar)
                Number of direct file (files that are directly in current folder and not in a subfolder)

            subdirs_total: (ttk.StringVar)
                Total number of all subdirectory

            files_total: (ttk.StringVar)
                Total number of all files
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
        """Updates the tkinter variables

        Parameters:
            pth: (str)
                path to retrieve infos from
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
        

    def get_direct_files_total(self, pth: str) -> int:
        """Returns number of direct files
        
        Parameters:
            pth: (str)
                path to get files number from
        """
        return len(list(filter(lambda file: file.is_file(), os.scandir(pth))))
    
    def get_direct_subdirs_total(self, pth: str) -> int:
        """Returns number of direct subdirectories
        
        Parameters:
            pth: (str)
                path to subdirectories number from
        """
        return len(list(filter(lambda file: file.is_dir(), os.scandir(pth))))

    def get_files_total(self) -> int:
        """Returns the total number of all files
        """
        ft = 0
        for _,filenames in self.content_files.items():
            ft += len(filenames[0])
        return ft
    
    def get_total_size(self) -> int:
        """Returns total size of current directory
        ! only work after self.update has been ran
        """
        ts = 0
        for _,size in self.content_files.values():
            ts += size
        return ts

    def convert_bytes(self, size: int) -> str:
        """Returns the given size in a more user-friendly way.
        the size is left to Bytes or converted to Kilobytes, Megabytes or Gigabytes depanding on given size
        
        Parameters: 
            size: (int)
                size to convert to string
        """
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

    def get_dir_content(self, starting_pth: str) -> tuple[dict,dict]:
        """Returns info about specified directory path in a dict where keys are file extensions & values are list of files with key's extension.
        Directories are also listed with 'dir' as key.
        Also return a copy of the extensions dict that is ordered by extension size

            Parameters:
                pth: (str)
                    the aboslute or relative path to retrieve info from

            Return type    : dict(str:list[list[DirEntry],int])
            Returned       : {'extension':[[<DirEntry 'filename'>], total_size_of_extension_in_bytes]}
            Return example : {'.txt': [[<DirEntry 'mytext'>, <DirEntry 'notes'>], 2840]}
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
