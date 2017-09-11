# Falling blocks as in Tetris(BUT NOT REALLY), use arrow \
# keys to move sideways and stack

import random

import simpleguitk as simplegui


# Player preferences
start_level = 0
left_movement = "left"
right_movement = "right"
clockwise_rotation = "up"
cc_rotation = "down"
soft_drop = "x"
hard_drop = "z"

# Standard Tetris grid is 10x22 blocks, top two row are
# hidden
# Define each block as 20 pixels

# setting up the gui stuff
width = 10
height = 22
block_size = 20

frame_width = 16
frame_height = 22

# scoring
num_cleared = 0
score = 0
level = 0

# define initial grid
grid = [[7 for j in range(height)] for i in range(width)]

# define dictionary to lookup color from grid values
color_Dict = {0: "Aqua", 1: "Orange", 2: "Blue", 3: "Purple", \
              4: "Red", 5: "Lime", 6: "Yellow", 7: "White", \
              8: "Black"}

# define helpers
def draw_block(c, pos, color):
    """ draws a block with position pos on the canvas c """
    c.draw_polygon([[pos[0], pos[1]], [pos[0] + block_size, \
                                       pos[1]], [pos[0] + block_size, \
                                                 pos[1] + block_size], [pos[0], \
                                                                        pos[1] + block_size]], 1, "White", color)


# define callbacks

def draw(c):
    """ callback for draw handler, draw blocks represented \
         by grid """

    global frame_height
    global block_size
    global pos_list
    global num_cleared
    global score
    global level
    global start_level

    c.draw_line((10 * block_size, 0), \
                (10 * block_size, frame_height * block_size), \
                15, "Black")
    c.draw_text("Next Block:", \
                (11 * block_size, 1 * block_size), \
                12, "Black")
    c.draw_text("Lines Cleared:", \
                (11 * block_size, 6 * block_size), \
                12, "Black")
    c.draw_text(str(num_cleared), \
                (13 * block_size, 7 * block_size), \
                12, "Black")
    c.draw_text("Score:", (11 * block_size, 9 * block_size), \
                12, "Black")
    c.draw_text(str(score), (13 * block_size, 10 * block_size), \
                12, "Black")
    c.draw_text("Level:", (11 * block_size, 12 * block_size), \
                12, "Black")
    c.draw_text(str(level + start_level), \
                (13 * block_size, 13 * block_size), \
                12, "Black")

    # drawing next block
    global width
    next_piece_offset = [(width - 2) * block_size, \
                         (2) * block_size]
    #print next_piece_offset
    for pos in pos_list.piece_dict[pos_list.next_piece]:
        draw_block(c, [pos[0] * block_size + \
                       next_piece_offset[0], \
                       pos[1] * block_size + \
                       next_piece_offset[1]], \
                   color_Dict[pos_list.next_piece])

    for i in range(width):
        for j in range(height):
            draw_block(c, [i * block_size, j * block_size], \
                       color_Dict[grid[i][j]])


