from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar, MDBottomAppBar
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem, MDList, BaseListItem, ILeftBodyTouch, IRightBodyTouch
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
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from notes import NotesList
from logic import *

class PropertyItem(BaseListItem, ILeftBodyTouch):
    def __init__(self, screen_manager, environment, screen_name: str, property_list: Optional[list[Property]], property: Property, mdlist: MDList, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_name = screen_name
        self.property_list: list[Property] = property_list
        self.property: Property = property
        self.name_w = MDLabel(text=self.property.name)
        self.mdlist = mdlist
        self.add_widget(self.name_w)
        self.value_w = MDLabel(text=str(self.property.name))
        self.add_widget(self.value_w)
        self.button = PropertyItemRightButton(self.property_list, self.property, self)
        self.add_widget(self.button)
        self.update()
    
    def delete(self):
        if self.property_list != None:
            self.property_list.remove(self.property)
            self.mdlist.remove_widget(self)

    def update(self):
        self.name_w.text = self.property.name
        self.value_w.text = str(self.property.value)
    
    def on_release(self):
        pe = PropertyEditor(self.screen_manager, self.environment, self.screen_name, self.property)
        self.screen_manager.add_widget(pe)
        self.screen_manager.current = pe.name


class PropertyItemRightButton(MDFlatButton, IRightBodyTouch):
    def __init__(self, property_item: PropertyItem, property: Property, left: PropertyItem, **kwargs):
        super().__init__(**kwargs)
        self.property_item = property_item
        self.property = property
        self.left = left
        self.text = "Генерировать"
    
    def on_release(self):
        if self.property.has_generator():
            self.property.generate()
            self.left.update()


class PropertyList(MDScrollView):
    def __init__(self, screen_manager, environment, screen_name, property_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.property_list: list[Property] = property_list
        self.list = MDList()
        for prop in property_list:
            self.list.add_widget(PropertyItem(screen_manager, environment, screen_name, property_list, prop, self.list))
        self.add_widget(self.list)

class PropertiesScreen(MDScreen):
    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "plist"
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        box = MDBoxLayout()
        box.orientation = "vertical"
        box.add_widget(PropertyEditorTopBar(screen_manager, environment, property))
        box.add_widget(PropertyList(screen_manager, environment, "plist", self.environment.current_profile.sample_properties))
        self.add_widget(box)
    
    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            self.save()
            self.screen_manager.current = self.screen_from
            self.screen_manager.remove_widget(self)


class PropertyEditorTopBar(MDTopAppBar):
    def __init__(self, screen_manager, environment: Environment, property: Property, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.environment: Environment = environment
        self.note: Property = property
        self.title = "Свойство"


class PropertyName(MDTextField):
    def __init__(self, property: Property, **kwargs):
        super().__init__(**kwargs)
        self.text = property.name


def eval_or_str(s: str) -> object:
    '''Возвращает объект из строки, либо строку в случае любой ошибки'''
    try:
        return eval(s)
    except:
        return s

def object_as_str(o: object) -> str:
    if type(o) is str: return '"'+o+'"'
    else: return str(o)

class PropertyValue(MDTextField):
    def __init__(self, property: Property, **kwargs):
        super().__init__(**kwargs)
        self.text = object_as_str(property.value)


class PropertyGenerator(MDTextField):
    def __init__(self, property: Property, **kwargs):
        super().__init__(**kwargs)
        self.text = property.generator


class PropertyGeneratorArguments(MDTextField):
    def __init__(self, property: Property, **kwargs):
        super().__init__(**kwargs)
        self.text = property.js_gargs


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
        bl = MDList()
        self.p_name = PropertyName(property)
        self.p_value = PropertyValue(property)
        self.p_generator = PropertyGenerator(property)
        self.p_arguments = PropertyGeneratorArguments(property)
        bl.add_widget(MDLabel(text="Имя свойства:"))
        bl.add_widget(self.p_name)
        bl.add_widget(MDLabel(text="Значение:"))
        bl.add_widget(self.p_value)
        bl.add_widget(MDLabel(text="Генератор:"))
        bl.add_widget(self.p_generator)
        bl.add_widget(MDLabel(text="Аргументы генератора:"))
        bl.add_widget(self.p_arguments)
        def gen_on_release(_self):
            try:
                if self.p_generator.text in environment.default_generators.keys():
                    self.p_value.text = object_as_str(self.property.agenerate(environment, self.p_generator.text, json.loads(self.p_arguments.text)))
            finally:
                pass

        bl.add_widget(MDFlatButton(text="Сгенерировать", on_release = gen_on_release))
        box.add_widget(bl)
        box.add_widget(MDLabel(text=Generator.get_generators_help()))
        self.add_widget(box)
    
    def save(self):
        self.property.name = self.p_name.text
        self.property.value = eval_or_str(self.p_value.text)
        self.property.generator = self.p_generator.text
        self.property.js_gargs = self.p_arguments.text

    def without_save(self):
        pass
    
    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            self.save()
            self.screen_manager.current = self.screen_from
            self.screen_manager.remove_widget(self)