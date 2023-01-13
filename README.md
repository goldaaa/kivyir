# kivy persian

The first kivy Persian users.

I converted the kivy library into Farsi for Iranians so that Iranians can use it.

I have added a sample test file so you can understand how to use it.

Download
--------
You can install this from pypi.

    pip install kivyir
    
You can also install from this repository.

    git clone https://github.com/goldaaa/kivyir.git

Then, install the library with

    python setup.py install


Importing
---------

Import kivyir commands, menus, and the shell

    from kivyir import *        # Line 1 should always be placed


Commands
--------

Commands that can be used
    
Some changes if needed

    from kivyir import *
    config = Config()
    config.change(
        direction='ltr',
        font_name='Sahel',
        file_regular='{path}.ttf',
        file_bold='{path}.ttf',
        file_italic='{path}.ttf',
        file_bolditalic='{path}.ttf'
    )

Custom made

    from kivyir import IrLabel, IrTextInput

[Sample image tested](https://github.com/goldaaa/kivyir/blob/main/test/sampel_test.png)

![](https://github.com/goldaaa/kivyir/blob/main/test/sampel_test.png)


Install the required package
--------
    kivy
    facleaning



If you are interested in financial support, you can send a message through Gmail if you have any questions.

gmail: goldaaa.program@gmail.com

[github kivy persian](https://github.com/goldaaa/kivyir)

If you Arab speaking friends need to use it, let me know so that I can apply it for you too.
