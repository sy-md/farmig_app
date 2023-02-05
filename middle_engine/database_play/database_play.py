import pynecone as pc
import engine as eg

"""
we are saying fuck you pc.models and gonna
use a middle man

"""


class testing (pc.State):  # the state of the website
    name: str = ""
    user_info = []
    amount = []
    plant = {"corn": 3, "pear": 2}

    def push(self, push):
        self.name = push

    def makeData(self):
        self.user_info = eg.get_keys(self.plant)

    def makeamt(self):
        self.amount = eg.get_values(self.plant)


def blank():
    return pc.vstack(
            pc.input(
                placeholder="username",
                on_blur=testing.push  # set a username
            ),
            pc.button(
                "submit",
                on_click=[testing.makeData,testing.makeamt],
            ),
            pc.foreach(testing.user_info, test_loop),
            pc.text("name: ", testing.name),
            pc.text("amount: ", testing.amount)

        )


def test_loop(user_info):
    return pc.button(
            user_info
            )


app = pc.App(state=testing)
app.add_page(blank)
app.compile
