# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ddt import ddt, data
import string
import unittest

from boggle_solver import BoggleBoard
from word_list import WordList


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


@ddt
class FourByFourExcludeTest(FourByFourBoardTest):
    # Data provider for data-driven tests. Each line contains a node and a list
    # of expected neighbors (using the standard board defined in the parent
    # class).
    @data(
        ('f', ['a', ]),
        ('f', ['a', 'b', 'c', 'e', 'g', 'i', 'j', 'k']),
        ('a', ['b', 'f']),
        ('b', ['a', 'f', 'g']),
        ('d', []),
        ('i', ['e', 'n', 'm']),
        ('p', ['k', 'l', 'o']),
    )
    def test_excluded_neighbors(self, (node_val, excluded)):
        id_map = {v: i for i, v in self.board.get_nodes()}
        exclude = set([id_map[v] for v in excluded])
        neighbor_ids = [
            n_id for n_id, _ in self.board.get_neighbors(
                id_map[node_val], exclude
            )]
        for excluded_id in exclude:
            self.assertTrue(
            excluded_id not in neighbor_ids,
                "Excluded neighbor node {} present in neighbor set".format(
                    excluded_id
                )
            )


# To test:
#   Invalid constructor arguments
#   Exclude sets containing nodes that wouldn't be expected in the neighbor set
#   All characters converted to lower case
#   Boards with duplicate characters
#   Passing invalid node IDs
#   Board sizes other than 4x4


@ddt
class WordListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word_list = WordList('boggle_app/word_lists/en.txt')

    @data(
        'still', 'crazy', 'after', 'all', 'these', 'years'
    )
    def test_expected_word(self, word):
        self.assertTrue(
            WordListTest.word_list.contains_word(word),
            "Expected word '{}' missing from list".format(word)
        )

    @data(
        'foob', 'grug', 'pubbawup', 'wattoom', 'gazork', 'spuzz'
    )
    def test_missing_word(self, word):
        self.assertFalse(
            WordListTest.word_list.contains_word(word),
            "Unexpected word '{}' found in list".format(word)
        )

    @data(
        'a', 'thi', 'yes', 'no', 'ecumenic'
    )
    def test_expected_prefix(self, prefix):
        self.assertTrue(
            WordListTest.word_list.contains_prefix(prefix),
            "Expected prefix '{}' missing from list".format(prefix)
        )

    @data(
        'kzn', 'eee', 'crazycat'
    )
    def test_missing_prefix(self, prefix):
        self.assertFalse(
            WordListTest.word_list.contains_prefix(prefix),
            "Unexpected prefix '{}' found in list".format(prefix)
        )
