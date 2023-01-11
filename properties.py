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
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivy.core.window import Window
from notes import NotesList
from logic import *

def eval_or_str(s: str) -> object:
    '''Возвращает объект из строки, либо строку в случае любой ошибки'''
    try:
        return eval(s)
    except:
        return s


class PropertyEditorTopBar(MDTopAppBar):
    def __init__(self, screen_manager, environment: Environment, property: Property, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.environment: Environment = environment
        self.note: Property = property
        self.title = "Свойство"


class PropertyEditor(MDScreen):
    def __init__(self, screen_manager: MDScreenManager, environment: Environment, screen_from: str, property: Property, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "property"
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_from: str = screen_from
        self.property: Property = property
        box = MDBoxLayout()
        box.orientation = "vertical"
        box.add_widget(PropertyEditorTopBar(screen_manager, environment, property))
        sv = MDScrollView()
        bl = MDList()
        bl.add_widget(MDLabel(text="Имя свойства:", height=50))
        bl.add_widget(MDTextField())
        bl.add_widget(MDLabel(text="Значение:", height=50))
        bl.add_widget(MDTextField())
        sv.add_widget(bl)
        box.add_widget(sv)
        self.add_widget(box)
    
    def exit_saving(self):
        pass

    def exit_without_saving(self):
        pass
    
    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            self.screen_manager.current = self.screen_from
            self.screen_manager.remove_widget(self)
            self.exit_saving()