class Controls:
    def __init__(self, left_movement, right_movement, \
                 clockwise_rotation, cc_rotation, \
                 soft_drop, hard_drop):
        """required init function"""
        self.previous_key = None
        self.left_movement = left_movement
        self.right_movement = right_movement
        self.clockwise_rotation = clockwise_rotation
        self.cc_rotation = cc_rotation  # still need to do
        self.soft_drop = soft_drop
        self.hard_drop = hard_drop  # still need to do

    def keydown_handler(self, key):
        """The keydown handler"""
        if self.previous_key == None:
            self.previous_key = key
            self.key = key
            self.keydown()  # so that holding down is not
            # necessary
            self.timer = simplegui.create_timer(1000.0 / 7, \
                                                self.keydown)
            self.timer.start()

    def keydown(self):
        """ key handler that control sideways motion of
            blocks """
        global pos_list
        global pos

        # finding the side pieces
        lowest_val = width
        highest_val = 0
        left_blocks = []
        right_blocks = []
        for pos in pos_list.piece:
            if pos[0] < lowest_val:
                lowest_val = pos[0]
                left_blocks = []
                left_blocks.append(pos)
            if pos[0] == highest_val:
                left_blocks.append(pos)
            if pos[0] > highest_val:
                highest_val = pos[0]
                right_blocks = []
                right_blocks.append(pos)
            if pos[0] == highest_val:
                right_blocks.append(pos)

        fall = check_fall()
        right, left = check_sideways()
        if self.key == simplegui.KEY_MAP \
                [self.left_movement] and \
                        left_blocks[0][0] != 0 and left:
            # update old squares to be white
            for block in pos_list.piece:
                grid[block[0]][block[1]] = 7
            pos_list.move_piece([-1, 0])

        elif self.key == simplegui.KEY_MAP \
                [self.right_movement] and \
                        right_blocks[0][0] != width - 1 and right:
            # update old squares to be white
            for block in pos_list.piece:
                grid[block[0]][block[1]] = 7
            pos_list.move_piece([1, 0])

        elif self.key == simplegui.KEY_MAP \
                [self.hard_drop] and fall:
            while fall:
                # update old squares to be white
                for block in pos_list.piece:
                    grid[block[0]][block[1]] = 7
                pos_list.move_piece([0, 1])
                fall = check_fall()

        elif self.key == simplegui.KEY_MAP \
                [self.soft_drop] and fall:
            # update old squares to be white
            for block in pos_list.piece:
                grid[block[0]][block[1]] = 7
            pos_list.move_piece([0, 1])

        elif self.key == simplegui.KEY_MAP \
                [self.clockwise_rotation]:
            pos_list.rotate(True)

        elif self.key == simplegui.KEY_MAP \
                [self.cc_rotation]:
            pos_list.rotate(False)

    def keyup(self, key):
        if key == self.previous_key:
            self.timer.stop()
            self.previous_key = None


