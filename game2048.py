#! /usr/bin/env python3

import random
import itertools


class Game2048:
    def __init__(self, size=4, target=2048):
        """Init a game
        @param: size, positive integer, size of board
        @param: target, the winning score
        """

        self.size = size
        self.target = target
        self.best = 0

        self._rng = random.Random()
        self._sample = [2]*4+[4]

        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self._coordinates = itertools.product(range(self.size), repeat=2)
        self._empty = list(self._coordinates)

        self._width = len(str(self.target))

        # add two numbers
        for _ in range(2):
            self.add_num()

        pass

    def __repr__(self):
        """Print Board
        """
        repr = ''
        repr += '-' * ((self._width + 3) * self.size) + '-\n'
        for r in range(self.size):
            row = self.board[r]
            for val in row:
                val_s = str(val)
                d = self._width - len(val_s)
                val_s = ' '*((d+1) // 2) + val_s + ' '*(d // 2)
                repr += '| {} '.format(val_s)
            repr += '|\n'
            if r != self.size-1:
                repr += '|' + '-' * ((self._width + 3) * self.size - 1) + '|\n'
        repr += '-' * ((self._width + 3) * self.size) + '-\n'
        return repr

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

    def move(self, direction=None):
        """Move the board
        @ param: direction, a letter 'U'/'D'/'L'/'R'
        @ return: True if valid move, otherwise False
        """
        valid = False

        # move board
        old = self.board.copy()
        # TODO

        if old != self.board:
            # board updated
            valid = True
        else:
            # board not updated
            valid = False

        valid = True
        # add new number
        if valid:
            self.add_num()
        return valid

    def run(self, ai=None):
        """Run the game
        @param: ai, a function with
                    input: board status
                    output: a move within 'UDLR'
        """
        if ai is None:
            ai = self.get_move

        print(self)

        end = False
        while end is False:
            m = ai(self.board)
            if len(m) != 1 or m not in 'UDLR':
                continue

            valid = self.move(m)
            if valid is False:
                # not valid move
                print('Not valid move.')
                continue

            # valid move
            print(self)
            if self.is_win():
                print("You WIN!!!")
                end = True
            elif self.is_dead():
                print("You LOSE >_<")
                end = True

    def is_win(self):
        return self.best == self.target

    def is_dead(self):
        return len(self._empty) == 0

    def get_move(self):
        got = False
        while got is False:
            m = input("Move (U)p / (D)own/ (L)eft / (R)ight ? ").upper()[0]
            if m in 'UDLR':
                got = True
            else:
                print("Not valid input.")
        return m


if __name__ == '__main__':
    game = Game2048()

    def myai(board):
        return random.choice('UDLR')

    game.run(ai=myai)
