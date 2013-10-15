import datetime

import mock
import unittest


import football_odds_emailer


def get_text_from_file(filepath):
	with open(filepath) as file:
		return file.read()

class OddsGetterTest(unittest.TestCase):

	def test_get_odds(self):
		books_text = get_text_from_file('tests/datafiles/books.xml')
		games_text = get_text_from_file('tests/datafiles/games.xml')
		with mock.patch.object(
			football_odds_emailer,
			'get_text_from_url',
			side_effect=[books_text, games_text]
		):
			self.assertEqual(
				football_odds_emailer.OddsGetter().get_odds(),
				[
					{
						'time': datetime.datetime(2013, 10, 15, 17),
						'teams': [
							{'number': '301', 'name': 'UL Lafayette', 'Opener': '', 'Bookmaker': '', 'BOnline': '3-115', '5Dimes': ''},
							{'number': '302', 'name': 'Western Kentucky', 'Opener': '6', 'Bookmaker': '4.5', '5Dimes': '4', 'BOnline': ''}
						]
					}
				]
			)
