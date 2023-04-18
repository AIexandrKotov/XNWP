from kivy.lang import Builder

from kivymd.app import MDApp


KV = '''
MDScreen:
    MDScrollView:
        MDList:
            MDBoxLayout:
                adaptive_height: True
                MDCheckbox:
                    size_hint: None, None
                    size: "48dp", "48dp"
                    pos_hint: { "center_x": 0, "center_y": 0.5 }
                MDLabel:
                    text: "Запретить!"
                    font_size: 20
                    pos_hint: { "center_x": 0, "center_y": 0.5 }
            MDBoxLayout:
                adaptive_height: True
                MDCheckbox:
                    id: checkbox
                    size_hint: None, None
                    size: "48dp", "48dp"
                    pos_hint: { "center_x": 0, "center_y": 0.5 }
                MDLabel:
                    text: "Что запретить-то?"
                    font_size: 20
                    pos_hint: { "center_x": 0, "center_y": 0.5 }
            MDBoxLayout:
                adaptive_height: True
                MDCheckbox:
                    size_hint: None, None
                    size: "48dp", "48dp"
                    pos_hint: { "center_x": 0, "center_y": 0.5 }
                MDLabel:
                    text: "Извините пожалуйста"
                    font_size: 20
                    pos_hint: { "center_x": 0, "center_y": 0.5 }
    
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()