class Blocks:
    def __init__(self):
        # 0:"I", 1:"L", 2:"J", 3:"T", 4:"Z", 5:"S", 6:"O"
        # O is a character not an int
        # self.block_dict = {0:"Aqua", 1:"Orange", \
        # 2:"Blue", 3:"Purple", 4:"Red",\
        # 5:"Lime", 6:"Yellow"}
        self.choice = random.randint(0, 6)  # last number
        # should be 6 and first 0
        self.next_piece = random.randint(0, 6)
        self.piece_dict = {0: [[3, 0], [4, 0], [5, 0], [6, 0]], \
                           1: [[4, 1], [5, 1], [6, 1], [6, 0]], \
                           2: [[4, 0], [4, 1], [5, 1], [6, 1]], \
                           3: [[4, 1], [5, 1], [6, 1], [5, 0]], \
                           4: [[4, 0], [5, 0], [5, 1], [6, 1]], \
                           5: [[5, 0], [6, 0], [4, 1], [5, 1]], \
                           6: [[4, 0], [5, 0], [4, 1], [5, 1]]}

    def create_piece(self):
        """Puts all 4 blocks together at the initial drop
            zone"""
        self.choice = self.next_piece
        self.next_piece = random.randint(0, 6)
        self.piece = self.piece_dict[self.choice]

        if self.choice == 0:
            self.piece = [[3, 0], [4, 0], [5, 0], [6, 0]]
            self.rotation_offset = \
                [[2, -1], [1, 0], [0, 1], [-1, 2]]
            self.cc_rotation_offset = \
                [[1, 2], [0, 1], [-1, 0], [-2, -1]]
        if self.choice == 1:
            self.piece = [[4, 1], [5, 1], [6, 1], [6, 0]]
            self.rotation_offset = \
                [[1, -1], [0, 0], [-1, 1], [0, 2]]
            self.cc_rotation_offset = \
                [[1, 1], [0, 0], [-1, -1], [-2, 0]]
        if self.choice == 2:
            self.piece = [[4, 0], [4, 1], [5, 1], [6, 1]]
            self.rotation_offset = \
                [[2, 0], [1, -1], [0, 0], [-1, 1]]
            self.cc_rotation_offset = \
                [[0, 2], [1, 1], [0, 0], [-1, -1]]
        if self.choice == 3:
            self.piece = [[4, 1], [5, 1], [6, 1], [5, 0]]
            self.rotation_offset = \
                [[1, -1], [0, 0], [-1, 1], [1, 1]]
            self.cc_rotation_offset = \
                [[1, 1], [0, 0], [-1, -1], [-1, 1]]
        if self.choice == 4:
            self.piece = [[4, 0], [5, 0], [5, 1], [6, 1]]
            self.rotation_offset = \
                [[2, 0], [1, 1], [0, 0], [-1, 1]]
            self.cc_rotation_offset = \
                [[0, 2], [-1, 1], [0, 0], [-1, -1]]
        if self.choice == 5:
            self.piece = [[5, 0], [6, 0], [4, 1], [5, 1]]
            self.rotation_offset = \
                [[1, 1], [0, 2], [1, -1], [0, 0]]
            self.cc_rotation_offset = \
                [[-1, 1], [-2, 0], [1, 1], [0, 0]]
        if self.choice == 6:
            self.piece = [[4, 0], [5, 0], [4, 1], [5, 1]]
            self.rotation_offset = \
                [[0, 0], [0, 0], [0, 0], [0, 0]]
            self.cc_rotation_offset = \
                [[0, 0], [0, 0], [0, 0], [0, 0]]

        self.move_piece([0, 0])  # draws the piece on
        # the starting point

    def move_piece(self, offset):
        """This function updates the piece's blocks'
            position the offset is a list with two
            elements. ex [0,1]"""
        global grid
        tmp = self.piece
        for block_idx in range(len(tmp)):
            self.piece[block_idx] = [tmp[block_idx][0] + \
                                     offset[0], \
                                     tmp[block_idx][1] + \
                                     offset[1]]
        for block in self.piece:  # coloring
            grid[block[0]][block[1]] = self.choice

    def rotate(self, CW):
        """Rotates the piece clockwise
            CW = True if clockwise, False otherwise"""
        global grid
        if CW == True:
            rot_offset = self.rotation_offset
        else:
            rot_offset = self.cc_rotation_offset
        if check_rotation(CW):
            # update old squares to be white
            for block in self.piece:
                grid[block[0]][block[1]] = 7

            # applying the offset
            tmp_piece = self.piece
            for pos_idx in range(len(tmp_piece)):
                self.piece[pos_idx][0] = self.piece[pos_idx] \
                                             [0] + rot_offset[pos_idx][0]
                self.piece[pos_idx][1] = self.piece[pos_idx] \
                                             [1] + rot_offset[pos_idx][1]

            # change rotation offsets for next time
            if CW:
                for i in [self.rotation_offset,
                          self.cc_rotation_offset]:
                    rot_tmp = i
                    for rot_idx in range(len(rot_tmp)):
                        i[rot_idx][1] = i[rot_idx][1] * (-1)
                        i[rot_idx].reverse()
            else:
                for i in [self.rotation_offset,
                          self.cc_rotation_offset]:
                    rot_tmp = i
                    for rot_idx in range(len(rot_tmp)):
                        i[rot_idx][0] = i[rot_idx][0] * (-1)
                        i[rot_idx].reverse()

            # coloring
            for pos in self.piece:
                grid[pos[0]][pos[1]] = self.choice


def check_rotation(CW):
    """Checks if the rotation is valid
        CW = True if clockwise, False otherwise"""
    global pos_list
    global grid
    if CW == True:
        rot_offset = pos_list.rotation_offset
    else:
        rot_offset = pos_list.cc_rotation_offset
    rotation = True
    check_pos = []
    for pos_idx in range(len(pos_list.piece)):
        check_pos.append([pos_list.piece[pos_idx][0] + \
                          rot_offset[pos_idx][0], \
                          pos_list.piece[pos_idx][1] + \
                          rot_offset[pos_idx][1]])
    for i in check_pos:
        if i[0] < 0 or i[1] < 0 or i[0] > width - 1 or \
                        i[1] > height - 1:
            rotation = False
            return rotation
    for col_idx in range(len(grid)):
        for row_idx in range(len(grid[0])):
            if grid[col_idx][row_idx] != 7 and \
                            [col_idx, row_idx] in check_pos and \
                            [col_idx, row_idx] not in pos_list.piece:
                rotation = False
                return rotation
    return rotation


def check_fall():
    """Checks if the piece can fall"""
    fall = True
    global pos_list
    for pos in pos_list.piece:  # seeing if the piece
        #needs to stop
        if pos[1] == height - 1:  #seperate to avoid indexing
            #errors in the elif
            fall = False
            break
        elif grid[pos[0]][pos[1] + 1] != 7 and ([pos[0], \
                                                 pos[1] + 1] not in pos_list.piece):
            fall = False
            break
    return fall


