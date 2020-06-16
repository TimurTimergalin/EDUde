from string import ascii_letters, digits, punctuation


def kir_to_lat(string):
    lets = ascii_letters + digits + punctuation
    dic = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'yo',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'х',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sh',
        'ъ': '\'',
        'ы': 'y',
        'ь': '\'',
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
        ' ': ' '
    }
    new_str = ''
    for i in string:
        if i not in lets:
            if i in dic:
                new_str += dic[i]
            elif i in punctuation:
                new_str += i
            else:
                new_str += '\''
        else:
            new_str += i
    return new_str


if __name__ == '__main__':
    print(kir_to_lat('12345wertydfgbn.lmq'))
    print(kir_to_lat('домашняя работа.docx'))
    print(kir_to_lat('ььььььььььььььь.docxxx'))





