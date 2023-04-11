from __future__ import annotations

from typing import Any, Callable, Optional

from kivy.core.window import Window
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IconLeftWidget, MDList, OneLineIconListItem, TwoLineListItem
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
# ————————————————————————— PersonEditorScreen —————————————————————————
# ———————————————————————————————————————————————————————————————————————————


class MyPersonsListScreen(MDScreen):
    def __init__(
        self,
        main_screen: MainScreen,
        nav_drawer: MDNavigationDrawer,
        profile: XNWPProfile,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = "my_persons_list"
        self.main_screen: MainScreen = main_screen
        self.nav_drawer = nav_drawer
        self.profile = profile
        self.persons: Optional[list[Person]] = None

    def change_persons(self, persons: list[Person]) -> None:
        self.persons = persons

    def on_enter(self, *args: Any) -> None:
        Window.bind(on_keyboard=self.keypress)

    def on_pre_leave(self, *args: Any) -> None:
        Window.unbind(on_keyboard=self.keypress)

    def keypress(self, window: Any, key: int, keycode: int, *largs: Any) -> None:
        if key == 27:
            self.main_screen.screen_manager.current = "my_persons_groups"


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
            str(person.properties[0][1][0].value) for person in persons[:3]
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
        # todo open person editor
        pass

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

        self.screen_manager.add_widget(
            MyPersonsListScreen(self, nav_drawer=navigation_drawer, profile=profile)
        )

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
