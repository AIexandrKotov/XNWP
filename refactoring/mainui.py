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
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Purple"
        return MainScreen(self.profile)

    def on_stop(self) -> None:
        self.profile.savefile(os.path.join("bin", "default.json"))


Config.set("kivy", "exit_on_escape", "0")
profile = XNWPProfile.loadfile(os.path.join("bin", "default.json"))
MainApp(profile).run()
