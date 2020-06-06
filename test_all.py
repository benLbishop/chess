import unittest
from tests.test_piece import PieceTest
from tests.test_board import TestBoard
from tests.test_player import TestPlayer
from tests.test_square import TestSquare
from tests.test_move_logic import TestMoveLogic

def make_suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(PieceTest))
    test_suite.addTest(unittest.makeSuite(TestBoard))
    test_suite.addTest(unittest.makeSuite(TestPlayer))
    test_suite.addTest(unittest.makeSuite(TestSquare))
    test_suite.addTest(unittest.makeSuite(TestMoveLogic))
    return test_suite

suite = make_suite()

runner = unittest.TextTestRunner()
runner.run(suite)