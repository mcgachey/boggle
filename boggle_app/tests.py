# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ddt import ddt, data
import string
import unittest

from boggle_solver import BoggleBoard


class FourByFourBoardTest(unittest.TestCase):
    # A B C D
    # E F G H
    # I J K L
    # M N O P
    STANDARD_BOARD = string.ascii_uppercase[0:16]

    def setUp(self):
        self.board = BoggleBoard(FourByFourBoardTest.STANDARD_BOARD)

    def test_all_values_stored(self):
        board_values = [val for _, val in self.board.get_nodes()]
        for value in FourByFourBoardTest.STANDARD_BOARD:
            self.assertTrue(
                value.lower() in board_values, "Missing value: {}".format(value)
            )

    def test_node_count(self):
        nodes = len(self.board.get_nodes())
        self.assertEqual(
            nodes, 16, "Incorrect number of nodes returned ({})".format(nodes)
        )


@ddt
class FourByFourNeighborTest(FourByFourBoardTest):
    # Data provider for data-driven tests. Each line contains a node and a list
    # of expected neighbors (using the standard board defined in the parent
    # class).
    @data(
        ('f', ['a', 'b', 'c', 'e', 'g', 'i', 'j', 'k']),
        ('a', ['b', 'e', 'f']),
        ('b', ['a', 'c', 'e', 'f', 'g']),
        ('d', ['c', 'g', 'h']),
        ('i', ['e', 'f', 'j', 'n', 'm']),
        ('p', ['k', 'l', 'o']),
    )
    def test_expected_neighbors(self, (node_val, expected_neighbors)):
        for node_id, val in self.board.get_nodes():
            if val == node_val:
                neighbor_vals = [
                    v for _, v in self.board.get_neighbors(node_id)
                ]
                self.assertEqual(len(neighbor_vals), len(expected_neighbors))
                for expected in expected_neighbors:
                    self.assertTrue(
                        expected in neighbor_vals,
                        "Expected value {} in neighbor set".format(expected)
                    )
                for seen in neighbor_vals:
                    self.assertTrue(
                        seen in expected_neighbors,
                        "Saw unexpected value {} in neighbor set".format(seen)
                    )

# To test:
#   Invalid constructor arguments
#   Excluded values aren't returned as neighbors
#   Exclude sets containing nodes that wouldn't be expected in the neighbor set
#   All characters converted to lower case
#   Boards with duplicate characters
#   Passing invalid node IDs
#   Board sizes other than 4x4

