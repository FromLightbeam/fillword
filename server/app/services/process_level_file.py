import zipfile
import io
import math

from ..helpers.math import is_square

def unzip_level_files(file):
    words = []
    levels = []

    # UNZIP
    zf = zipfile.ZipFile(io.BytesIO(file), "r")
    for fileinfo in zf.infolist():
        if (fileinfo.filename == 'words_list.txt'):
            words = zf.read(fileinfo).decode('utf-8').splitlines()

        if (fileinfo.filename.startswith('levels/') and not fileinfo.is_dir()):
            levels.append(zf.read(fileinfo).decode('utf-8')) 
        # TODO when file not found throw error
    
    return words, levels

def process_levels(words, levels):
    level_infos = []

    # transform to user like object
    for level in levels:
        chunks = level.split(' ')

        level_summ = 0

        level_dict = {}
        level_info = {'matrix': None, 'words': [], "bonus_words": []}

        while len(chunks):
            level_word = int(chunks.pop(0))
            level_path = list(map(lambda x: int(x), chunks.pop(0).split(';')))
            level_dict[level_word] = level_path

            # TODO validation here
            level_summ += len(level_path)


        if is_square(level_summ):
            level_size = math.isqrt(level_summ)
            matrix = [['*' for col in range(level_size)] for row in range(level_size)]

            for word_index, path in level_dict.items():
                word = words[word_index]

                level_info['words'].append(word)

                word_iterator = iter(word)

                for letter_index in path:
                    if letter_index >= level_summ:
                        # TODO throw exception skip the level
                        continue

                    i = letter_index // level_size
                    j = letter_index % level_size
                    try:
                        letter = next(word_iterator)
                        matrix[i][j] = letter

                    except StopIteration:
                        # TODO throw exception skip the level
                        print('STOP ITERATION')
            level_info['matrix'] = matrix
            level_infos.append(level_info)
    return level_infos