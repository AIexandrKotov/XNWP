from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.core.window import Window
from old_logic import *


#
#   NotesListScreen - экран списка идей (списка заметок)
#       NotesListScreenTopBar - верхняя полоска
#


class NotesListScreenTopBar(MDTopAppBar):
    def __init__(self, screen_manager, env: Environment, list_screen, list: MDList, **kwargs):
        super().__init__(**kwargs)
        self.title = "Список идей"
        self.screen_manager = screen_manager

        def add_new_note(x):
            note = Note()
            note.text = "Новая идея"
            list.add_widget(TwoLineListItem(text=note.text[:80],
                                            secondary_text='\\'.join(note.tags),
                                            on_release=list_screen.choose_command(len(env.current_profile.notes))))
            env.current_profile.notes.append(note)

        self.right_action_items = [["plus", add_new_note, "Новая идея"]]


class NotesList(MDBottomNavigationItem):
    def note_on_release(self, list_item: TwoLineListItem, note_index: int):
        self.notescreen = NoteEditorScreen(self.screen_manager, self.environment, self, list_item, self.environment.current_profile.notes[note_index])
        self.screen_manager.add_widget(self.notescreen)
        self.screen_manager.current = self.notescreen.name

    def choose_command(self, index: int):
        return lambda list_item: self.note_on_release(list_item, index)

    def update_list(self):
        self.list.clear_widgets()
        for ind, note in enumerate(self.environment.current_profile.notes):
            self.list.add_widget(TwoLineListItem(text=note.text[:80],
                                            secondary_text='\\'.join(note.tags),
                                            on_release=self.choose_command(ind)))

    def __init__(self, screen_manager, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment
        self.name = "Notes"
        self.text = "Идеи"
        self.icon = "lightbulb-variant-outline"
        self.screen_manager: MDScreenManager = screen_manager
        self.environment: Environment = environment

        box = MDBoxLayout()
        box.orientation = "vertical"
        self.list = list = MDList()
        box.add_widget(NotesListScreenTopBar(screen_manager, environment, self, self.list))
        scroll = MDScrollView()
        list.id = "container"
        self.update_list()
        scroll.add_widget(list)
        box.add_widget(scroll)
        self.add_widget(box)



#
#   NoteScreen - окно редактирования идеи (заметки)
#       NoteScreenTopBar - верхняя полоска с надписью "идея" и кнопкой выхода без сохранения изменений
#       NoteTagsField - список тегов этой идее, разделенных через \
#       NoteTextField - текст идеи
#


class NoteScreenTopBar(MDTopAppBar):
    def __init__(self, screen_manager, environment: Environment, list_screen, note_screen, note: Note, **kwargs):
        super().__init__(**kwargs)
        self.title = "Идея"
        self.environment = environment
        self.note = note
        self.screen_manager = screen_manager

        def exit_without_save(x):
            self.screen_manager.current = "mainscreen"
            self.screen_manager.remove_widget(note_screen)

        def delete(x):
            self.screen_manager.current = "mainscreen"
            self.screen_manager.remove_widget(note_screen)
            self.environment.current_profile.notes.remove(note)
            list_screen.update_list()

        self.right_action_items = [
            ["delete", delete, "Удалить идею"],
            ["content-save-off", exit_without_save, "Выйти без сохранения"],
        ]


class NoteTagsField(MDTextField):
    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.text = '\\'.join(note.tags)
        self.helper_text = "Введите теги, разделяя их знаком'\\'"


class NoteTextField(MDTextFieldRect):
    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.text = note.text
        self.mode = "fill"
        self.multiline = True


class NoteEditorScreen(MDScreen):
    def __init__(self, screen_manager: MDScreenManager, environment: Environment, list_screen, list_item: TwoLineListItem, note: Note, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_manager: MDScreenManager = screen_manager
        self.env: Environment = environment
        self.list_item = list_item
        self.note = note
        self.name = "note"
        box = MDBoxLayout()
        box.orientation = "vertical"
        sw = MDScrollView()
        box.add_widget(NoteScreenTopBar(screen_manager, environment, list_screen, self, note))
        self.text_field = NoteTextField(note)
        sw.add_widget(self.text_field)
        self.tags_field = NoteTagsField(note)
        box.add_widget(self.tags_field)
        box.add_widget(sw)
        self.add_widget(box)

    def on_enter(self, *args):
        Window.bind(on_keyboard = self.keypress)

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard = self.keypress)

    def keypress(self, window, key, keycode, *largs):
        if key == 27:
            self.note.text = self.text_field.text[:80]
            self.note.tags = self.tags_field.text.split('\\')
            self.list_item.text = self.note.text
            self.list_item.secondary_text = '\\'.join(self.note.tags)
            self.screen_manager.current = "mainscreen"
            self.screen_manager.remove_widget(self)
