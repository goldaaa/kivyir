from .Data import Arabic, Persian, CharacterReverse


def cleaning(text, lang='fa', reverse_text=False, reverse_other_char=True):
    if not text: return ''
    if lang == 'fa':
        letters = Persian
    elif lang == 'ar':
        letters = Arabic
    else:
        letters = Persian

    result = ''
    old_word = [0, '']
    for letter in text:
        if not letter in letters:
            if reverse_other_char:
                character = CharacterReverse.get(letter)
                result += character if character else letter
            else:
                result += letter
            old_word[0] = -1

        elif not result:
            result += letters[letter][0]
            old_word[0] = 0

        else:
            num, o_text = old_word
            old_letter = letters.get(o_text)
            if not old_letter: old_letter = ('', '', '', '')

            now_letter = letters[letter]

            if num == -1:
                result += now_letter[0]
                old_word[0] = 0
                pass

            elif not now_letter[3] or not old_letter[1]:
                result += now_letter[0]
                old_word[0] = 0

            elif num == 3 and not old_letter[1]:
                result += now_letter[1]
                old_word[0] = 0

            elif num == 0:
                result = result[:-1] + old_letter[1]
                result += now_letter[3]
                old_word[0] = 3

            else:
                result = result[:-1] + old_letter[2]
                result += now_letter[3]
                old_word[0] = 3

        old_word[1] = letter
    if reverse_text: result = result[::-1]
    return result
