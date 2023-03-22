from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem, MDList, BaseListItem, ILeftBodyTouch, IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager, ScreenManager
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.core.window import Window
from properties import *
from notes import NotesList
from old_logic import *
import copy

class PersonItem(TwoLineListItem, ILeftBodyTouch):
    def __init__(self, screen_manager, environment, screen_name: str, person_list: Optional[list[Person]], person: Person, mdlist: MDList, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_name = screen_name
        self.person_list: list[Person] = person_list
        self.person: Person = person
        self.mdlist = mdlist
        self.title = title
        self.text = str(self.person.properties[0].value)
        self.secondary_text = ' / '.join(str(x.value) for x in self.person.properties[1:5])[:100]
        self.update()
    
    def delete(self):
        self.person_list.remove(self.person)
        self.mdlist.remove_widget(self)

    def update(self):
        self.text = str(self.person.properties[0].value)
        self.secondary_text = ' / '.join(str(x.value) for x in self.person.properties[1:5])[:100]
    
    def on_release(self):
        pe = PropertiesScreen(self.screen_manager, self.environment, self.screen_name, self.person.properties, self.title)
        self.screen_manager.add_widget(pe)
        self.screen_manager.current = pe.name


class PersonList(MDScrollView):
    def __init__(self, screen_manager, environment, screen_name, person_list, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_list: list[Person] = person_list
        self.list = MDList()
        self.list.id = "container"
        self.title = title
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_name: str = screen_name
        self.update_list()
        self.add_widget(self.list)
    
    def update_list(self):
        self.list.clear_widgets()
        for person in self.person_list:
            self.list.add_widget(PersonItem(self.screen_manager, self.environment, self.screen_name, self.person_list, person, self.list, self.title))


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
            pass
        
        self.right_action_items = [["plus", add_new_person, "Новый персонаж"], ["plus-circle-outline", add_new_sample_person, "Персонаж из шаблонов"]]


class PersonsScreen(MDScreen):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.name = "persons"

        box = MDBoxLayout()
        box.orientation = "vertical"
        self.plist = PersonList(screen_manager, environment, "persons", self.environment.current_profile.sample_persons, title="Шаблон персонажа")
        box.add_widget(PersonsScreenTopBar(screen_manager, environment, self.plist, title="Шаблонные персонажи"))
        box.add_widget(self.plist)
        self.add_widget(box)
    
    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            self.screen_manager.current = "mainscreen"
            self.screen_manager.remove_widget(self)