def duplicate_handler(duplicates_list, input_row):
    # List to handle duplicates in Book 1 where 'blockquote' is a parent to 'noindent'
    # which causes duplicate record for chapter opening quotes
    if (input_row[0] == 1 or input_row[0] == 8) and input_row[2] == 'blockquote':
        duplicates_list.append(True)
    else:
        duplicates_list.append(False)

    return duplicates_list


def empty_lines_handler(empty_lines_list, input_row):
    # Empty lines at the beginning of each chapter in Book 7 & 8
    empty_lines_set = {
        'linespace',
        'right-para',
        'center-para',
        'linegroup'
    }
    if input_row[2] in empty_lines_set or input_row[2][:5] == 'image':
        empty_lines_list.append(True)
    else:
        empty_lines_list.append(False)

    return empty_lines_list


def text_classification(dune_cronicles, book, chapter, paragraph):
    # split paragraphs into chapters
    chapter_starters = {
        1: 'blockquote',
        2: 'blockquote1a',
        3: 'extract',
        4: 'extract',
        5: 'epigraph',
        6: 'extracts',
        7: 'blockquote',
        8: 'blockquote'
    }

    class_name = paragraph.attrs['class'][0]
    text = paragraph.get_text().replace(
        '\n        ', '').replace(
        '\n', '').replace(
        '  ', ' ').replace(
        '  ', ' ')
    if class_name == chapter_starters[book]:
        chapter += 1
    if class_name == 'volume':
        text = str.upper(text)

    dune_cronicles.append([book, chapter, class_name, text])

    return dune_cronicles
