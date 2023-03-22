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
from notes import NotesList
from old_logic import *

class PropertyItem(OneLineAvatarIconListItem, ILeftBodyTouch):
    def __init__(self, screen_manager, environment, screen_name: str, property_list: Optional[list[Property]], property: Property, mdlist: MDList, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_name = screen_name
        self.property_list: list[Property] = property_list
        self.property: Property = property
        self.name_w = MDLabel(text=self.property.name)
        self.mdlist = mdlist
        self.text = f"{property.name}: {property.value}"
        self.button = PropertyItemRightButton(environment, self.property_list, self.property, self)
        self.add_widget(self.button)
        self.update()
        self.ids._right_container.width = 120
    
    def delete(self):
        self.property_list.remove(self.property)
        self.mdlist.remove_widget(self)

    def update(self):
        self.text = f"{self.property.name}: {self.property.value}"
    
    def on_release(self):
        pe = PropertyEditor(self.screen_manager, self.environment, self.screen_name, self.mdlist, self, self.property)
        self.screen_manager.add_widget(pe)
        self.screen_manager.current = pe.name


class PropertyItemRightButton(IRightBodyTouch, MDRectangleFlatButton):
    def __init__(self, environment, property_item: PropertyItem, property: Property, left_prop: PropertyItem, **kwargs):
        super().__init__(**kwargs)
        self.environment: Environment = environment
        self.property_item = property_item
        self.property = property
        self.left_prop = left_prop
        self.text = "Случайное"
        self.pos_hint = { "center_y": 0.5 }

    def on_release(self):
        try:
            if self.property.has_generator():
                self.property.generate(self.environment)
                self.left_prop.update()
        except:
            pass
        

class PropertyList(MDScrollView):
    def __init__(self, screen_manager, environment, screen_name, property_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.property_list: list[Property] = property_list
        self.list = MDList()
        self.list.id = "container"
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_name: str = screen_name
        self.update_list()
        self.add_widget(self.list)
    
    def update_list(self):
        self.list.clear_widgets()
        for prop in self.property_list:
            self.list.add_widget(PropertyItem(self.screen_manager, self.environment, self.screen_name, self.property_list, prop, self.list))


class PropertyScreenTopBar(MDTopAppBar):
    def __init__(self, screen_manager, environment, plist: PropertyList, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.environment: Environment = environment
        self.properties = plist.property_list

        def add_new_property(x):
            property = Property()
            property.name = "Новое свойство"
            property.value = 0
            self.properties.append(property)
            plist.update_list()
        
        def add_new_sample_property(x):
            # todo
            pass

        self.right_action_items = [["plus", add_new_property, "Новое свойство"], ["plus-circle-outline", add_new_sample_property, "Свойство из шаблонов"]]


class PropertiesScreen(MDScreen):
    def __init__(self, screen_manager, environment, screen_from, properties: list[property], title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "plist"
        self.screen_from = screen_from
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        box = MDBoxLayout()
        box.orientation = "vertical"
        self.plist = PropertyList(screen_manager, environment, "plist", properties)
        box.add_widget(PropertyScreenTopBar(screen_manager, environment, self.plist, title=title))
        box.add_widget(self.plist)
        self.add_widget(box)
    
    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            self.screen_manager.current = self.screen_from
            self.screen_manager.remove_widget(self)


class PropertyEditorTopBar(MDTopAppBar):
    def __init__(self, screen_manager, environment: Environment, property_editor, pitem: PropertyItem, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.environment: Environment = environment
        self.property: Property = pitem.property
        self.property_list = pitem.property_list
        self.property_editor: PropertyEditor = property_editor
        self.title = "Свойство"

        def exit_without_save(x):
            self.screen_manager.current = "plist"
            self.screen_manager.remove_widget(property_editor)

        def delete(x):
            self.screen_manager.current = "plist"
            self.screen_manager.remove_widget(property_editor)
            pitem.delete()
            

        self.right_action_items = [
            ["delete", delete, "Удалить свойство"],
            ["content-save-off", exit_without_save, "Выйти без сохранения"],
        ]


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
    def __init__(self, screen_manager: MDScreenManager, environment: Environment, screen_from: str, plist: MDList, pitem: PropertyItem, property: Property, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "property"
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.screen_from: str = screen_from
        self.property: Property = property
        self.pitem = pitem
        box = MDBoxLayout()
        box.orientation = "vertical"
        box.add_widget(PropertyEditorTopBar(screen_manager, environment, self, pitem))
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
            except:
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
            self.pitem.update()