from sre_compile import compile


def find_text(word, p, flags=0):
    word = compile(p, flags).findall(word)
    filter_items = list(filter(lambda x: x is not '', word))
    if len(word)/1.5 <= len(filter_items) != 0:
        empty = True
    else:
        empty = False
    return empty, filter_items, word


def en(word):
    return find_text(word, "[A-Z a-z 1-9]")[0]


def fa(word):
    return find_text(word, "[ا-ی ۱-۹]")[0]


def reverse_parse(text, search='fa', reverse_text=True):
    if search == 'en':
        search = en
    elif search == 'fa':
        search = fa
    else:
        search = search
    if reverse_text: text = text[::-1]
    text = text.split(' ')
    for i, word in enumerate(text):
        if search(word):
            text[i] = text[i][::-1]
    return ' '.join(text)


if __name__ == '__main__':
    text = 'این متن توسط navid برای تست نوشته شده است'
    reverse_fa = reverse_parse(text, search='fa')
    print(reverse_fa)
    reverse_fa = reverse_parse(text, search='en')
    print(reverse_fa)


