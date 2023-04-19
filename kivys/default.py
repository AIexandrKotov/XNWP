from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import (
    IconLeftWidget,
    MDList,
    OneLineAvatarListItem,
    OneLineIconListItem,
    OneLineListItem,
    TwoLineIconListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.textfield import MDTextField

KV = """
<DrawerClickableItem@MDNavigationDrawerItem>


<DrawerLabelItem@MDNavigationDrawerItem>
    focus_behavior: False
    _no_ripple_effect: True


MDScreen:

    MDNavigationLayout:

        MDScreenManager:
            id: scrm
            MDScreen:
                name: "edit_property"
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: 25
                    MDTopAppBar:
                        title: "Редактор свойства"
                        elevation: 2
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["repeat"]]
                    MDScrollView:
                        MDList:
                            cols: 1
                            spacing: 25
                            padding: 50, 0, 50, 0
                            MDTextField:
                                mode: "rectangle"
                                hint_text: "Название свойства"
                                text: "Имя персонажа"
                            MDTextField:
                                mode: "rectangle"
                                hint_text: "Значение свойства"
                                text: "Евгений Петросян"
                                multiline: True
                            MDRaisedButton:
                                text: "Сгенерировать значение"
                                font_size: 16
                            MDBoxLayout:
                                orientation: "horizontal"
                                spacing: 16
                                adaptive_height: True
                                MDTextField:
                                    icon_left: "android"
                                    text: "android"
                                    mode: "rectangle"
                                    readonly: True
                                    hint_text: "Иконка свойства"
                                MDRaisedButton:
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    text: "Сменить иконку"
                                    font_size: 16
                            MDTextField:
                                mode: "rectangle"
                                hint_text: "Генератор"
                                text: "Отсутствует"
                                readonly: True
                            MDBoxLayout:
                                orientation: "horizontal"
                                spacing: 16
                                adaptive_height: True
                                adaptive_width: True
                                MDRaisedButton:
                                    text: "Настройки генератора"
                                    font_size: 16
                                MDRaisedButton:
                                    text: "Выбрать другой"
                                    font_size: 16
                            # MDTabs:
                            #     padding: 0, 0, 0, 0
                            #     NoGeneratorTab:
                            #         title: "Нет"
                            #     DigitGeneratorTab:
                            #         title: "Число"
                            #     DatabaseChooseGeneratorTab:
                            #         title: "ДБ-выбор"
                            #     DatabaseRanameGeneratorTab:
                            #         title: "ДБ-Raname"
                            #     ChooseGeneratorTab:
                            #         title: "Выбор"
                            #     RanameGeneratorTab:
                            #         title: "Raname"
                            #     CodeGeneratorTab:
                            #         title: "Python"
            
                            
            MDScreen:
                name: "persons"
                MDBoxLayout:
                    orientation: "vertical"
                    MDTopAppBar:
                        title: "Главные герои"
                        elevation: 2
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["content-paste"], ["plus-circle-outline"], ["plus"]]
                        # вставить из буфера, 
                        # добавить полностью пустонго персонажа,
                        # добавить персонажа из шаблонов
                    MDScrollView:
                        MDList:
                            TwoLineListItem:
                                text: "Евгений Петросян"
                                secondary_text: "Мужик из подворотни"
                                on_release: app.edit_person_dialog()
                        

            MDScreen:
                name: "persons_group"
                MDBoxLayout:
                    orientation: "vertical"
                    MDTopAppBar:
                        title: "Мои персонажи"
                        elevation: 2
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["plus", lambda x: app.make_add_group_dialog()]]
                    MDScrollView:

                        MDList:
                            TwoLineListItem:
                                text: "Главные герои (1)"
                                secondary_text: "Евгений Петросян"
                            TwoLineListItem:
                                text: "Второстепенные персонажи (12)"
                                secondary_text: "Иван Иванов, Сергей Сергеев, Алексей Алексеев и другие"

            MDScreen:
                name: "edit_person"
                MDBoxLayout:
                    orientation: "vertical"
                    MDTopAppBar:
                        title: "Редактирование персонажа"
                        elevation: 2
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["creation"], ["autorenew-off"]]
                        # создание (сгенерировать всё), режим генератора
                    MDScrollView:

                        MDList:

                            OneLineListItem:
                                text: "ОСНОВНЫЕ ХАРАКТЕРИСТИКИ"

                            TwoLineIconListItem:
                                text: "Евгений Петросян"
                                secondary_text: "Имя персонажа"
                                on_release: app.delete_property_dialog()

                                IconLeftWidget:
                                    icon: "account"

                            TwoLineIconListItem:
                                text: "18"
                                secondary_text: "Возраст"

                                IconLeftWidget:
                                    icon: "border-none-variant"

                            OneLineIconListItem:
                                text: "Редактировать"
                                on_release: app.edit_property_group_dialog()

                                IconLeftWidget:
                                    icon: "cog"

                            OneLineListItem:
                                text: "ИСТОРИЯ ПЕРСОНАЖА"

                            TwoLineIconListItem:
                                text: "Родился в бедной семье на окраине Нью-Йорка"
                                secondary_text: "Рождение"

                                IconLeftWidget:
                                    icon: "book"

                            TwoLineIconListItem:
                                text: "Рос в ужасных условиях"
                                secondary_text: "Детство"

                                IconLeftWidget:
                                    icon: "book"

                            TwoLineIconListItem:
                                text: "С детства попал на войну"
                                secondary_text: "Юность"

                                IconLeftWidget:
                                    icon: "book"

                            TwoLineIconListItem:
                                text: "И получил пулю в лоб"
                                secondary_text: "Смерть"

                                IconLeftWidget:
                                    icon: "book"

                            OneLineIconListItem:
                                text: "Редактировать"
                                on_release: app.edit_property_group_dialog()

                                IconLeftWidget:
                                    icon: "cog"

                            OneLineListItem:
                                text: "ДОБАВИТЬ НОВУЮ ГРУППУ СВОЙСТВ"

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "XNWP"
                    text: "eXtended Notes for Writers"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

                MDNavigationDrawerLabel:
                    text: "Основные"

                DrawerClickableItem:
                    icon: "account-multiple"
                    right_text: "12"
                    text: "Мои персонажи"

                DrawerClickableItem:
                    icon: "lightbulb-variant-outline"
                    right_text: "5"
                    text: "Мои заметки"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    text: "Окружение"

                DrawerClickableItem:
                    icon: "account-box-multiple"
                    right_text: "3"
                    text: "Мои шаблоны"

                DrawerClickableItem:
                    icon: "database"
                    right_text: "200"
                    text: "Мои свойства"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    text: "Тестирование"

                DrawerClickableItem:
                    icon: "car-shift-pattern"
                    right_text: ""
                    text: "Список персонажей группы"
                    on_release: scrm.current = "persons"

                DrawerClickableItem:
                    icon: "car-shift-pattern"
                    right_text: ""
                    text: "Группы персонажей"
                    on_release: scrm.current = "persons_group"

                DrawerClickableItem:
                    icon: "car-shift-pattern"
                    right_text: ""
                    text: "Редактор персонажа"
                    on_release: scrm.current = "edit_person"

                DrawerClickableItem:
                    icon: "car-shift-pattern"
                    right_text: ""
                    text: "Редактор свойства"
                    on_release: scrm.current = "edit_property"

                MDNavigationDrawerDivider:

                DrawerLabelItem:
                    icon: "information-outline"
                    text: "0.3.0"


<DigitGeneratorTab>
    MDGridLayout:
        padding: 0, 20, 0, 20
        spacing: 20
        cols: 2
        MDTextField:
            mode: "rectangle"
            hint_text: "Нижнее значение"
            text: "0"
        MDTextField:
            mode: "rectangle"
            hint_text: "Верхнее значение"
            text: "100"
<ChooseGeneratorTab>
    MDScrollView:
        MDList:
            OneLineListItem:
                text: "Первое значение"
            OneLineListItem:
                text: "Второе значение"
            OneLineIconListItem:
                text: "Добавить значение"
                IconLeftWidget:
                    icon: "plus"
<RanameGeneratorTab>
    MDBoxLayout:
        MDGridLayout:
            padding: 0, 20, 0, 20
            spacing: 20
            cols: 2
            MDTextField:
                mode: "rectangle"
                hint_text: "Минимальная глубина"
                text: "1"
            MDTextField:
                mode: "rectangle"
                hint_text: "Максимальная глубина"
                text: "5"
            MDTextField:
                mode: "rectangle"
                hint_text: "Только центральные"
                text: "True"
        MDScrollView:
            MDList:
                OneLineListItem:
                    text: "Первое значение"
                OneLineListItem:
                    text: "Второе значение"
                OneLineIconListItem:
                    text: "Добавить значение"
                    IconLeftWidget:
                        icon: "plus"
<DatabaseChooseGeneratorTab>
    MDGridLayout:
        padding: 0, 20, 0, 20
        spacing: 20
        cols: 1
        MDTextField:
            mode: "rectangle"
            hint_text: "Название базы данных"
            text: "db_name"
<DatabaseRanameGeneratorTab>
    MDGridLayout:
        padding: 0, 20, 0, 20
        spacing: 20
        cols: 2
        MDTextField:
            mode: "rectangle"
            hint_text: "Название базы данных"
            text: "db_name"
        MDTextField:
            mode: "rectangle"
            hint_text: "Только центральные"
            text: "True"
        MDTextField:
            mode: "rectangle"
            hint_text: "Минимальная глубина"
            text: "1"
        MDTextField:
            mode: "rectangle"
            hint_text: "Максимальная глубина"
            text: "5"
<CodeGeneratorTab>
    MDGridLayout:
        padding: 0, 20, 0, 20
        spacing: 20
        cols: 2
        MDTextField:
            multiline: True
            mode: "rectangle"
            hint_text: "Python"
            text: "xnwp(100)"
<NoGeneratorTab>
    MDGridLayout:
        padding: 0, 20, 0, 20
        spacing: 20
        cols: 1
        MDLabel:
            text: "У данного свойства отсутствует генератор. Выберите и настройте генератор, а затем нажмите кнопку в правом верхнем углу"
            valign: "top"
            halign: "center"
"""


class My2Item(TwoLineIconListItem, TouchBehavior):
    pass


class CodeGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class NoGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class DigitGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class ChooseGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class DatabaseChooseGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class DatabaseRanameGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class RanameGeneratorTab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class DialogOneLineIconItem(OneLineIconListItem):
    divider = None

    def __init__(self, text, icon, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.add_widget(IconLeftWidget(icon=icon))


class Example(MDApp):
    delete_dialog = None
    edit_group_dialog = None
    add_group_dialog = None
    edit_person = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Purple"
        return Builder.load_string(KV)

    def delete_property_dialog(self):
        if not self.delete_dialog:
            self.delete_dialog = MDDialog(
                text="Вы точно хотите удалить это свойство?",
                buttons=[
                    MDFlatButton(
                        text="Отменить",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="Удалить его",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self.delete_dialog.open()

    def edit_person_dialog(self):
        if not self.edit_person:
            self.edit_person = MDDialog(
                title="Редактировать персонажа",
                type="simple",
                items=[
                    DialogOneLineIconItem(
                        text="Переместить выше", icon="arrow-collapse-up"
                    ),
                    DialogOneLineIconItem(
                        text="Переместить ниже", icon="arrow-collapse-down"
                    ),
                    DialogOneLineIconItem(
                        text="Копировать в буфер", icon="content-copy"
                    ),
                    DialogOneLineIconItem(
                        text="Вырезать персонажа", icon="content-cut"
                    ),
                    DialogOneLineIconItem(
                        text="Удалить персонажа", icon="account-remove"
                    ),
                ],
            )
        self.edit_person.open()

    def edit_property_group_dialog(self):
        if not self.edit_group_dialog:
            self.edit_group_dialog = MDDialog(
                title="Редактировать группу",
                type="simple",
                items=[
                    DialogOneLineIconItem(
                        text="Добавить свойство", icon="plus-circle-outline"
                    ),
                    DialogOneLineIconItem(text="Создать свойство", icon="plus"),
                    DialogOneLineIconItem(text="Удалить группу свойств", icon="delete"),
                ],
            )
        self.edit_group_dialog.open()

    def make_add_group_dialog(self):
        if not self.add_group_dialog:
            self.add_group_dialog = MDDialog(
                title="Добавить группу",
                buttons=[
                    MDFlatButton(
                        text="Отменить",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="Создать группу",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
            textfield = MDTextField()
            textfield.padding = [25, 0, 25, 0]
            self.spacing = "10dp"
            self.add_group_dialog.add_widget(textfield)
        self.add_group_dialog.open()


Example().run()
