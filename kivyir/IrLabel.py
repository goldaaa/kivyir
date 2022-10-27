from .ConfigBase import *
from kivy.uix.label import Label


class IrLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_size = self.size
        self.text_language = 'fa'
        self.valign = 'top'
        self.halign = 'right'
        self.line_height = 0.8

    def on_size(self, *args):
        self.text_size = self.size
        self.texture_update()
