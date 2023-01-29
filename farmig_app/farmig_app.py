import pynecone as pc
from typing import List

##################data_file########################
class Fields(pc.Model, table=True):
    thirst: int
    plant: str 

class Farm(pc.Model, table=True): # global farm database
    my_plot: list = list[Fields]
    money: int

class User(pc.Model, table=True): # user database
    username: str
    password: str
    user_farm: list = list[Farm] #pointer to users farm/s

###################farm_app#########################
class main_farm_app(pc.State): #main page state
    farm: list[User]

class AuthState(main_farm_app): #the login box
    password: str
    confrim_password: str
    
    def signup(self): #method for the signup 
        pass 
    def login(self): #method for the login
        with pc.seesion() as session:
            user = session.exec(
                    User.select.where(User.username == self.username)
            ).first()
            if user and User.password == self.password:
                pass
                return pc.redirect("/")
            else:
                return pc.window_alert("invalid username or password")

def signup(): #when button is pressed 
    return pc.text("signup page")
def login():
    return pc.text("login page")
def home(): #when button is pressed
    return pc.vstack(
            pc.heading("farming App", size="4x1"),
            
            pc.link(
                pc.button("Login"),
                href="/login",
            ),
             pc.link(
                pc.button("Signup"),
                href="/signup",
            ),
            
        )

app = pc.App(state=main_farm_app)
app.add_page(home, path="/")
app.add_page(login, path="/login")
app.add_page(signup, path="/signup")
app.compile()
