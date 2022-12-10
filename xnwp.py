from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, ScreenManager
from kivy.config import Config
from kivy.core.window import Window
from logic import *
from ui import *


class MainApp(MDApp):
    def __init__(self, env: Environment, **kwargs):
        super().__init__(**kwargs)
        self.env = env

    def build(self):
        sm = MDScreenManager()
        sm.add_widget(NotesListScreen(sm, self.env, name="notelist"))
        return sm

    def on_stop(self):
        self.env.save()


Config.set("kivy", "exit_on_escape", "0")
e = Environment().load()
MainApp(e).run()