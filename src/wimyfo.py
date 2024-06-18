import sys
from gui import WimyfoApp

if len(sys.argv) > 1:
    if sys.argv[1] in ("--gui", "-g"):
        gui = WimyfoApp()
        gui.mainloop()  