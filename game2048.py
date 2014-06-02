#! /usr/bin/env python3

import random
import copy


class Game2048:
    def __init__(self, size=4, target=2048, ai=None):
        """Init a game
        :param size: positive integer, size of board
        :param target: the winning score
        :param ai: a function compute a move by board status
                    :param board: board status
                    :return ch: chr in 'UDLR'
        """

        try:
            assert isinstance(size, int) and size > 0
            assert isinstance(target, int) and target > 0
        except AssertionError:
            print('ValueError: `size` and `target` should be non-negative integers.')
            exit(1)

        self.size = size
        self.target = target

        if ai is None:
            def cli_input(board):
                assert isinstance(board, list)
                got = False
                my_move = ''
                while got is False:
                    my_move = input("Move (U)p / (D)own/ (L)eft / (R)ight ? ")
                    my_move = my_move.upper()[0]
                    if my_move in list('UDLR'):
                        got = True
                    else:
                        print("Not valid input.")
                return my_move

            self.ai = cli_input
        else:
            self.ai = ai

        self.best = 0
        self.step = 0

        self._rng = random.Random()
        self._sample = [2]*4+[4]

        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._coordinates = [(r, c) for r in range(self.size) for c in range(self.size)]
        self._empty = self._coordinates[:]

        self._move_dic = dict({})
        self._move_dic['L'] = [[(r, c) for c in range(self.size)] for r in range(self.size)]
        self._move_dic['R'] = [[(r, self.size - 1 - c) for c in range(self.size)] for r in range(self.size)]
        self._move_dic['U'] = [[(r, c) for r in range(self.size)] for c in range(self.size)]
        self._move_dic['D'] = [[(self.size - 1 - r, c) for r in range(self.size)] for c in range(self.size)]

        self._width = len(str(self.target))

        # add two numbers
        for _ in range(2):
            self.add_num()

    def __repr__(self):
        """Print Board
        """
        board_str = ''
        board_str += '-' * ((self._width + 3) * self.size) + '-\n'
        for r in range(self.size):
            row = self.board[r]
            for val in row:
                val_s = str(val) if val != 0 else ' '
                d = self._width - len(val_s)

                # align center
                # val_s = ' ' * ((d+1) // 2) + val_s + ' ' * (d // 2)
                # align right
                val_s = ' ' * d + val_s

                board_str += '| {} '.format(val_s)
            board_str += '|\n'
            if r != self.size-1:
                board_str += '|' + '-' * ((self._width + 3) * self.size - 1) + '|\n'
        board_str += '-' * ((self._width + 3) * self.size) + '-\n'
        return board_str

    def add_num(self, val=None):
        """Add a number at random empty cell
        """
        r, c = self._rng.choice(self._empty)
        self._empty.remove((r, c))

        if val is None:
            val = self._rng.choice(self._sample)

        self.board[r][c] = val

        self.best = max(self.best, val)
        return

    def merge(self, direction=None):
        """Move the board
        @ param: direction, a letter 'U'/'D'/'L'/'R'
        @ return: True if valid move, otherwise False
        """
        valid = False
        self._empty = []
        # print('Dir: ', direction)
        rows = self._move_dic[direction]
        for row in rows:
            old_values = [self.board[r][c] for (r, c) in row if self.board[r][c] != 0]
            new_values = []
            i = 0
            while i < len(old_values):
                if i + 1 < len(old_values) and old_values[i] == old_values[i + 1]:
                    # current value equals next value --> merge
                    new_values.append(old_values[i] * 2)
                    i += 2
                else:
                    # 1. current and next not equal
                    # 2. only one value
                    # either way, put it to new array
                    new_values.append(old_values[i])
                    i += 1
            # padding with 0
            new_values += [0] * (self.size - len(new_values))
            # copy back
            for i in range(len(row)):
                (r, c) = row[i]
                if valid is False and self.board[r][c] != new_values[i]:
                    # board has a update
                    valid = True
                self.board[r][c] = new_values[i]
                if self.board[r][c] == 0:
                    self._empty.append((r, c))
                else:
                    # update max score
                    self.best = max(self.best, self.board[r][c])

        return valid

    def run(self):
        """Run the game
        """
        print(self)

        end = False
        while end is False:

            # make a copy in case ai() tries to modify the board status
            tmp_board = copy.deepcopy(self.board)
            m = self.ai(tmp_board)

            if len(m) != 1 or m not in list('UDLR'):
                continue

            valid = self.merge(m)
            if valid is False:
                # not valid move
                # print('Not valid move.')
                continue
            else:
                # valid move
                # add new number
                self.step += 1
                self.add_num()

            # valid move
            print('\nStep: {}\tMove: {}'.format(self.step, m))
            print(self)

            # check if game ends
            if self.is_win():
                print("You WIN!!!")
                end = True
            elif self.is_dead():
                print("You LOSE >_<")
                end = True

    def is_win(self):
        return self.best >= self.target

    def is_dead(self):
        # empty cell exists
        if len(self._empty) > 0:
            return False

        # cell full, but can merge: two neighbor are the same
        dead = True
        # print(list(self._coordinates))
        for (r, c) in self._coordinates:
            # print((r, c))
            # look right
            if c + 1 < self.size and self.board[r][c] == self.board[r][c + 1]:
                dead = False
                break
            # look down
            if r + 1 < self.size and self.board[r][c] == self.board[r + 1][c]:
                dead = False
                break

        return dead


if __name__ == '__main__':
    def my_ai(board):
        isinstance(board, list)
        return random.choice('U' * 10 + 'D' + 'L' * 10 + 'R')

    game = Game2048(target=256, size=4, ai=my_ai)

    game.run()