def check_sideways():
    """Checks if the piece can move sideways"""
    global pos_list
    right = True
    left = True
    for pos in pos_list.piece:
        if pos[0] == width - 1:
            right = False
        elif grid[pos[0] + 1][pos[1]] != 7 and \
                ([pos[0] + 1, pos[1]] not in pos_list.piece):
            right = False
        if grid[pos[0] - 1][pos[1]] != 7 and \
                ([pos[0] - 1, pos[1]] not in pos_list.piece):
            left = False
    return right, left


class Theme:
    """deals with sound"""

    def __init__(self):
        pass

    # self.sound = simplegui.load_sound(
    # "http://commondatastorage.googleapis.com/codeskulptor-assets/Tetris-Theme-Original.mp3")
    #        self.sound.play()
    #        self.sound.set_volume(1)
    #        self.last_time = time.time()

    def check_restart(self):
        pass

    #        if time.time() - self.last_time > 48:  #0:48 = music length
    # self.sound.rewind()
    #            self.sound.play()
    #            self.last_time = time.time()

    def stop(self):
        pass


# self.sound.pause()  #stops the music


def my_update():
    """updates the blocks' positions"""
    global pos_list
    global grid
    global song_them
    global num_cleared
    global score
    global level
    global start_level

    lines_bonus = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

    #checks if song needs to loop
    song_theme.check_restart()

    #finding the lowest block
    #21 is the bottom and 0 is the top
    lowest_val = -1
    lowest_blocks = []
    for pos in pos_list.piece:
        if pos[1] > lowest_val:
            lowest_val = pos[1]
            lowest_blocks = []
            lowest_blocks.append(pos)
        if pos[1] == lowest_val:
            lowest_blocks.append(pos)

    fall = check_fall()

    #move the piece
    if fall == True:
        #update old squares to be white
        for block in pos_list.piece:
            grid[block[0]][block[1]] = 7
        #draws the new piece
        pos_list.move_piece([0, 1])

    lose_flag = False
    if fall == False:
        for pos in pos_list.piece:
            if pos[1] == 0:
                lose_flag = True
                break

    if lose_flag == False and fall == False:
        remove_lines = check_line()
        num_cleared += len(remove_lines)
        score += lines_bonus[len(remove_lines)] * \
                 (start_level + level + 1)
        if num_cleared >= (level + 1) * 10:
            level += 1
        clear_lines(remove_lines)
        pos_list.create_piece()

    if lose_flag == True:
        print("You lose")
        t.stop()
        grid = [[8 for j in range(height)] \
                for i in range(width)]
        song_theme.stop()


def check_line():
    """This function checks if a line needs to disappear"""

    global grid
    #populating the list
    remove_lines = []
    for i in range(height):
        remove_lines.append(i)

    tmp = grid
    for row_idx in range(len(tmp[0])):
        for col_idx in range(len(tmp)):
            if tmp[col_idx][row_idx] == 7:
                if row_idx in remove_lines:
                    remove_lines.remove(row_idx)

    return remove_lines


def clear_lines(remove_lines):
    """This function clears lines"""
    global grid
    tmp = grid
    for line_num in remove_lines:
        for col_idx in range(len(tmp)):
            grid[col_idx][line_num] = 7

    #updates the grid after the lines are removed
    tmp = grid
    for line in remove_lines:
        for row_idx in range(line + 1):
            for col_idx in range(len(tmp)):
                if line - row_idx != 0:
                    grid[col_idx][line - row_idx] = \
                        tmp[col_idx][line - row_idx - 1]

# initialize position of first block
pos_list = Blocks()
pos_list.create_piece()

song_theme = Theme()
controls = Controls(left_movement, right_movement, \
                    clockwise_rotation, cc_rotation, \
                    soft_drop, hard_drop)

f = simplegui.create_frame("Tetris Clone", \
                           frame_width * block_size, \
                           frame_height * block_size, 200)
f.set_canvas_background("White")
f.set_draw_handler(draw)
f.set_keydown_handler(controls.keydown_handler)
f.set_keyup_handler(controls.keyup)

# create and start timer for block motion
t = simplegui.create_timer(1000.0 / (start_level + level + 1), \
                           my_update)
t.start()

f.start()

# Written by Sarah Davies to raise awareness of
# procrastination as a legitimate hobby.