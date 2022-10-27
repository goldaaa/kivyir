from kivyir import *
from kivy.app import App
from kivy.lang import Builder


kv = Builder.load_string("""
BoxLayout:
    orientation: 'vertical'

    IrLabel:
        text: 'این یک متن برای تست می باشد, این دو متن برای تست می باشد, این سه متن برای تست می باشد.'
        height: 200
        valign: 'center'
        halign: 'right'

    IrTextInput:
        base_direction: 'rtl'
        text: 'این یک متن برای تست می باشد, این دو متن برای تست می باشد, این سه متن برای تست می باشد.'

        use_handles: True
        cursor_color: (1, 0, 0, 1)
        cursor_width: '2sp'
        foreground_color: (0, 0, 0, 1)
        background_color: (1, 1, 1, 1)
""")


class MyLabelApp(App):
    def build(self):
        return kv


label = MyLabelApp()
label.run()
