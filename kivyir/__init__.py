__version__ = "1.0.0"
__programing__ = "navid nasiri --> github user (goldaaa)"


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

