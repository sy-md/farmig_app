import pynecone as pc
from typing import List

styles = {
    "login_page": {
        "padding_top": "10em",
        "text_align": "top",
        "position": "relative",
        "background_image": "bg.svg",
        "background_size": "100% auto",
        "width": "100%",
        "height": "100vh",
    },
    "login_input": {
        "shadow": "lg",
        "padding": "1em",
        "border_radius": "lg",
        "background": "white",
    },
}
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
         """Sign up a user."""
        with pc.session() as session:
            if self.password != self.confirm_password:
                return pc.window_alert("Passwords do not match.")
            if session.exec(User.select.where(User.username == self.username)).first():
                return pc.window_alert("Username already exists.")
            user = User(username=self.username, password=self.password)
            session.add(user)
            session.commit()
            self.logged_in = True
            return pc.redirect("/home")
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
    return pc.box(
        pc.vstack(
            navbar(State),
            pc.center(
                pc.vstack(
                    pc.heading("Sign Up", font_size="1.5em"),
                    pc.input(
                        on_blur=State.set_username, placeholder="Username", width="100%"
                    ),
                    pc.input(
                        on_blur=AuthState.set_password,
                        placeholder="Password",
                        width="100%",
                    ),
                    pc.input(
                        on_blur=AuthState.set_confirm_password,
                        placeholder="Confirm Password",
                        width="100%",
                    ),
                    pc.button("Sign Up", on_click=AuthState.signup, width="100%"),
                ),
                style=styles["login_input"],
            ),
        ),
        style=styles["login_page"],
    )
def login():
        return pc.box(
        pc.vstack(
            navbar(State),
            pc.center(
                pc.vstack(
                    pc.input(
                        on_blur=State.set_username, placeholder="Username", width="100%"
                    ),
                    pc.input(
                        on_blur=AuthState.set_password,
                        placeholder="Password",
                        type_="password",
                        width="100%",
                    ),
                    pc.button("Login", on_click=AuthState.login, width="100%"),
                    pc.link(
                        pc.button("Sign Up", width="100%"), href="/signup", width="100%"
                    ),
                ),
                style=styles["login_input"],
            ),
        ),
        style=styles["login_page"],
    )
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
