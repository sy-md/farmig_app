import pynecone as pc

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
# #################data_file########################


class Fields(pc.Model, table=True):
    thirst: int
    plant: str


class Farm(pc.Model, table=True):  # global farm database
    plot: list[str]
    money: int


class User(pc.Model, table=True):  # user database
    username: str
    password: str
    user_farm: list[str]  # pointer to users farm/s

# ##################farm_app#########################


class main_farm_app(pc.State):  # main page state
    farm: list[User]

class storeDrawer(main_farm_app):
    show_store: bool = False

    def open_store(self):
        self.show_store = not (self.show_store)  # clean way for opposite


class AuthState(main_farm_app):  # the login box
    username: str
    password: str
    confirm_password: str
    logged_in: str = False


    def signup(self):  # method for the signup
        """Sign up a user."""
        with pc.session() as session:
            #add functionally of securece
            user = User(username=self.username, password=self.confirm_password, user_farm=self.testing)
            session.add(user)
            session.commit()
        self.logged_in = True
        return pc.redirect("/login")

    def login(self):  # method for the login
        with pc.session() as session:
            user = session.exec(
                    User.select.where(User.username == self.username)).first()
            if user and user.password == self.password:
                return pc.redirect("/home")
            else:
                return pc.window_alert("invalid")


class plots(main_farm_app):
    row1 = ["#","#","#"]
    row2 = ["#","#","#"]
    row3 = ["#","#","#"]
    row4 = ["#","#","#"]

    rows = [row1,row2,row3,row4] # while conditon

#  HTML
def get_seed(row1):
    return pc.button(
            row1
            )

def create_tab(rows): # use container
    return pc.tab_panel(
                pc.hstack(
                    pc.foreach(
                        plots.row1, get_seed,
                    )
                )
            )

def myfarm():
    return pc.container(
            pc.tabs(
                pc.tab_list(
                    pc.tab("farm 1"),
                    pc.spacer(),
                    pc.tab("farm 2"),
                    pc.spacer(),
                    pc.tab("farm 3"),
                    pc.spacer(),
                    pc.tab("farm 4"),
                ),
                pc.tab_panels(
                    pc.foreach( plots.rows, create_tab),
                )
            ),
            pc.box(
                pc.hstack(
                    pc.button(" Water "),
                    pc.spacer(),
                    pc.button(" Plant "),
                    pc.spacer(),
                    pc.button(" Uproot "),
                    pc.spacer(),
                    pc.button(
                        pc.link(
                            "Store", on_click=storeDrawer.open_store, color="rgb(107,99,246)"
                        ),
                        pc.box(
                            pc.drawer(
                                pc.drawer_overlay(
                                    pc.drawer_content(
                                        pc.drawer_header("Store"),
                                        pc.drawer_body("nothong"),
                                        pc.drawer_footer(
                                            pc.button("Close", on_click=storeDrawer.open_store)
                                        ),
                                    )
                                ),  # the overlay
                                is_open=storeDrawer.show_store,
                            ),  # the drawer
                        )
                    )
                )
            ),
            pc.avatar(name=AuthState.username),
        )


def signup():  # when button is pressed
    return pc.box(
        pc.vstack(
            pc.center(
                pc.vstack(
                    pc.heading("Sign Up", font_size="1.5em"),
                    pc.input(
                        on_blur=AuthState.set_username,
                        placeholder="Username", width="100%"
                    ),
                    pc.input(

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
            pc.center(
                pc.vstack(
                    pc.input(
                        on_blur=AuthState.set_username, placeholder="Username", width="100%"
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


app = pc.App(state=main_farm_app)
app.add_page(login, path="/login")
app.add_page(signup, path="/signup")  # home page
app.add_page(myfarm, path="/home")
app.compile()
