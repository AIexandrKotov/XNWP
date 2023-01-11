from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, ScreenManager
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import *
from kivymd.uix.stacklayout import MDStackLayout
from kivy.core.window import Window
from properties import *
from notes import NotesList
from logic import *


class PersonsTab(MDBottomNavigationItem):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.name = "Persons"
        self.text = "Персонажи"
        self.icon = "account"


class MiscTab(MDBottomNavigationItem):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.name = "Misc"
        self.text = "Разное"
        self.icon = "animation"
        sl = MDBoxLayout()
        sl.orientation = "vertical"

        def start_props(_self):
            p = PropertyEditor(self.screen_manager, self.environment, "mainscreen", Property())
            self.screen_manager.add_widget(p)
            self.screen_manager.current = p.name
        
        def start_proplist(_self):
            ps = PropertiesScreen(self.screen_manager, self.environment)
            self.screen_manager.add_widget(ps)
            self.screen_manager.current = ps.name
        
        sl.add_widget(MDRectangleFlatButton(text="Тест свойств", on_release=start_props))
        sl.add_widget(MDRectangleFlatButton(text="Тест списка свойств", on_release=start_proplist))
        self.add_widget(sl)


class MainScreenTabs(MDBottomNavigation):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.add_widget(NotesList(screen_manager, environment))
        self.add_widget(PersonsTab(screen_manager, environment))
        self.add_widget(MiscTab(screen_manager, environment))


#
#   MainScreen - основной экран, содержащий страницы идей, персонажей и настроек
#


class MainScreen(MDScreen):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "mainscreen"
        self.add_widget(MainScreenTabs(screen_manager, environment))

    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            Window.close()


