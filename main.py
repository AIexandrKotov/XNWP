from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, ScreenManager
from kivy.config import Config
from kivy.core.window import Window
from logic import *
from ui import *


class MainApp(MDApp):
    def __init__(self, environment: Environment, **kwargs):
        super().__init__(**kwargs)
        self.environment = environment

    def build(self):
        sm = MDScreenManager()
        sm.add_widget(MainScreen(sm, self.environment))
        return sm

    def on_stop(self):
        self.environment.save()


Config.set("kivy", "exit_on_escape", "0")
e = Environment().load()
MainApp(e).run()