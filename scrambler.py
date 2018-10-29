#!/usr/bin/python
import random
import sys


FACES = (
    ('F', 'B'),
    ('L', 'R'),
    ('U', 'D')
)

POSTFIXES = ('', '2', '\'')


class Move():
    def __init__(self, axis=None, pole=None, postfix=None):
        """Abstract description of a move encoded as integers.

        axis (0, 1 2): FB, LR, UD
        pole (0, 1): determintes the specific face on a given axis
        postfix (0, 1, 2): the factor of quarter turns of the face
        """
        self.axis = axis
        self.pole = pole
        self.postfix = postfix


def get_random_move_without_postfix():
    return Move(
        axis=random.randint(0, 2),
        pole=random.randint(0, 1),
        postfix=None
    )


def is_move_valid(cur_move, prev_move, prev_2_move):
    same_face_twice = cur_move.axis == prev_move.axis and cur_move.pole == prev_move.pole
    same_axis_three_times = cur_move.axis == prev_move.axis == prev_2_move.axis
    return not same_face_twice and not same_axis_three_times


def get_scramble(group=0):
    counter = 0
    prev_move = Move()
    prev_2_move = Move()
    scramble = []

    while counter < 25:
        cur_move = get_random_move_without_postfix()
        if not is_move_valid(cur_move, prev_move, prev_2_move):
            continue
        cur_move.postfix = '2' if cur_move.axis < group else random.choice(POSTFIXES)
        scramble += [cur_move]
        prev_2_move, prev_move = prev_move, cur_move
        counter += 1

    return ' '.join([FACES[move.axis][move.pole] + move.postfix for move in scramble])


def is_valid_invocation(argv):
    return len(argv) == 1 or (
        len(argv) == 2 and
        len(argv[1]) == 3 and
        argv[1].startswith('-g') and
        argv[1][-1] in ['1', '2', '3']
    )


if __name__ == '__main__':
    if not is_valid_invocation(sys.argv):
        print "Usage: {file} [-gN] (where N is the group number between 1 and 3)".format(file=sys.argv[0])
        sys.exit(1)
    lastarg = sys.argv[-1]
    if lastarg.startswith('-g') and lastarg[-1] in ['1', '2', '3']:
        group = int(lastarg[-1])
    else:
        group = 0
    print(get_scramble(group))
