# import libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,pandas
from tools import *

class Screen(QMainWindow): # create a class that is a subclass of the pyqt5 widget class
    
    def __init__(self):
        super().__init__() # initialize the widget
        self.widgets = {}
        self.setFixedSize(600,600) # set the position and the size
        self.setWindowTitle("Fitness Calculator") # set the title
        self.setStyleSheet("background: #161219;")  # set the colour
        self.excercises = pandas.read_csv("excercises.csv")
        try : # reads data about users and if no users are found create a new data file
            self.userdata = pandas.read_csv("users.csv")
            if (True in set(self.userdata["loggedin"])):
                self.username = list(self.userdata.loc[self.userdata["loggedin"]==True,"username"])[0]
                print(self.username)
                self.mainscreen()
            else:
                self.startscreen()
        except FileNotFoundError: # creates a new file if it doesn't exist
            frame = dict(username=["admin"],password=["adminpassword"],loggedin=[False])
            self.userdata = pandas.DataFrame(frame)
            self.userdata.to_csv("users.csv",mode="w",index=False)
            self.startscreen()

    #region - SCREENS -----------------------------------------
    def screen(func):#This updates the different frames so that each widget can be seen
        def wrapper(self):
            func(self)
            self.update()
        return wrapper
    
    
    @ screen
    def startscreen(self):
        self.clearscreen()
        # Creates a blank screen and then loads 3 widgets onto the screen - this is the first screen the user will see
        self.widgets = {
            "title": Text(self,"Fitness Calculator",(200,0),20),
            "login": Button(self,"Login",(200,60),func=self.loginscreen),
            "createuser" : Button(self,"Create new user",(200,140),func=self.createuserscreen)
        }
    
    @screen
    def mainscreen(self):
        # Creates a blank screen and then loads 3 widgets onto the screeb - this is the main screen 
        self.clearscreen()
        self.widgets = {
            "title": Text(self,"Main Menu",(200,0),20),
            "logout": Button(self,"Logout",(10,10),(100,70),self.logout),
            "addworkout": Button(self,"Add new workout",(200,140),func=self.addworkoutscreen),
        }
    
    @screen
    def createuserscreen(self):
        # This is the create user screen with 5 widgets about creating users
        self.clearscreen()
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.startscreen),
            "title": Text(self,"Create New User",(225,0),20),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "showpassword": Button(self,"Show",(410,120),(60,50),func=self.showpassword),
            "submit": Button(self,"Submit",(200,180),func=self.submitcreateuser)
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.showpass = False
        self.widgets["password"].setEchoMode(QLineEdit.Password) 
    
    @screen
    def loginscreen(self): #This is the login screen with 5 widgets about logging into the saved users
        self.clearscreen()
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.startscreen),
            "title": Text(self,"Login",(225,0),20),
            "username": LineEdit(self,"Username",(200,60)),
            "password": LineEdit(self,"Password",(200,120)),
            "showpassword": Button(self,"Show",(410,125),(50,40),func=self.showpassword,text_size=12),
            "RememberMe": CheckBox(self,"Remember me",(195,180)),
            "submit": Button(self,"Submit",(200,240),func=self.submitlogin)
            
        }
        #Sets the preview of the password field to dots for better security against shouldering
        self.showpass = False
        self.widgets["password"].setEchoMode(QLineEdit.Password)
    
    @screen
    def addworkoutscreen(self):
        self.clearscreen()
        self.buttnum = 0
        self.widgets= {
            "back" : Button(self,"Back",(10,10),(100,50),func=self.mainscreen),
            "title": Text(self,"Add excercise",(225,0),20),
            "scroll" : QScrollArea(self),
            "workoutbox": QGroupBox(self),
        }
        self.widgets["scroll"].move(10,100)
        self.widgets["scroll"].setFixedSize(580,490)
        self.widgets["scroll"].verticalScrollBar().setStyleSheet("""
    QScrollBar:vertical
    {
        background-color: none;
    }

    QScrollBar::handle:vertical
    {
        background-color: blue;      /* #605F5F; */
        min-width: 5px;
        border-radius: 4px;
    
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
    {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        background: none;
    }
    }
        """)
        labellist = []
        combolist = []
        myform = QFormLayout()
        for i in range(30):
            labellist.append(QLabel('mylabel'))
            combolist.append(QComboBox())
            myform.addRow(labellist[i],combolist[i])
        self.widgets["workoutbox"].setLayout(myform)
        self.widgets["scroll"].setWidgetResizable(True)
        self.widgets["scroll"].setWidget(self.widgets["workoutbox"])
    
    def update(self):
        for key, widget in self.widgets.items():
            print(key) # To check what widgets have been loaded
            widget.show()
        print()
    
    def clearscreen(self):# This clears the screen and ensures that it has been deleted from the widget dictionary
        print("screen cleared")
        for value in self.widgets.values():
            value.setParent(None) # deletes the widget from the screen
        self.widgets = {} # deletes it from the widget dictionary
    
        #This is extra functions of buttons that aren't changing frames so that I won't need to switch to the other 
        # script every time I need to create a new button
    
    #endregion SCREENS -------------------------------------------
    
    #region-BUTTONFUNCTIONS ---------------------------------
    def submitlogin(self): # controls what the submit button does in the login screen
        username,password = (self.widgets[i].text() for i in ["username","password"]) # creates a list with the text of each box
        if all(i == "" for i in (username,password)): # If every box is empty
            self.widgets["submit"].notice(0.5,"Boxes aren't filled","Submit")
        else:
            if username not in set(self.userdata["username"]): # Checks if the username does not exists
                self.widgets["submit"].notice(0.5,"Username does not exist","Submit")
                print(self.userdata["username"])
            else:
                if self.userdata.loc[self.userdata["username"] == username,"password"].values[0] != password: #Checks if the password doesnt match
                    self.widgets["submit"].notice(0.5,"Password incorrect","Submit")
                else:
                    
                    self.userdata.loc[self.userdata["username"]==username,"loggedin"] = self.widgets["RememberMe"].isChecked()
                    self.userdata.to_csv("users.csv",mode="w",index=False)
                    self.username = username
                    self.clearscreen()
                    self.mainscreen()
        
    def submitcreateuser(self): # controls what the submit button does in the create user screen
        username,password = (self.widgets[i].text() for i in ["username","password"]) # creates a list with the text of each box
        if all(i == "" for i in (username,password)):# If every box is empty
            self.widgets["submit"].notice(0.5,"Boxes aren't filled","Submit")
        else:
            if username in set(self.userdata): # If the user already exists
                self.widgets["submit"].notice(0.5,"Username already exists","Submit")
            else:
                # Appends the new user and password into the dataframe
                newrow = pandas.DataFrame.from_records([{"username":username,"password":password,"loggedin":False}])
                self.userdata = pandas.concat([self.userdata, newrow])
                self.userdata.reset_index(drop=True) # Resets indexes
                self.widgets["submit"].notice(0.5,"User created","Submit")
                self.userdata.to_csv("users.csv",mode="w",index=False) # Saves to the the file
        
    def showpassword(self):
        self.showpass = not self.showpass
        if self.showpass:
            self.widgets["password"].setEchoMode(QLineEdit.Normal)
            self.widgets["showpassword"].setText("Hide")
        else:
            self.widgets["password"].setEchoMode(QLineEdit.Password)
            self.widgets["showpassword"].setText("Show")
    
    
    def createnewexcercise(self): # 1:Legs 2: Chest 3: Bicep 4: Tricep 5:Back 6:Shoulders 7:Lats 8: Core 9: Forearm 0: Full Body
        workout,muscle = (self.widgets[i].text() for i in ["workoutname","bodypart"])
        if all(i == "" for i in (workout,muscle)):# If every box is empty
            self.widgets["addworkout"].notice(0.5,"Boxes aren't filled","Submit")
        else:
            if workout in set(self.excercises): # If the user already exists
                self.widgets["addworkout"].notice(0.5,"Workout already exists","Submit")
            else:
                newrow = pandas.DataFrame.from_records([{"excercise":workout,"musclehit":muscle}])
                self.excercises = pandas.concat([self.excercises,newrow])
                self.excercises.reset_index(drop=True,inplace=True)
                self.widgets["addworkout"].notice(0.5,"Workout added","Add")
                self.excercises.to_csv("excercises.csv",mode="w",index=False)
                for i in ["workoutname","bodypart"]:
                    self.widgets[i].setParent(None)
                    del self.widgets[i]
                self.widgets["workoutname"] = LineEdit(self,"Workout Name",(150,100),(300,50))
                self.widgets["bodypart"] = LineEdit(self,"Muscle Group Hit",(150,160),(300,50))
                self.update()
        
    def logout(self):
        self.userdata.loc[self.userdata["username"]==self.username,"loggedin"] = False
        self.userdata.to_csv("users.csv",mode="w",index=False)
        self.startscreen()
    #endregion BUTTONFUNCTIONS ------------------------------


if __name__ == "__main__": # So that the script can't be executed indirectly
    app = QApplication(sys.argv) # Initializes the application
    window = Screen() # initializes the window by instantiating the screen class
    window.show()
    sys.exit(app.exec_()) # destroys the program to stop it running after the program has been closed.