from kivyir import *           # باید همیشه خط اول قرار بگیرد
from kivyir import IrLabel, IrTextInput
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

Builder.load_string("""
<Home>:
    orientation: 'vertical'
    
    IrLabel:
        text: 'این یک متن برای تست می باشد, این دو متن برای تست می باشد, این سه متن برای تست می باشد.'
        height: 200
        valign: 'center'
        halign: 'right'

    IrTextInput:
        font_size: 20
        size_hint_y: None
        height: 200
        base_direction: 'rtl'
        text: 'این یک متن برای تست می باشد, این دو متن برای تست می باشد, این سه متن برای تست می باشد.'

        use_handles: True
        foreground_color: (0,0,1,1)
""")


class Home(BoxLayout):
    pass


class MyLabelApp(App):
    def build(self):
        self.root = Factory.Home()
        return super().build()


label = MyLabelApp()
label.run()
