import string


class BoggleBoard(object):
    """
    Internal representation of an nxn Boggle board. For the purposes of the 
    solver,  the board can be thought of as an undirected graph, where each node
    contains  a letter and is connected by edges to its immediate and diagonal
    neighbors. 

    Since we're going to be calculating neighbors frequently, we can optimize
    our representation to simplify this case by padding the outside of the board
    with None values. For a 3x3 board, for example, we visualize the board as:

    0 0 0 0 0
    0 A B C 0
    0 D E F 0
    0 G H I 0
    0 0 0 0 0

    This cuts down on edge cases as we calculate the neighbor set for a given
    node; rather than having to check for the edges of the board, we just check
    whether the value returned is None. There may be some performance
    improvement from this approach (due to fewer and simpler conditionals), but 
    the main benefit is the simplicity of the code.

    To represent the board in memory, we encode the graph as a simple list of 
    characters. Since the edge set for each node is fixed, the list 
    representation lets us use simple arithmetic to calculate a node's 
    neighbors. So the above 3x3 board is represented by:

    00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
    0  0  0  0  0  0  A  B  C  0  0  D  E  F  0  0  G  H  I  0  0  0  0  0  0

    From this representation, we can calculate the neighbors of node x in a grid 
    of size n as:
        NW: x-n-3
         N: x-n-2
        NE: x-n-1
         W: x-1
         E: x+1
        SW: x+n+1
         S: x+n+2
        SE: x+n+3
        
    For simplicity in comparisons, we normalize all characters by converting
    them to lower case.
    """

    def __init__(self, values, board_width=4):
        """
        Create a new board with the size and values supplied
        :param values: A list of single-character ASCII strings.
        :param board_width: An int containg the width of a square Boggle board.
        """
        BoggleBoard._check_input(board_width, values)
        self.board_width = board_width
        self.board = BoggleBoard._to_internal_representation(board_width,
                                                             values)

    def get_nodes(self):
        """
        Get a list of node identifiers and values for the board. 

        A node identifier is guaranteed to uniquely and consistently identify a
        node throughout the life of an instance of this class. However, callers
        of this method should not assume any meaning in the values of the
        node identifiers. An implementation of this class will assign 
        identifiers based on its internal representation, which may change as
        the code evolves.

        :return: a list of two-value tuples, each of which contains a
        (node_id, node_value) pair. Node values will be returned in lower case.
        """
        nodes = []
        for idx in range(0, len(self.board)):
            if self.board[idx]:
                nodes.append((idx, self.board[idx]))
        return nodes

    def get_neighbors(self, node_id, exclude=None):
        """
        Get the neighbor set for this node, assuming that all nodes have edges
        to their immediate and diagonal neighbors. Optionally, exclude a set of
        nodes from the neighbor set; if a node's identifier is in this set it 
        will not be returned as a neighbor. Any identifers in the set that would
        not otherwise have been returned as neighbors will be ignored.
        
        :param node_id: The node identifier, as defined by this object, for a
        node. The method will find all valid neighbors of this node.
        :param exclude: An optional set of node identifiers (as defined by this
        object) to exclude from the returned neighbor set.
        :return: a list of two-value tuples, each of which contains a
        (node_id, node_value) pair. Node values will be returned in lower case.
        """
        # TODO: Check that incoming node IDs are valid
        if not exclude:
            exclude = set()
        neighbors = []
        offset_north = node_id - self.board_width - 2
        offset_south = node_id + self.board_width + 2
        for neighbor_idx in [
                    offset_north - 1,
            offset_north,
                    offset_north + 1,
                    node_id - 1,
                    node_id + 1,
                    offset_south - 1,
            offset_south,
                    offset_south + 1
        ]:
            value = self.board[neighbor_idx]
            if value and neighbor_idx not in exclude:
                neighbors.append((neighbor_idx, value))
        return neighbors

    # Convert a list of values representing a (grid_size x grid_size) boggle
    # board into the internal representation described in the class
    # documentation (a None-padded, single list representation, where all
    # characters are lower-case).
    @staticmethod
    def _to_internal_representation(board_width, values):
        board = [None] * (board_width + 2)
        for row in range(0, board_width):
            board += [None] + [
                v.lower() for v in values[
                                   (row * board_width):
                                   (row * board_width) + board_width]
            ] + [None]
        board += [None] * (board_width + 2)
        return board

    # Validate input for the initializer; expect the grid size to be an int >= 1
    # and values be a list of ascii strings, each one character long.
    @staticmethod
    def _check_input(grid_size, values):
        if not type(grid_size) == int:
            raise ValueError(u"Grid size {} must be an int.".format(
                grid_size
            ))
        if not grid_size > 0:
            raise ValueError(u"Invalid grid size {}.".format(
                grid_size
            ))
        if len(values) != grid_size * grid_size:
            raise ValueError(u"Expected {} values, saw {}.".format(
                grid_size * grid_size, len(values)
            ))
        for value in values:
            if not value or value not in string.ascii_letters:
                raise ValueError(u"Invalid value {} in input".format(
                    value
                ))
            if len(value) != 1:
                raise ValueError(u"Expected single character, saw {}.".format(
                    value
                ))


class BoggleSolver(object):
    def __init__(self, board, word_list):
        self.board = board
        self.word_list = word_list
        self.matches = set()

    def find_words(self):
        """
        Find all words within the Boggle board.
        :return: a list of Strings containing all matching words.
        """
        for node_id, node_val in self.board.get_nodes():
            self._find_suffix_words(node_id, node_val, '', set())
        result_list = list(self.matches)
        result_list.sort(key=lambda s: len(s), reverse=True)
        return result_list

    def _find_suffix_words(self, node_id, node_val, prefix, exclude):
        word_at_node = "{}{}".format(prefix, node_val)
        if self.word_list.contains_word(word_at_node):
            self.matches.add(word_at_node)
        if self.word_list.contains_prefix(word_at_node):
            neighbor_exclude = exclude.union({node_id})
            for neighbor_id, neighbor_val in self.board.get_neighbors(
                    node_id, neighbor_exclude
            ):
                self._find_suffix_words(
                    neighbor_id, neighbor_val, word_at_node, neighbor_exclude
                )
