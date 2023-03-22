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
from persons import *
from notes import NotesList
from old_logic import *

class PersonsScreenTopBar(MDTopAppBar):
    def __init__(self, screen_manager, environment: Environment, plist: PersonList, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.environment: Environment = environment

        def add_new_person(x):
            person = Person()
            property = Property()
            property.name = "Новое свойство"
            property.value = 0
            person.properties.append(property)
            self.environment.current_profile.persons.append(person)
            plist.update_list()
        
        def add_new_sample_person(x):
            person = copy.deepcopy(self.environment.current_profile.sample_persons[0])
            self.environment.current_profile.persons.append(person)
            plist.update_list()


        self.right_action_items = [["plus", add_new_person, "Новый персонаж"], ["plus-circle-outline", add_new_sample_person, "Персонаж из шаблонов"]]


class PersonsTab(MDBottomNavigationItem):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.name = "Persons"
        self.text = "Персонажи"
        self.icon = "account"

        box = MDBoxLayout()
        box.orientation = "vertical"
        self.plist = PersonList(screen_manager, environment, "mainscreen", self.environment.current_profile.persons, title="Персонаж")
        box.add_widget(PersonsScreenTopBar(screen_manager, environment, self.plist, title="Персонажи"))
        box.add_widget(self.plist)
        self.add_widget(box)


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
        
        def start_proplist(_self):
            ps = PropertiesScreen(self.screen_manager, self.environment, "mainscreen", self.environment.current_profile.sample_properties, "Шаблоны свойств")
            self.screen_manager.add_widget(ps)
            self.screen_manager.current = ps.name
        
        def start_perslist(_self):
            ps = PersonsScreen(self.screen_manager, self.environment)
            self.screen_manager.add_widget(ps)
            self.screen_manager.current = ps.name
        
        sl.add_widget(MDRectangleFlatButton(size_hint=[1.0, 0], text="Шаблонные свойства", on_release=start_proplist))
        sl.add_widget(MDRectangleFlatButton(size_hint=[1.0, 0], text="Шаблоны персонажей", on_release=start_perslist))
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


