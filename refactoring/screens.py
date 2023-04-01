from typing import Any

from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from logic import XNWPProfile


class MainScreen(MDScreen):
    def __init__(
        self,
        screen_manager: MDScreenManager,
        profile: XNWPProfile,
        *args: Any,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.name = "mainscreen"

    def on_enter(self, *args: Any) -> None:
        Window.bind(on_keyboard=self.keypress)

    def on_pre_leave(self, *args: Any) -> None:
        Window.unbind(on_keyboard=self.keypress)

    def keypress(self, window: Any, key: int, keycode: int, *largs: Any) -> None:
        if key == 27:
            Window.close()
