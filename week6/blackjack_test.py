__author__ = 'claube'

import unittest

from blackjack import Blackjack


class MyTestCase(unittest.TestCase):
    def test_something(self):
        bj = Blackjack()
        bj.deal()
        bj.hit()
        print str(bj.player_hand)
        print str(bj.dealer_hand)

if __name__ == '__main__':
    unittest.main()
