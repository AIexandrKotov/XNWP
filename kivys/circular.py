from kivy.lang.builder import Builder
from kivy.uix.label import Label

from kivymd.app import MDApp

kv = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Мультигенератор"
            elevation: 2
            left_action_items: [["menu"]]
            right_action_items: [["plus", lambda x: app.up()], ["minus", lambda x: app.down()]]
        MDScrollView:
            MDList:
                padding: 10, 10, 10, 10
                spacing: 10
                cols: 1
                MDBoxLayout:
                    pos_hint: {"center_x": .5, "center_y": .5}
                    adaptive_size: True
                    MDGridLayout:
                        id: container
                        cols: 2
                        spacing: 25
                        adaptive_size: True
                        MDTextButton:
                            text: "Москва"
                        MDTextButton:
                            text: "Санкт-Петербург"
                        MDTextButton:
                            text: "Нижний Новгород"
                        MDTextButton:
                            text: "Новосибирск"
                        MDTextButton:
                            text: "Краснодар"
                        MDTextButton:
                            text: "Красноярск"
                        MDTextButton:
                            text: "Ростов-на-Дону"
                        MDTextButton:
                            text: "Сочи"
                        MDTextButton:
                            text: "Севастополь"
                        MDTextButton:
                            text: "Луганск"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                        MDTextButton:
                            text: "Донецк"
                MDRaisedButton:
                    text: "Сгенерировать новые значения"
                    font_size: 16
                    adaptive_height: True
                MDTextField:
                    mode: "rectangle"
                    hint_text: "База данных"
                    adaptive_height: True
                    text: "Русские города"
                MDRaisedButton:
                    text: "Изменить"
                    font_size: 16
                    adaptive_height: True
                MDGridLayout:
                    cols: 2
                    spacing: 10
                    adaptive_height: True
                    MDTextField:
                        mode: "rectangle"
                        hint_text: "Минимальная глубина"
                        text: "3"
                    MDTextField:
                        mode: "rectangle"
                        hint_text: "Максимальная глубина"
                        text: "7"
                MDTextField:
                    mode: "rectangle"
                    hint_text: "Только центральные"
                    adaptive_height: True
                    text: "True"
'''


class Main(MDApp):
    def up(self):
        if self.root.ids.container.cols >= 6:
            return
        self.root.ids.container.cols += 1
    def down(self):
        if self.root.ids.container.cols <= 1:
            return
        self.root.ids.container.cols -= 1
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Purple"
        return Builder.load_string(kv)

Main().run()