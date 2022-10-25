import re
from copy import copy

from kivy.core import text
from kivy.core.text import Label
from kivy.parser import parse_color
from kivy.properties import dpi2px
from kivy.core.text.markup import MarkupLabel
from kivy.core.text.text_layout import LayoutWord, layout_text

from .FaCleaning.Cleaning import cleaning
from .FaCleaning.LanguageCheck import reverse_parse, find_text


def reverse_lang_other(text):
    return reverse_parse(text=text, search=lambda word: find_text(word, "[A-Z a-z 1-9 ۱-۹]")[0], reverse_text=True)


def label_base_render(self, real=False):
    '''Return a tuple (width, height) to create the image
    with the user constraints. (width, height) includes the padding.
    '''
    if real:
        return self._render_real()

    options = copy(self.options)
    options['space_width'] = self.get_extents(' ')[0]
    options['strip'] = strip = (options['strip'] or
                                options['halign'] == 'justify')
    uw, uh = options['text_size'] = self._text_size
    text = cleaning(self.text)

    if strip:
        text = text.strip()
    self.is_shortened = False
    if uw is not None and options['shorten']:
        text = self.shorten(text)

    self._cached_lines = lines = []
    if not text:
        return 0, 0

    if uh is not None and (options['valign'] == 'middle' or
                           options['valign'] == 'center'):
        center = -1  # pos of newline
        if len(text) > 1:
            middle = int(len(text) // 2)
            l, r = text.rfind('\n', 0, middle), text.find('\n', middle)
            if l != -1 and r != -1:
                center = l if center - l <= r - center else r
            elif l != -1:
                center = l
            elif r != -1:
                center = r

        # if a newline split text, render from center down and up til uh
        if center != -1:
            # layout from center down until half uh
            w, h, clipped = layout_text(text[center + 1:], lines, (0, 0),
                                        (uw, uh / 2), options, self.get_cached_extents(), True, True)

            # now layout from center upwards until uh is reached
            w, h, clipped = layout_text(text[:center + 1], lines, (w, h),
                                        (uw, uh), options, self.get_cached_extents(), False, True)
        else:  # if there's no new line, layout everything
            w, h, clipped = layout_text(text, lines, (0, 0), (uw, None),
                                        options, self.get_cached_extents(), True, True)
    else:  # top or bottom
        w, h, clipped = layout_text(text, lines, (0, 0), (uw, uh), options,
                                    self.get_cached_extents(), options['valign'] == 'top', True)

    self._internal_size = w, h
    if uw:
        w = uw
    if uh:
        h = uh
    if h > 1 and w < 2:
        w = 2
    return int(w), int(h)


def label_base_render_lines(self, lines, options, render_text, y, size):
    get_extents = self.get_cached_extents()
    uw, uh = options['text_size']
    xpad = options['padding_x']
    if uw is not None:
        uww = uw - 2 * xpad  # real width of just text
    w = size[0]
    sw = options['space_width']
    halign = options['halign']
    split = re.split
    find_base_dir = self.find_base_direction
    cur_base_dir = options['base_direction']

    for layout_line in lines:  # for plain label each line has only one str
        lw, lh = layout_line.w, layout_line.h
        line = ''
        assert len(layout_line.words) < 2
        if len(layout_line.words):
            last_word = layout_line.words[0]
            text_lang = options['text_language']
            if text_lang == 'fa' or text_lang == 'ar' or not text_lang:
                line = reverse_lang_other(text=last_word.text)
            else:
                line = last_word.text
            if not cur_base_dir:
                cur_base_dir = find_base_dir(line)

        x = xpad
        if halign == 'auto':
            if cur_base_dir and 'rtl' in cur_base_dir:
                x = max(0, int(w - lw - xpad))  # right-align RTL text
        elif halign == 'center':
            x = int((w - lw) / 2.)
        elif halign == 'right':
            x = max(0, int(w - lw - xpad))

        # right left justify
        # divide left over space between `spaces`
        # TODO implement a better method of stretching glyphs?
        if (uw is not None and halign == 'justify' and line and not
        layout_line.is_last_line):
            # number spaces needed to fill, and remainder
            n, rem = divmod(max(uww - lw, 0), sw)
            n = int(n)
            words = None
            if n or rem:
                # there's no trailing space when justify is selected
                words = split(re.compile('( +)'), line)
            if words is not None and len(words) > 1:
                space = type(line)(' ')
                # words: every even index is spaces, just add ltr n spaces
                for i in range(n):
                    idx = (2 * i + 1) % (len(words) - 1)
                    words[idx] = words[idx] + space
                if rem:
                    # render the last word at the edge, also add it to line
                    ext = get_extents(words[-1])
                    word = LayoutWord(last_word.options, ext[0], ext[1],
                                      words[-1])
                    layout_line.words.append(word)
                    last_word.lw = uww - ext[0]  # word was stretched
                    render_text(words[-1], x + last_word.lw, y)
                    last_word.text = line = ''.join(words[:-2])
                else:
                    last_word.lw = uww  # word was stretched
                    last_word.text = line = ''.join(words)

                layout_line.w = uww  # the line occupies full width

        if len(line):
            layout_line.x = x
            layout_line.y = y
            render_text(line, x, y)
        y += lh
    return y


def markup__pre_render(self):
    # self.resolve_font_name()
    # split markup, words, and lines
    # result: list of word with position and width/height
    # during the first pass, we don't care about h/valign
    self._cached_lines = lines = []
    self._refs = {}
    self._anchors = {}
    clipped = False
    w = h = 0
    uw, uh = self.text_size
    spush = self._push_style
    spop = self._pop_style
    options = self.options
    options['_ref'] = None
    options['_anchor'] = None
    options['script'] = 'normal'
    shorten = options['shorten']
    # if shorten, then don't split lines to fit uw, because it will be
    # flattened later when shortening and broken up lines if broken
    # mid-word will have space mid-word when lines are joined
    uw_temp = None if shorten else uw
    xpad = options['padding_x']
    uhh = (None if uh is not None and options['valign'] != 'top' or
           options['shorten'] else uh)
    options['strip'] = options['strip'] or options['halign'] == 'justify'
    find_base_dir = Label.find_base_direction
    base_dir = options['base_direction']
    self._resolved_base_dir = None
    for item in self.markup:
        if item == '[b]':
            spush('bold')
            options['bold'] = True
            self.resolve_font_name()
        elif item == '[/b]':
            spop('bold')
            self.resolve_font_name()
        elif item == '[i]':
            spush('italic')
            options['italic'] = True
            self.resolve_font_name()
        elif item == '[/i]':
            spop('italic')
            self.resolve_font_name()
        elif item == '[u]':
            spush('underline')
            options['underline'] = True
            self.resolve_font_name()
        elif item == '[/u]':
            spop('underline')
            self.resolve_font_name()
        elif item == '[s]':
            spush('strikethrough')
            options['strikethrough'] = True
            self.resolve_font_name()
        elif item == '[/s]':
            spop('strikethrough')
            self.resolve_font_name()
        elif item[:6] == '[size=':
            item = item[6:-1]
            try:
                if item[-2:] in ('px', 'pt', 'in', 'cm', 'mm', 'dp', 'sp'):
                    size = dpi2px(item[:-2], item[-2:])
                else:
                    size = int(item)
            except ValueError:
                raise
                size = options['font_size']
            spush('font_size')
            options['font_size'] = size
        elif item == '[/size]':
            spop('font_size')
        elif item[:7] == '[color=':
            color = parse_color(item[7:-1])
            spush('color')
            options['color'] = color
        elif item == '[/color]':
            spop('color')
        elif item[:6] == '[font=':
            fontname = item[6:-1]
            spush('font_name')
            options['font_name'] = fontname
            self.resolve_font_name()
        elif item == '[/font]':
            spop('font_name')
            self.resolve_font_name()
        elif item[:13] == '[font_family=':
            spush('font_family')
            options['font_family'] = item[13:-1]
        elif item == '[/font_family]':
            spop('font_family')
        elif item[:14] == '[font_context=':
            fctx = item[14:-1]
            if not fctx or fctx.lower() == 'none':
                fctx = None
            spush('font_context')
            options['font_context'] = fctx
        elif item == '[/font_context]':
            spop('font_context')
        elif item[:15] == '[font_features=':
            spush('font_features')
            options['font_features'] = item[15:-1]
        elif item == '[/font_features]':
            spop('font_features')
        elif item[:15] == '[text_language=':
            lang = item[15:-1]
            if not lang or lang.lower() == 'none':
                lang = None
            spush('text_language')
            options['text_language'] = lang
        elif item == '[/text_language]':
            spop('text_language')
        elif item[:5] == '[sub]':
            spush('font_size')
            spush('script')
            options['font_size'] = options['font_size'] * .5
            options['script'] = 'subscript'
        elif item == '[/sub]':
            spop('font_size')
            spop('script')
        elif item[:5] == '[sup]':
            spush('font_size')
            spush('script')
            options['font_size'] = options['font_size'] * .5
            options['script'] = 'superscript'
        elif item == '[/sup]':
            spop('font_size')
            spop('script')
        elif item[:5] == '[ref=':
            ref = item[5:-1]
            spush('_ref')
            options['_ref'] = ref
        elif item == '[/ref]':
            spop('_ref')
        elif not clipped and item[:8] == '[anchor=':
            options['_anchor'] = item[8:-1]
        elif not clipped:
            item = item.replace('&bl;', '[').replace(
                '&br;', ']').replace('&amp;', '&')
            if len(item) > 1:
                item = cleaning(item)
                if self.options['font_name'] == 'Roboto':
                    options['font_name'] = font_name
                    self.resolve_font_name()
            if not base_dir:
                base_dir = self._resolved_base_dir = find_base_dir(item)
            opts = copy(options)
            extents = self.get_cached_extents()
            opts['space_width'] = extents(' ')[0]
            w, h, clipped = layout_text(
                item, lines, (w, h), (uw_temp, uhh),
                opts, extents,
                append_down=True,
                complete=False
            )

    if len(lines):  # remove any trailing spaces from the last line
        old_opts = self.options
        self.options = copy(opts)
        w, h, clipped = layout_text(
            '', lines, (w, h), (uw_temp, uhh),
            self.options, self.get_cached_extents(),
            append_down=True,
            complete=True
        )
        self.options = old_opts

    self.is_shortened = False
    if shorten:
        options['_ref'] = None  # no refs for you!
        options['_anchor'] = None
        w, h, lines = self.shorten_post(lines, w, h)
        self._cached_lines = lines
    # when valign is not top, for markup we layout everything (text_size[1]
    # is temporarily set to None) and after layout cut to size if too tall
    elif uh != uhh and h > uh and len(lines) > 1:
        if options['valign'] == 'bottom':
            i = 0
            while i < len(lines) - 1 and h > uh:
                h -= lines[i].h
                i += 1
            del lines[:i]
        else:  # middle
            i = 0
            top = int(h / 2. + uh / 2.)  # remove extra top portion
            while i < len(lines) - 1 and h > top:
                h -= lines[i].h
                i += 1
            del lines[:i]
            i = len(lines) - 1  # remove remaining bottom portion
            while i and h > uh:
                h -= lines[i].h
                i -= 1
            del lines[i + 1:]

    # now justify the text
    if options['halign'] == 'justify' and uw is not None:
        # XXX: update refs to justified pos
        # when justify, each line should've been stripped already
        split = partial(re.split, re.compile('( +)'))
        uww = uw - 2 * xpad
        chr = type(self.text)
        space = chr(' ')
        empty = chr('')

        for i in range(len(lines)):
            line = lines[i]
            words = line.words
            # if there's nothing to justify, we're done
            if (not line.w or int(uww - line.w) <= 0 or not len(words) or
                    line.is_last_line):
                continue

            done = False
            parts = [None, ] * len(words)  # contains words split by space
            idxs = [None, ] * len(words)  # indices of the space in parts
            # break each word into spaces and add spaces until it's full
            # do first round of split in case we don't need to split all
            for w in range(len(words)):
                word = words[w]
                sw = word.options['space_width']
                p = parts[w] = split(word.text)
                idxs[w] = [v for v in range(len(p)) if
                           p[v].startswith(' ')]
                # now we have the indices of the spaces in split list
                for k in idxs[w]:
                    # try to add single space at each space
                    if line.w + sw > uww:
                        done = True
                        break
                    line.w += sw
                    word.lw += sw
                    p[k] += space
                if done:
                    break

            # there's not a single space in the line?
            if not any(idxs):
                continue

            # now keep adding spaces to already split words until done
            while not done:
                for w in range(len(words)):
                    if not idxs[w]:
                        continue
                    word = words[w]
                    sw = word.options['space_width']
                    p = parts[w]
                    for k in idxs[w]:
                        # try to add single space at each space
                        if line.w + sw > uww:
                            done = True
                            break
                        line.w += sw
                        word.lw += sw
                        p[k] += space
                    if done:
                        break

            # if not completely full, push last words to right edge
            diff = int(uww - line.w)
            if diff > 0:
                # find the last word that had a space
                for w in range(len(words) - 1, -1, -1):
                    if not idxs[w]:
                        continue
                    break
                old_opts = self.options
                self.options = word.options
                word = words[w]
                # split that word into left/right and push right till uww
                l_text = empty.join(parts[w][:idxs[w][-1]])
                r_text = empty.join(parts[w][idxs[w][-1]:])
                left = LayoutWord(
                    word.options,
                    self.get_extents(l_text)[0],
                    word.lh,
                    l_text
                )
                right = LayoutWord(
                    word.options,
                    self.get_extents(r_text)[0],
                    word.lh,
                    r_text
                )
                left.lw = max(left.lw, word.lw + diff - right.lw)
                self.options = old_opts

                # now put words back together with right/left inserted
                for k in range(len(words)):
                    if idxs[k]:
                        words[k].text = empty.join(parts[k])
                words[w] = right
                words.insert(w, left)
            else:
                for k in range(len(words)):
                    if idxs[k]:
                        words[k].text = empty.join(parts[k])
            line.w = uww
            w = max(w, uww)

    self._internal_size = w, h
    if uw:
        w = uw
    if uh:
        h = uh
    if h > 1 and w < 2:
        w = 2
    if w < 1:
        w = 1
    if h < 1:
        h = 1
    return int(w), int(h)


def markup_render_lines(self, lines, options, render_text, y, size):
    xpad = options['padding_x']
    w = size[0]
    halign = options['halign']
    refs = self._refs
    anchors = self._anchors
    base_dir = options['base_direction'] or self._resolved_base_dir
    auto_halign_r = halign == 'auto' and base_dir and 'rtl' in base_dir

    for layout_line in lines:  # for plain label each line has only one str
        lw, lh = layout_line.w, layout_line.h
        x = xpad
        if halign == 'center':
            x = int((w - lw) / 2.)
        elif halign == 'right' or auto_halign_r:
            x = max(0, int(w - lw - xpad))
        layout_line.x = x
        layout_line.y = y
        psp = pph = 0
        for word in layout_line.words:
            options = self.options = word.options
            # the word height is not scaled by line_height, only lh was
            wh = options['line_height'] * word.lh
            # calculate sub/super script pos
            if options['script'] == 'superscript':
                script_pos = max(0, psp if psp else self.get_descent())
                psp = script_pos
                pph = wh
            elif options['script'] == 'subscript':
                script_pos = min(lh - wh, ((psp + pph) - wh)
                if pph else (lh - wh))
                pph = wh
                psp = script_pos
            else:
                script_pos = (lh - wh) / 1.25
                psp = pph = 0
            if len(word.text):
                text_lang = options['text_language']
                if text_lang == 'fa' or text_lang == 'ar' or not text_lang:
                    word.text = reverse_lang_other(text=word.text)
                render_text(word.text, x, y + script_pos)

                # should we record refs ?
                ref = options['_ref']
                if ref is not None:
                    if ref not in refs:
                        refs[ref] = []
                    refs[ref].append((x, y, x + word.lw, y + wh))

                # Should we record anchors?
                anchor = options['_anchor']
                if anchor is not None:
                    if anchor not in anchors:
                        anchors[anchor] = (x, y)
                x += word.lw
            y += lh
        return y


base_direction = 'rtl'
font_name = 'Sahel'
file_regular, file_bold, file_italic, file_bolditalic = \
    'kivyir/font/Sahel.ttf', 'kivyir/font/Sahel-Bold.ttf', None, None

text.LabelBase.find_base_direction = lambda *x: base_direction
text.LabelBase.render = label_base_render
text.LabelBase.render_lines = label_base_render_lines
MarkupLabel._pre_render = markup__pre_render
MarkupLabel.render_lines = markup_render_lines

set_fonts = file_regular, file_bold, file_italic, file_bolditalic
text._default_font_paths = set_fonts
text.DEFAULT_FONT = font_name
text.LabelBase.register(font_name, *set_fonts)
