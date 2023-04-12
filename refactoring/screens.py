from __future__ import annotations

import copy
from typing import Any, Callable, Optional

from kivy.core.window import Window
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import (
    IconLeftWidget,
    MDList,
    OneLineIconListItem,
    ThreeLineListItem,
    TwoLineListItem,
)
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawer,
    MDNavigationDrawerDivider,
    MDNavigationDrawerHeader,
    MDNavigationDrawerItem,
    MDNavigationDrawerLabel,
    MDNavigationDrawerMenu,
    MDNavigationLayout,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from logic import Person, XNWPProfile

# ———————————————————————————————————————————————————————————————————————————
# ————————————————————————— Globals —————————————————————————
# ———————————————————————————————————————————————————————————————————————————


class DialogOneLineIconItem(OneLineIconListItem):
    divider = None

    def __init__(self, text: str, icon: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.text = text
        self.add_widget(IconLeftWidget(icon=icon))


# ———————————————————————————————————————————————————————————————————————————
# ————————————————————————— MyPersonsListScreen —————————————————————————
# ———————————————————————————————————————————————————————————————————————————


class EditPersounDialog(MDDialog):
    def __init__(
        self,
        person: Optional[Person],
        persons_screen: PersonsListScreen,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            title="Редактировать персонажа",
            type="simple",
            items=[
                DialogOneLineIconItem(
                    text="Переместить выше",
                    icon="arrow-collapse-up",
                    on_release=lambda x: self.move_up_person(),
                ),
                DialogOneLineIconItem(
                    text="Переместить ниже",
                    icon="arrow-collapse-down",
                    on_release=lambda x: self.move_down_person(),
                ),
                DialogOneLineIconItem(
                    text="Копировать в буфер",
                    icon="content-copy",
                    on_release=lambda x: self.copy_person(),
                ),
                DialogOneLineIconItem(
                    text="Вырезать персонажа",
                    icon="content-cut",
                    on_release=lambda x: self.cut_person(),
                ),
                DialogOneLineIconItem(
                    text="Удалить персонажа",
                    icon="account-remove",
                    on_release=lambda x: self.remove_person(),
                ),
            ],
            **kwargs,
        )
        self.person = person
        self.persons_screen = persons_screen

    def update_person(self, person: Person) -> EditPersounDialog:
        self.person = person
        return self

    def move_up_person(self) -> None:
        if self.person is None:
            return
        self.persons_screen.move_up_person(self.person)

    def move_down_person(self) -> None:
        if self.person is None:
            return
        self.persons_screen.move_down_person(self.person)

    def copy_person(self) -> None:
        if self.person is None:
            return
        self.persons_screen.copy_person(self.person)
        self.dismiss()

    def cut_person(self) -> None:
        if self.person is None:
            return
        self.persons_screen.cut_person(self.person)
        self.dismiss()

    def remove_person(self) -> None:
        if self.person is None:
            return
        self.persons_screen.remove_person(self.person)
        self.dismiss()


class PersonElement(ThreeLineListItem, TouchBehavior):
    def __init__(
        self,
        person: Person,
        persons_screen: PersonsListScreen,
    ) -> None:
        super().__init__()
        self.person = person
        self.person_screen = persons_screen
        self.update(self.person)

    def update(self, person: Optional[Person]) -> None:
        if person is None:
            return
        self.person = person
        self.text = PersonElement.get_text(self.person)
        self.secondary_text = PersonElement.get_sec_text(self.person)
        self.tertiary_text = PersonElement.get_ter_text(self.person)

    @staticmethod
    def get_text(person: Person) -> str:
        if len(person.properties) > 0 and len(person.properties[0][1]) > 0:
            return str(person.properties[0][1][0].value)
        return "> No first property"

    @staticmethod
    def get_sec_text(person: Person) -> str:
        if len(person.properties) > 0 and len(person.properties[0][1]) > 1:
            return str(person.properties[0][1][1].value)
        return ">> No second property"

    @staticmethod
    def get_ter_text(person: Person) -> str:
        if len(person.properties) > 0 and len(person.properties[0][1]) > 2:
            return str(person.properties[0][1][2].value)
        return ">>> No third property"

    def on_release(self) -> None:
        # todo open person editor
        pass

    def on_long_touch(self, touch: Any, *args: Any) -> None:
        if self.person is None:
            return
        self.person_screen.edit_persoun_dialog.update_person(self.person).open()


class PersonsListScreen(MDScreen):
    buffer: Optional[Person] = None

    def __init__(
        self,
        main_screen: MainScreen,
        nav_drawer: MDNavigationDrawer,
        profile: XNWPProfile,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = "persons_list"
        self.main_screen: MainScreen = main_screen
        self.nav_drawer = nav_drawer
        self.edit_persoun_dialog = EditPersounDialog(None, self)
        self.profile = profile
        self.persons_tuple: Optional[tuple[str, list[Person]]] = None
        self.ret_point = "my_persons_groups"

        box_layout1 = MDBoxLayout()
        box_layout1.orientation = "vertical"

        self.top_bar = MDTopAppBar()
        self.top_bar.title = ""
        self.top_bar.elevation = 2
        self.top_bar.left_action_items = [
            ["menu", lambda x: nav_drawer.set_state("open")]
        ]
        self.top_bar.right_action_items = [
            ["content-paste", lambda _: self.paste_person()],
            ["plus-circle-outline", lambda _: self.add_new_person()],
            ["plus", lambda _: self.add_sample_person()],
        ]

        scroll_view = MDScrollView()
        self.list = MDList()
        scroll_view.add_widget(self.list)
        box_layout1.add_widget(self.top_bar)
        box_layout1.add_widget(scroll_view)
        self.add_widget(box_layout1)

    @property
    def persons(self) -> list[Person]:
        if self.persons_tuple is None:
            return []
        return self.persons_tuple[1]

    def _update_persons(self, persons_tuple: tuple[str, list[Person]]) -> None:
        if self.persons_tuple in self.profile.persons:
            self.ret_point = "my_persons_groups"
        elif self.persons_tuple in self.profile.sample_persons:
            self.ret_point = "sample_persons_groups"
        self.top_bar.title = persons_tuple[0]
        self.list.clear_widgets()
        for person in persons_tuple[1]:
            self.list.add_widget(PersonElement(person=person, persons_screen=self))
        pass

    def change_persons(self, persons_tuple: tuple[str, list[Person]]) -> None:
        if self.persons_tuple != persons_tuple:
            self.persons_tuple = persons_tuple
            self._update_persons(persons_tuple)

    def paste_person(self) -> None:
        if PersonsListScreen.buffer is None:
            return
        new_person = copy.deepcopy(PersonsListScreen.buffer)
        self.persons.append(new_person)
        self.list.add_widget(PersonElement(person=new_person, persons_screen=self))
        pass

    def add_new_person(self) -> None:
        new_person = Person(properties=[])
        self.persons.append(new_person)
        self.list.add_widget(PersonElement(person=new_person, persons_screen=self))

    def add_sample_person(self) -> None:
        if len(self.profile.sample_persons) == 0:
            return
        # todo create sample chooser
        pass

    def get_element_of_person(self, person: Person) -> PersonElement:
        for list_element in self.list.children[:]:
            if type(list_element) is PersonElement:
                pge: PersonElement = list_element
                if pge.person == person:
                    list_element_of_group = pge
        return list_element_of_group

    def move_up_person(self, person: Person) -> None:
        index = self.persons.index(person)
        if index == 0 or len(self.persons) < 2:
            return
        element_this = self.get_element_of_person(person)
        swap_index = index - 1
        swap = self.persons[swap_index]
        element_swap = self.get_element_of_person(swap)
        element_this.update(swap)
        element_swap.update(person)
        self.persons.pop(index)
        self.persons.insert(index, swap)
        self.persons.pop(swap_index)
        self.persons.insert(swap_index, person)

    def move_down_person(self, person: Person) -> None:
        index = self.persons.index(person)
        if index == len(self.persons) - 1 or len(self.persons) < 2:
            return
        element_this = self.get_element_of_person(person)
        swap_index = index + 1
        swap = self.persons[swap_index]
        element_swap = self.get_element_of_person(swap)
        element_this.update(swap)
        element_swap.update(person)
        self.persons.pop(index)
        self.persons.insert(index, swap)
        self.persons.pop(swap_index)
        self.persons.insert(swap_index, person)

    def copy_person(self, person: Person) -> None:
        PersonsListScreen.buffer = copy.deepcopy(person)

    def cut_person(self, person: Person) -> None:
        PersonsListScreen.buffer = copy.deepcopy(person)
        element_this = self.get_element_of_person(person)
        self.persons.remove(person)
        self.list.remove_widget(element_this)

    def remove_person(self, person: Person) -> None:
        element_this = self.get_element_of_person(person)
        self.persons.remove(person)
        self.list.remove_widget(element_this)

    def on_enter(self, *args: Any) -> None:
        Window.bind(on_keyboard=self.keypress)

    def on_pre_leave(self, *args: Any) -> None:
        Window.unbind(on_keyboard=self.keypress)

    def keypress(self, window: Any, key: int, keycode: int, *largs: Any) -> None:
        if key == 27:
            self.main_screen.screen_manager.current = self.ret_point


# ———————————————————————————————————————————————————————————————————————————
# ————————————————————————— MyPersonsGroupsScreen —————————————————————————
# ———————————————————————————————————————————————————————————————————————————


class AddNewPersonGroupDialog(MDDialog):
    def __init__(self, person_screen: MyPersonsGroupsScreen, **kwargs: Any) -> None:
        super().__init__(
            title="Добавить группу",
            buttons=[
                MDFlatButton(
                    text="Добавить",
                    on_release=lambda x: self.add_new_group(),
                )
            ],
            **kwargs,
        )
        self.person_screen = person_screen

        self.textfield = MDTextField()
        self.textfield.padding = [25, 0, 25, 0]
        # self.spacing = "10dp"
        self.add_widget(self.textfield)

    def add_new_group(self) -> None:
        if not self.textfield.text.isspace():
            self.person_screen.add_new_group(self.textfield.text)
            self.textfield.text = ""
        self.dismiss()


class RenamePersonGroupDialog(MDDialog):
    def __init__(
        self,
        person_group: tuple[str, list[Person]],
        person_screen: MyPersonsGroupsScreen,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            title="Переименовать группу",
            buttons=[
                MDFlatButton(
                    text="Переименовать",
                    on_release=lambda x: self.rename_group(),
                )
            ],
            **kwargs,
        )
        self.person_screen = person_screen
        self.person_group = person_group

        self.textfield: MDTextField = MDTextField()
        self.textfield.padding = [25, 0, 25, 0]
        self.textfield.text = person_group[0]
        # self.spacing = "10dp"
        self.add_widget(self.textfield)

    def rename_group(self) -> None:
        if not self.textfield.text.isspace():
            self.person_screen.rename_person_group(
                self.person_group, self.textfield.text
            )
            self.textfield.text = ""
        self.dismiss()


class EditPersounGroupDialog(MDDialog):
    def __init__(
        self,
        person_group: Optional[tuple[str, list[Person]]],
        person_screen: MyPersonsGroupsScreen,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            title="Редактировать группу",
            type="simple",
            items=[
                DialogOneLineIconItem(
                    text="Переименовать группу",
                    icon="rename-box",
                    on_release=lambda x: self.rename_person_group(),
                ),
                DialogOneLineIconItem(
                    text="Переместить выше",
                    icon="arrow-collapse-up",
                    on_release=lambda x: self.move_up_person_group(),
                ),
                DialogOneLineIconItem(
                    text="Переместить ниже",
                    icon="arrow-collapse-down",
                    on_release=lambda x: self.move_down_person_group(),
                ),
                DialogOneLineIconItem(
                    text="Удалить группу персонажей",
                    icon="delete",
                    on_release=lambda x: self.remove_person_group(),
                ),
            ],
            **kwargs,
        )
        self.person_group = person_group
        self.person_screen = person_screen

    def update_group(
        self, person_group: tuple[str, list[Person]]
    ) -> EditPersounGroupDialog:
        self.person_group = person_group
        return self

    def rename_person_group(self) -> None:
        if self.person_group is None:
            return
        rename_person_group = RenamePersonGroupDialog(
            self.person_group, self.person_screen
        )
        rename_person_group.open()
        self.dismiss()

    def move_up_person_group(self) -> None:
        if self.person_group is None:
            return
        self.person_screen.move_up_person_group(self.person_group)

    def move_down_person_group(self) -> None:
        if self.person_group is None:
            return
        self.person_screen.move_down_person_group(self.person_group)

    def remove_person_group(self) -> None:
        if self.person_group is None:
            return
        self.person_screen.remove_person_group(self.person_group)
        self.dismiss()


class PersonGroupElement(TwoLineListItem, TouchBehavior):
    def __init__(
        self,
        person_group: Optional[tuple[str, list[Person]]],
        person_screen: MyPersonsGroupsScreen,
    ) -> None:
        super().__init__()
        self.person_group = person_group
        self.person_screen = person_screen
        self.update(self.person_group)

    @staticmethod
    def get_sec_text(persons: list[Person]) -> str:
        if len(persons) == 0:
            return "В этой группе пока нет персонажей"
        ret: str = " ".join(
            str(
                person.properties[0][1][0].value
                if len(person.properties) > 0 and len(person.properties[0][1]) > 0
                else ""
            )
            for person in persons[:3]
        )
        if len(persons) > 3:
            ret += " и другие"
        return ret

    def update(self, person_group: Optional[tuple[str, list[Person]]]) -> None:
        if person_group is None:
            return
        self.person_group = person_group
        self.text = person_group[0] + f" ({len(person_group[1])})"
        self.secondary_text = PersonGroupElement.get_sec_text(person_group[1])

    def on_release(self) -> None:
        if self.person_group is None:
            return
        self.person_screen.release_person_group(self.person_group)

    def on_long_touch(self, touch: Any, *args: Any) -> None:
        if self.person_group is None:
            return
        self.person_screen.edit_persoun_group_dialog.update_group(
            self.person_group
        ).open()


class MyPersonsGroupsScreen(MDScreen):
    def __init__(
        self,
        main_screen: MainScreen,
        nav_drawer: MDNavigationDrawer,
        profile: XNWPProfile,
        is_sample: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = "sample_persons_groups" if is_sample else "my_persons_groups"
        self.nav_drawer: MDNavigationDrawer = nav_drawer
        self.add_new_group_dialog = AddNewPersonGroupDialog(self)
        self.edit_persoun_group_dialog = EditPersounGroupDialog(None, self)
        self.main_screen = main_screen
        box_layout1 = MDBoxLayout()
        box_layout1.orientation = "vertical"

        top_bar = MDTopAppBar()
        top_bar.title = "Мои шаблоны" if is_sample else "Мои персонажи"
        top_bar.elevation = 2
        top_bar.left_action_items = [["menu", lambda x: nav_drawer.set_state("open")]]
        top_bar.right_action_items = [
            ["plus", lambda x: self.add_new_group_dialog.open()]
        ]

        scroll_view = MDScrollView()
        self.list = MDList()
        scroll_view.add_widget(self.list)
        self.profile: XNWPProfile = profile
        self.change_profile(profile)

        box_layout1.add_widget(top_bar)
        box_layout1.add_widget(scroll_view)
        self.add_widget(box_layout1)

    @property
    def persons(self) -> list[tuple[str, list[Person]]]:
        return self.get_persons(self.profile)

    def get_persons(self, profile: XNWPProfile) -> list[tuple[str, list[Person]]]:
        return profile.persons

    def change_profile(self, profile: XNWPProfile) -> None:
        self.profile = profile
        self.list.clear_widgets()
        for group in self.get_persons(profile):
            self.list.add_widget(
                PersonGroupElement(person_group=group, person_screen=self)
            )

    def add_new_group(self, group_name: str) -> None:
        new_group: tuple[str, list[Person]] = (group_name, [])
        self.persons.append(new_group)
        self.list.add_widget(
            PersonGroupElement(person_group=new_group, person_screen=self)
        )
        self.main_screen.update_groups_count()

    def get_element_of_person_group(
        self, person_group: tuple[str, list[Person]]
    ) -> PersonGroupElement:
        for list_element in self.list.children[:]:
            if type(list_element) is PersonGroupElement:
                pge: PersonGroupElement = list_element
                if pge.person_group == person_group:
                    list_element_of_group = pge
        return list_element_of_group

    def release_person_group(self, person_group: tuple[str, list[Person]]) -> None:
        self.main_screen.person_list_screen.change_persons(person_group)
        self.main_screen.screen_manager.current = "persons_list"
        pass

    def rename_person_group(
        self, person_group: tuple[str, list[Person]], new_name: str
    ) -> None:
        index = self.persons.index(person_group)
        self.persons.remove(person_group)
        element = self.get_element_of_person_group(person_group)
        new_group = (new_name, person_group[1])
        self.persons.insert(index, new_group)
        element.update(new_group)
        pass

    def move_up_person_group(self, person_group: tuple[str, list[Person]]) -> None:
        index = self.persons.index(person_group)
        if index == 0 or len(self.persons) < 2:
            return
        element_this = self.get_element_of_person_group(person_group)
        swap_index = index - 1
        swap = self.persons[swap_index]
        element_swap = self.get_element_of_person_group(swap)
        element_this.update(swap)
        element_swap.update(person_group)
        self.persons.pop(index)
        self.persons.insert(index, swap)
        self.persons.pop(swap_index)
        self.persons.insert(swap_index, person_group)

    def move_down_person_group(self, person_group: tuple[str, list[Person]]) -> None:
        index = self.persons.index(person_group)
        if index == len(self.persons) - 1 or len(self.persons) < 2:
            return
        element_this = self.get_element_of_person_group(person_group)
        swap_index = index + 1
        swap = self.persons[swap_index]
        element_swap = self.get_element_of_person_group(swap)
        element_this.update(swap)
        element_swap.update(person_group)
        self.persons.pop(index)
        self.persons.insert(index, swap)
        self.persons.pop(swap_index)
        self.persons.insert(swap_index, person_group)

    def remove_person_group(self, person_group: tuple[str, list[Person]]) -> None:
        element_this = self.get_element_of_person_group(person_group)
        self.persons.remove(person_group)
        self.list.remove_widget(element_this)
        self.main_screen.update_groups_count()

    def on_enter(self, *args: Any) -> None:
        Window.bind(on_keyboard=self.keypress)

    def on_pre_leave(self, *args: Any) -> None:
        Window.unbind(on_keyboard=self.keypress)

    def keypress(self, window: Any, key: int, keycode: int, *largs: Any) -> None:
        if key == 27 and self.nav_drawer.status != "opened":
            Window.close()


# ———————————————————————————————————————————————————————————————————————————
# ————————————————————————— SamplePersonsGroupsScreen —————————————————————————
# ———————————————————————————————————————————————————————————————————————————


class SamplePersonsGroupsScreen(MyPersonsGroupsScreen):
    def __init__(
        self,
        main_screen: MainScreen,
        nav_drawer: MDNavigationDrawer,
        profile: XNWPProfile,
        is_sample: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(main_screen, nav_drawer, profile, is_sample, *args, **kwargs)

    def get_persons(self, profile: XNWPProfile) -> list[tuple[str, list[Person]]]:
        return profile.sample_persons


# ———————————————————————————————————————————————————————————————————————————
# ————————————————————————— MainScreen —————————————————————————
# ———————————————————————————————————————————————————————————————————————————


class DrawerClickableItem(MDNavigationDrawerItem):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class DrawerLabelItem(MDNavigationDrawerItem):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.focus_behavior = False
        self._no_ripple_effect = True


class MainScreen(MDScreen):
    def __init__(self, profile: XNWPProfile, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.name = "mainscreen"
        self.profile: XNWPProfile = profile

        self.screen_manager = MDScreenManager()
        self.screen_manager.id = "screen_manager"

        navigation_layout = MDNavigationLayout()
        navigation_layout.add_widget(self.screen_manager)
        self.add_widget(navigation_layout)

        navigation_drawer = MDNavigationDrawer()
        navigation_drawer.radius = (0, 16, 16, 0)

        nav_menu = MDNavigationDrawerMenu()

        nav_menu.add_widget(
            MDNavigationDrawerHeader(
                title="XNWP",
                text="eXtended Notes for Writers",
                spacing="4dp",
                padding=("12dp", 0, 0, "56dp"),
            )
        )

        def change_screen(screen_name: str) -> Callable[[Any], None]:
            def internal_change(x: Any) -> None:
                self.screen_manager.current = screen_name

            return internal_change

        nav_menu.add_widget(MDNavigationDrawerLabel(text="Основные"))
        self.my_persons_click = DrawerClickableItem(
            text="Мои персонажи",
            icon="account-multiple",
            right_text="12",
            on_release=change_screen("my_persons_groups"),
        )
        nav_menu.add_widget(self.my_persons_click)
        nav_menu.add_widget(MDNavigationDrawerDivider())
        nav_menu.add_widget(MDNavigationDrawerLabel(text="Окружение"))
        self.sample_persons_click = DrawerClickableItem(
            text="Мои шаблоны",
            icon="account-box-multiple",
            right_text="3",
            on_release=change_screen("sample_persons_groups"),
        )
        nav_menu.add_widget(self.sample_persons_click)
        nav_menu.add_widget(MDNavigationDrawerDivider())
        nav_menu.add_widget(DrawerLabelItem(icon="information-outline", text="1.0.0"))

        navigation_drawer.add_widget(nav_menu)
        self.add_widget(navigation_drawer)

        self.screen_manager.add_widget(
            MyPersonsGroupsScreen(self, nav_drawer=navigation_drawer, profile=profile)
        )

        self.screen_manager.add_widget(
            SamplePersonsGroupsScreen(
                self, nav_drawer=navigation_drawer, profile=profile
            )
        )

        self.person_list_screen = PersonsListScreen(
            self, nav_drawer=navigation_drawer, profile=profile
        )

        self.screen_manager.add_widget(self.person_list_screen)

        self.update_groups_count()

    def update_groups_count(self) -> None:
        self.my_persons_click.right_text = str(len(self.profile.persons))
        self.sample_persons_click.right_text = str(len(self.profile.sample_persons))

    def change_profile(self, new_profile: XNWPProfile) -> None:
        # todo
        pass

    # def on_enter(self, *args: Any) -> None:
    #     Window.bind(on_keyboard=self.keypress)

    # def on_pre_leave(self, *args: Any) -> None:
    #     Window.unbind(on_keyboard=self.keypress)

    # def keypress(self, window: Any, key: int, keycode: int, *largs: Any) -> None:
    #     if key == 27:
    #         Window.close()
