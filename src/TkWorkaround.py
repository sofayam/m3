import sys
def raiseWindow(root):
    # this was a false alarm caused by a threading conflict btw tkinter and xmlrpclib
    # but raising windows in Tk can be very platform dependant - so we have left it in
    if sys.platform == "win32":
        root.focus_force()
        root.tkraise()        
    else:
        root.focus_force()
        root.tkraise()
