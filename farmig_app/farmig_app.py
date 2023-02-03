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
    "home": {
        'backgroud': 'rgb(55,55,55)',

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
    inventory: dict[str, int]

# ##################farm_app#########################


class main_farm_app(pc.State):  # main page state
    farm: list[User] # the global tcaht with


class plots(main_farm_app):
    row1 = [
        ["1-#"],
        ["2-#"],
        ]

    rows = [row1]  # get rid of this 
    index = 0
    tmp = "selected"
    dirt = 'rgb(140,66,31)',
    water = 'rgb(0,0,255)',

    needs_water: bool = False
    needs_plant: bool = False
    ready: bool = False

    def dummy(self, row1):
        for k, v in enumerate(self.row1):
            if True: #k in row1[self.index][0]:
                self.tmp = row1 #row1[self.index][0]
                self.index = 0
            else:
                self.index += 1
        return plots.check_plant

    def check_plant(self):
        if self.row1[self.index] != "#":
            self.needs_plant = not (self.needs_plant)
        else:
            self.needs_water = not (self.needs_water)

    def water_plant(self):
        self.dirt = self.water

class Inventory(main_farm_app):
    stg = {}

class storeDrawer(main_farm_app):
    show_store: bool = False

    def open_store(self):
        self.show_store = not (self.show_store)  # clean way for opposite


class AuthState(main_farm_app):  # the login box
    username: str
    password: str
    confirm_password: str
    logged_in: str = False
    farms = plots

    def signup(self):  # method for the signup
        """Sign up a user."""
        with pc.session() as session:
            # add functionally of securece
            user = User(username=self.username, password=self.confirm_password, user_farm=self.farms)
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


class NumberInputState(main_farm_app):
    number: int


def get_seed(row1):
    return pc.container(
                pc.button(
                    pc.box(
                        row1,
                        on_click=lambda: plots.dummy(row1)
                    ),
                    border_radius="8em",
                    bg=plots.dirt,
                ),
                pc.text(plots.tmp),
                pc.text(plots.index)
            )


def create_tab(rows):  # use container
    return pc.tab_panel(
                pc.container(
                    pc.hstack(
                        pc.foreach(
                            plots.row1, get_seed,
                        )
                    )
                )
            )


def myfarm():
    return pc.container(
            pc.tabs(
                pc.tab_list(
                    pc.spacer(),
                    pc.tab("farm"),
                    pc.spacer(),
                    pc.tab("test")
                ),
                pc.tab_panels(
                    pc.foreach(plots.rows, create_tab),
                )
            ),
            pc.box(
                pc.hstack(
                    pc.button("Water", is_active=plots.needs_water, on_click=plots.water_plant),
                    pc.spacer(),
                    pc.button("Plant", is_active=plots.needs_plant),
                    pc.spacer(),
                    pc.button("Uproot", is_active=plots.ready),
                    pc.spacer(),
                    pc.button(
                        pc.link(
                            "Store",
                            on_click=storeDrawer.open_store,
                            color="rgb(107,99,246)"
                        ),
                        pc.box(
                            pc.drawer(
                                pc.drawer_overlay(
                                    pc.drawer_content(
                                        pc.drawer_header(
                                            pc.container(
                                                pc.heading(
                                                    "Store",
                                                    text_color="green",
                                                    text_align="center"
                                                ),
                                                pc.divider()
                                            ),
                                            pc.container(
                                                pc.hstack(
                                                    pc.stat_label("Cash"),
                                                    pc.stat_number("$00000"),
                                                ),
                                                center_content=True,
                                            ),
                                        ),
                                        pc.drawer_body(
                                            pc.responsive_grid(
                                                pc.badge(  # foreach comp from a database
                                                    "Wheat",
                                                    variant="subtle",
                                                    color_scheme="yellow",
                                                    text_align="center"
                                                ),
                                                pc.button(
                                                    pc.stat_number("$25"),
                                                ),
                                                pc.badge(
                                                    "Pears",
                                                    variant="subtle",
                                                    color_scheme="yellow",
                                                    text_align="center"
                                                ),
                                                pc.button(
                                                    pc.stat_number("$5"),
                                                ),
                                                pc.badge(
                                                    "Corn",
                                                    variant="subtle",
                                                    color_scheme="yellow",
                                                    text_align="center"
                                                ),
                                                pc.button(
                                                    pc.stat_number("$12"),
                                                )
                                            ),
                                            columns=[3],
                                            spacing="1",
                                        ),
                                        pc.drawer_footer(
                                            pc.button("Close", on_click=storeDrawer.open_store)
                                        ),
                                    )
                                ),  # the overlay
                                is_open=storeDrawer.show_store,
                            ),  # the drawer
                        )
                    )
                ),
                pc.divider(),
                pc.container(
                    pc.heading("Inventory"),
                    pc.container(
                        pc.responsive_grid(
                            # foreach comp from a invetory state
                            pc.text(Inventory.stg["test"])



                        ),
                        coloums=[4],
                        spacing="3",
                    ),
                    center_content=True
                ),
            )
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
