from .ConfigBase import *
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.utils import boundary


def get_cursor_from_xy(self, x, y):
    padding_left, padding_top, padding_right, padding_bottom = self.padding

    lines = self._lines
    dy = self.line_height + self.line_spacing
    cursor_x = x - self.x
    scroll_y = self.scroll_y
    scroll_x = self.scroll_x
    scroll_y = scroll_y / dy if scroll_y > 0 else 0

    cursor_y = (self.top - padding_top + scroll_y * dy) - y

    cursor_y = int(boundary(
        round(cursor_y / dy - 0.5),
        0,
        len(lines) - 1
    ))

    get_text_width = self._get_text_width
    tab_width = self.tab_width
    label_cached = self._label_cached

    # Offset for horizontal text alignment
    xoff = 0
    halign = self.halign
    base_dir = self.base_direction or self._resolved_base_dir
    auto_halign_r = halign == 'auto' and base_dir and 'rtl' in base_dir

    if halign == 'center':
        viewport_width = self.width - padding_left - padding_right
        xoff = max(
            0, int((viewport_width - self._get_row_width(cursor_y)) / 2)
        )

    elif halign == 'right' or auto_halign_r:
        viewport_width = self.width - padding_left - padding_right
        xoff = max(
            0, int(viewport_width - self._get_row_width(cursor_y))
        )

    for i in range(0, len(lines[cursor_y])):
        line_y = lines[cursor_y][::-1]

        if cursor_x + scroll_x < (
            xoff
            + get_text_width(line_y[:i], tab_width, label_cached)
            + get_text_width(line_y[i], tab_width, label_cached) * 0.6
            + padding_left
        ):
            cursor_x = (len(line_y)-1) - i
            break

    return int(cursor_x), int(cursor_y)


def cursor_offset(self):
    '''Get the cursor x offset on the current line.
    '''
    offset = 0
    row = int(self.cursor_row)
    col = int(self.cursor_col)
    lines = self._lines
    if col and row < len(lines):
        col = len(lines[row]) - col
        offset = self._get_text_width(
            lines[row][::-1][:col],
            self.tab_width,
            self._label_cached
        )
    return offset


def _draw_selection(self, pos, size, line_num, selection_start, selection_end,
                    lines, get_text_width, tab_width, label_cached, width_minus_padding,
                    padding_left, padding_right, x, canvas_add, selection_color):
    selection_start_col, selection_start_row = selection_start
    selection_end_col, selection_end_row = selection_end

    # Draw the current selection on the widget.
    if not selection_start_row <= line_num <= selection_end_row: return
    x, y = pos
    w, h = size
    beg = x
    end = x + w

    if line_num == selection_start_row:
        line = lines[line_num]
        beg -= self.scroll_x
        beg += get_text_width(
            line[:len(line) - selection_start_col],
            tab_width,
            label_cached
        )

    if line_num == selection_end_row:
        line = lines[line_num]
        end = (x - self.scroll_x) + get_text_width(
            line[:len(line) - selection_end_col],
            tab_width,
            label_cached
        )

    beg = boundary(beg, x, x + width_minus_padding)
    end = boundary(end, x, x + width_minus_padding)
    if beg == end: return

    canvas_add(Color(*selection_color, group='selection'))
    canvas_add(
        Rectangle(
            pos=(end, y),
            size=(beg - end, h),
            group='selection'
        )
    )


dict_def = ['get_cursor_from_xy', 'cursor_offset', '_draw_selection']
for df in dict_def: exec("%s = %s" % (f"TextInput.{df}", df))


class IrTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.text: self.text = cleaning(self.text)
        self.text_language = "fa"
