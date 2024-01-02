############################
#    Application Name     #
#        MySQL2FTP        #
###########################


#tested funcitons encapsulated
from support.functions import *
from tkinter.ttk import Progressbar
#creates necesary paths needed for application to run
from support.path import * 
APPNAME = 'MySQL2FTP'
splashMessage = """
############################
#    Application Name     #
#        MySQL2FTP        #
###########################
"""


def mSQL2CSV():#Wrapped function for Button
    bar.start(10)
    try:
        logMsg = runmSQL2CSV()
        messagebox.showinfo(title=APPNAME, message=logMsg)   
    except:
        pass
    finally:
        bar.stop()

def runmSQL2CSV():#Connect to MySQL DB, run query and store as a CSV File
    try:
        return SQL2CSV(getEngine(config['DB']),loadQuery('query.sql'),config['DB']['dbname'],CSVfile)
    except:
        error= 'There was an issue retriving/processing records.'
        log(error)
        messagebox.showerror(title=APPNAME, message=error)


def CSV2FTP():#Wrapped function for Button
    bar.step(10)
    try:
        logMsg = runCSV2FTP()
        if logMsg != None:
            messagebox.showinfo(title=APPNAME, message=logMsg)
    except:
        pass
    finally:
        bar.stop()

def runCSV2FTP():#Upload CSV File to FTP Site
    try:
        return Upload(CSVfile,config['FTP'])
    except:
        error= 'There was an issue uploading the CSV File. The local file is stored at\n\t'+ CSVfile
        log(error)
        messagebox.showerror(title=APPNAME, message=error)
        
    
def SQL2FTP():
    bar.start(19)
    try:
        runmSQL2CSV()
        runCSV2FTP()
        messagebox.showinfo(title=APPNAME, message="Data was stored and uploaded!")
    except:
        pass
    finally:
        bar.stop()

#########
#  End of Definitons
#########



log("Test run v1.0")

#Load configuration and minor file checks.
configFile = 'MySQL2FTP.conf'
config = loadConfig(configFile)
if len(config.sections()) < 2 or len(config.sections()[0]) < 2:
    log("Issues with MySQL2FTP.conf file. Ensure it exist and is not blank.")
    

#Create file name for CSV File
CSVfile = "docs\\"+ config['FTP']['filename'] + getDate() +".csv"

log('Config Initialized.')



#########
#  End of Initializaiton
#########


root = Tk()

root.geometry("400x140")
root.title(APPNAME)
root.resizable(0, 0)
root.iconbitmap("MySQL2FTP.ico")
root.grid()

bar = Progressbar(root,orient=HORIZONTAL,length=80,mode="indeterminate",takefocus=True,maximum=100)
bar.grid(column=3,columnspan=2, row=5)

ttk.Label(root, text="Status:").grid(column=0, row=0)
FileLabel = "File: \n" + CSVfile
ttk.Label(root, text=FileLabel).grid(column=0, row=2)
button = ttk.Button(root, text="Run All", command=SQL2FTP).grid(column=5, row=0)
ttk.Button(root, text="SQL to CSV", command=mSQL2CSV).grid(column=5, row=2)
ttk.Button(root, text="CSV to FTP", command=CSV2FTP).grid(column=5, row=3)
ttk.Button(root, text="Quit", command=root.destroy).grid(column=5, row=5)



root.mainloop()

#########
#  End of GUI
#########


log('Successful Run Complete!')


