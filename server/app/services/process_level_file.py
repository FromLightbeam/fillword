import zipfile
import io
import math

from ..helpers.math import is_square

class ValidationException(Exception):
    pass

def unzip_level_files(file):
    words = []
    levels = []

    # UNZIP
    zf = zipfile.ZipFile(io.BytesIO(file), "r")
    for fileinfo in zf.infolist():
        if (fileinfo.filename == 'words_list.txt'):
            words = zf.read(fileinfo).decode('utf-8').splitlines()

        if (fileinfo.filename.startswith('levels/') and not fileinfo.is_dir()):
            levels.append((fileinfo.filename.replace('levels/', ''), zf.read(fileinfo).decode('utf-8'))) 
    
    return words, levels

def process_levels(words, levels):
    level_infos = []

    # transform to user like object
    for filename, level in levels:
        level_info = {
            'filename': filename,
            'matrix': None,
            'words': [],
            "bonus_words": [],
            "status": ''
        }

        try:
            chunks = level.split(' ')
            level_summ = 0
            level_dict = {}

            while len(chunks):
                try:
                    level_word = int(chunks.pop(0))
                    level_path = list(map(lambda x: int(x), chunks.pop(0).split(';')))
                    level_dict[level_word] = level_path
                except:
                    raise ValidationException('Incorrect format of decision')

                level_summ += len(level_path)

            if not is_square(level_summ):
                raise ValidationException('Incorrect format of decision')

            level_size = math.isqrt(level_summ)
            matrix = [['*' for col in range(level_size)] for row in range(level_size)]

            for word_index, path in level_dict.items():
                if len(words) <= word_index:
                    raise ValidationException('Cannot find word')

                word = words[word_index]

                level_info['words'].append(word)

                word_iterator = iter(word)

                for letter_index in path:
                    if letter_index >= level_summ:
                        raise ValidationException('Wrong letter in decision')

                    i = letter_index // level_size
                    j = letter_index % level_size
                    try:
                        letter = next(word_iterator)
                        matrix[i][j] = letter

                    except StopIteration:
                        raise ValidationException('Too short word')
            level_info['matrix'] = matrix
            level_info['status'] = 'valid'

        except ValidationException as e:
            level_info['status'] = 'Error: ' + str(e)

        level_infos.append(level_info)
            
    return level_infos