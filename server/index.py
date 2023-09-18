from fastapi import FastAPI, File
from typing import Annotated

import zipfile
import io
import math

app = FastAPI()

def find_neighbors(grid, row, col):
    neighbors = []
    rows, cols = len(grid), len(grid[0])
    
    # Define the relative positions of neighbors
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        
        # Check if the neighbor is within the grid boundaries
        if 0 <= r < rows and 0 <= c < cols:
            neighbors.append((r, c))
    
    return neighbors


def is_square(i: int) -> bool:
    return i == math.isqrt(i) ** 2

def find_word(matrix, word):
    if not matrix or not matrix[0]:
        return False

    rows, cols = len(matrix), len(matrix[0])
    
    stack = []
    visited = set()
    
    # Helper function to check if a cell is valid and matches the current word character
    def is_valid(row, col, word_index):
        return 0 <= row < rows and 0 <= col < cols and matrix[row][col] == word[word_index] and (row, col) not in visited
    
    # Iterate through each cell in the matrix
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == word[0]:
                stack.append((row, col, 0))  # (row, col, word_index)
                
                while stack:
                    r, c, word_index = stack.pop()
                    
                    if word_index == len(word) - 1:
                        return True  # Found the word
                        
                    visited.add((r, c))  # Mark the current cell as visited
                    
                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_r, new_c = r + dr, c + dc
                        
                        if is_valid(new_r, new_c, word_index + 1):
                            stack.append((new_r, new_c, word_index + 1))
                    
                visited.clear()  # Clear visited set after each search

    return False

def find_bonus(words, level):
    print('level["matrix"]', level["words"])
    for word in words:
        if find_word(level["matrix"], word):
            print('word', word)


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.post("/api/files")
async def create_file(file: Annotated[bytes, File()]):
    words = []
    levels = []
    level_infos = []

    # UNZIP
    zf = zipfile.ZipFile(io.BytesIO(file), "r")
    for fileinfo in zf.infolist():
        if (fileinfo.filename == 'words_list.txt'):
            words = zf.read(fileinfo).decode('utf-8').splitlines()

        if (fileinfo.filename.startswith('levels/') and not fileinfo.is_dir()):
            levels.append(zf.read(fileinfo).decode('utf-8')) 
        # TODO when file not found throw error
    
    # transform to user like object
    for level in levels[:10]:
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
            search_matrix = []

            for word_index, path in level_dict.items():
                word = words[word_index]

                level_info['words'].append(word)

                word_iterator = iter(word)

                for letter_index in path:
                    # print('letter_index', level)
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
            # print('matrix', matrix)
    # print("level_infos", level_infos)
    find_bonus(words, level_infos[9])

    return level_infos[0:10]
