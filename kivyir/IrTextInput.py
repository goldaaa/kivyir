from .ConfigInput import *
from kivy.uix.textinput import TextInput


class IrTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.text: self.text = cleaning(self.text)
        self.text_language = "fa"
        self.text_size = self.size
