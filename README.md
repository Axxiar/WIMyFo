<a name="readme-top"></a>

<!-- INTRO -->
# <img src=res/icon.ico align=center width=40> wimyfo.py - Folder statistics 
A desktop app that gives you stats about a specific folder and its files/subfolders


<img src=res/stats.png width=80%>

WIMyFo = What In My Folder

<br>

## About The Project

It is a project I've had in mind for a long time, but also challenge from "le P." ([@PierreHvrd](https://github.com/PierreHvrd)). 

Each of us had to create it on our own under 9 days.

**Check out his version [here](https://github.com/PierreHvrd/StatFiles)**

### Specifications
> - allow user to select the folder he want to analyse
> - give number of files of each type
> - give total number of files and subfolders
> - give occupied space by each type of file
> - give occupied space for each direct subfolder
> - give total occupied space by the folder
> - show statistics in a user-friendly way



### Built With 

![](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=FFFFFF&style=for-the-badge)
 
Modules : Tkinter + [ttkbootstrap](https://ttkbootstrap.readthedocs.io) (The theme by default is ["Superhero"](https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/)), os, datetime


<br>

## Getting Started

### Installation

``git clone`` the project

To launch the Graphical App run the `src/gui.py` script <br>
or run the `src/wimyfo.py` srcipt with the option `--gui` or `-g`

*example :*
```
> git clone https://github.com/Axxiar/WIMyFo.git
> python ./src/wimyfo.py --gui
```
<br>

## Roadmap
- [X] 🗝️ allow user to select the folder to analyse
- [X] 🗝️ give number of files of each type
- [X] 🗝️ give total number of files and subfolders
- [X] 🗝️ give occupied space by each type of file
- [X] 🗝️ give occupied space for each direct subfolder
- [X] 🗝️ give total occupied space by the folder
- [X] 🗝️ show everything in a graphical interface
- [X] 🔥 navigation system amongst folders
- [ ] ~~random colors for progressbars~~
- [X] 🔥 posibility to change the theme
- [ ] 🔥 option for hidden folders too
- [ ] 🔥 add possibility to execute in command line without graphic interface
- [ ] ❓ make the program an importable module
- [ ] ❓ optimizing navigation <!-- (quand on remonte/descned un dossier, concerve les infos précédentes pour réutiliser celles nécessaires) -->

🗝️: key feature<br>
🔥: cool extra feature idea<br>
❓: extra feature idea (wil probably not be added or at least not soon)
