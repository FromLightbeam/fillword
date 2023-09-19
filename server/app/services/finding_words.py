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

def find_bonus(words, level_matrix, exesting_words=[]):
    new_words = []
    for word in words:
        if word not in exesting_words and find_word(level_matrix, word):
            new_words.append(word)
    return new_words
