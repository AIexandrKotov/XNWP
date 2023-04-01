import os
from typing import Any

from kivy.config import Config
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from logic import XNWPProfile
from screens import MainScreen


class MainApp(MDApp):
    def __init__(self, profile: XNWPProfile, **kwargs: Any):
        super().__init__(**kwargs)
        self.profile = profile

    def build(self) -> MDScreenManager:
        screen_manager = MDScreenManager()
        screen_manager.add_widget(MainScreen(screen_manager, self.profile))
        return screen_manager

    def on_stop(self) -> None:
        self.profile.savefile(os.path.join("bin", "default.json"))


Config.set("kivy", "exit_on_escape", "0")
e = XNWPProfile.loadfile(os.path.join("bin", "default.json"))
MainApp(e).run()
