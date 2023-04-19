from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class MainApp(App):
    def build(self):
        self.button = Button(text="Click", on_release=self.get_caption)
        return self.button

    def get_caption(self, btn):
        Popup(
            title="Enter text here",
            content=TextInput(focus=True),
            size_hint=(0.6, 0.6),
            on_dismiss=self.set_caption,
        ).open()

    def set_caption(self, popup):
        self.button.text = popup.content.text


MainApp().run()
