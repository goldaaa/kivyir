# kivyir | kivy persian | kivy فارسی

The first kivy Persian users for Iranians.

I converted the kivy library into Farsi for Iranians so that Iranians can use it.

کتابخانه کیوی را برای ایرانیان به فارسی تبدیل کردم تا ایرانی ها بتوانند از آن استفاده کنند.

I have added a sample test file so you can understand how to use it.

یک نمونه فایل تست اضافه کردم تا بتوانید نحوه استفاده از آن را بدانید.


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
    kivy>=2.0.0
    facleaning



If you are interested in financial support, you can send a message through Gmail if you have any questions.

اگر قصد حمایت مالی یا سوال دارید می توانید از طریق جیمیل پیام ارسال کنید.

gmail: goldaaa.program@gmail.com

[Telegram group of this project: t.me/kivyiran](http://t.me/kivyiran)

[github facleaning](https://github.com/goldaaa/kivyir)
