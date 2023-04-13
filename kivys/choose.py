import os

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd import images_path

KV = '''
<Content1>
    adaptive_height: True

    MDList:
        TwoLineListItem:
            text: "Евгений петросян"
            secondary_text: "Главный герой"



<Content2>
    adaptive_height: True

    MDList:
        TwoLineListItem:
            text: "Сергей Сергеев"
            secondary_text: "Не главный герой"


MDBoxLayout:
    orientation: "vertical"
    MDTopAppBar:
        title: "Выберите шаблон"
        elevation: 2
        left_action_items: [["menu"]]
    MDScrollView:
        MDGridLayout:
            padding: 25, 0, 25, 0
            id: box
            cols: 1
            adaptive_height: True
'''


class Content1(MDBoxLayout):
    '''Custom content.'''
class Content2(MDBoxLayout):
    '''Custom content.'''



class Test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Purple"
        return Builder.load_string(KV)

    def on_start(self):
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                content=Content1(),
                panel_cls=MDExpansionPanelOneLine(
                    text="Главные герои"
                )
            )
        )
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                content=Content2(),
                panel_cls=MDExpansionPanelOneLine(
                    text="Второстепенные персонажи"
                )
            )
        )


Test().run()