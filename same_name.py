def same_name(lst):
    dic = {}
    new_list = []
    for i in range(len(lst)):
        cur = lst[i]
        if '.' in cur:
            ind = cur.rindex('.')
            cur1 = [cur[:ind], cur[ind + 1:]]
        else:
            cur1 = [cur, '']
        try:
            new_list.append(cur1[0] + f'({dic[cur]})' + ('.' if '.' in cur else '') + cur1[1])
            dic[cur] += 1
        except KeyError:
            dic[cur] = 1
            new_list.append(cur)
    return new_list


if __name__ == '__main__':
    # print(same_name(['123.docx', 'lol.xlsx']))
    # print(same_name(['123.docx', '123.docx']))
    print(same_name(['12.34.docx', '12.34.docx']))




