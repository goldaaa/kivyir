__version__ = "1.0.0"
__programer__ = "navid nasiri"
__github__ = "https://github.com/goldaaa"
__gmail__ = "goldaaa.program@gmail.com"

from .ConfigText import *
from .ConfigInput import *

from .FaCleaning import *

from .IrTextInput import *
from .IrLabel import *


from kivy import *
try:
    from kivymd import *
except ImportError:
    pass

