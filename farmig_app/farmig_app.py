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
        "pl1-#",
        "pl2-#",
        "pl3-#",
        ]

    rows = [row1]  # get rid of this 
    index = 0
    thirst = 75
    tmp = "selected"
    dirt = 'rgb(140,66,31)'
    water = 'rgb(0,0,255)'
    render = ""

    needs_water: bool = False
    needs_plant: bool = False
    needs_harvest: bool = False
    needs_plow: bool =False

    def check_plant(self, row1):
        chose = row1  # the plant
        plnt_type = 3  # the plant name
        plnt = 4 # the stae of the plant
        dirt = "#"
        wet = "_"

        self.tmp = chose

        if chose[plnt] != dirt and chose[plnt] != wet:  # is a plant
            # state to if the plant is ready to be harvest
            if self.thirst >= 50:
                self.needs_water = True
            else:
                self.needs_water = True
                self.needs_harvest = True
            self.needs_plant =False
            self.needs_plow = False
        else:  # is dirt or wet
            if chose[plnt] == dirt:
                self.needs_plow = True
                self.needs_plant =False
                self.needs_water =False
            if chose[plnt] == wet:
                self.needs_plow = False
                self.needs_plant = True
                self.needs_water=False
        

    def water_plant(self):
        for x in self.row1:
            if x == self.tmp:
                self.row1[self.index] = self.row1[self.index][0] + "{}{}-{}".format("l",(self.index+1), 'c')
            else:
                self.index += 1
        self.index = 0

    def plow_plant(self):
        for x in self.row1:
            if x == self.tmp:
                self.row1[self.index] = self.row1[self.index][0] + "{}{}-{}".format("l",(self.index+1),"_")
            else:
                self.index += 1
        self.index = 0

    def harvest_plant(self):
        for x in self.row1:
            if x == self.tmp:
                self.row1[self.index] = self.row1[self.index][0] + "{}{}-{}".format("l",(self.index+1),"#")
            else:
                self.index += 1
        self.index = 0

    def plant_plant(self):
        for x in self.row1:
            if x == self.tmp:
                self.row1[self.index] = self.row1[self.index][0] + "{}{}-{}".format("l",(self.index+1),"pick")
            else:
                self.index += 1
        self.index = 0




class Inventory(main_farm_app):
    stg = [
        ["corn " ,5],
        ["skfj"],
        [""],
        [""],
        [""],
        [""],
        [""],
    ]

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
                        on_click=lambda: plots.check_plant(row1)
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
                ),
                pc.tab_panels(
                    pc.foreach(plots.rows, create_tab),
                )
            ),
            pc.box(
                pc.hstack(
                    pc.button("plow", is_active=plots.needs_plow , on_click=plots.plow_plant),
                    pc.spacer(),
                    pc.button("Plant", is_active=plots.needs_plant , on_click=plots.plant_plant),
                    pc.spacer(),
                    pc.button("Harvest", is_active=plots.needs_harvest, on_click=plots.harvest_plant),
                    pc.spacer(),
                    pc.button("Water", is_active=plots.needs_water, on_click=plots.water_plant),
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
                        pc.foreach(Inventory.stg, make_iventory),
                    ),
                    center_content=True,
                )
            )
        )

def make_iventory(stg):
    return pc.box(
        pc.button(
            stg
        ),
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
