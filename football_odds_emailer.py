import datetime

import requests
from BeautifulSoup import BeautifulSoup


def get_text_from_url(url):
	return requests.get(url)


class OddsGetter(object):
	odds_url = 'http://jimfeist.com/lines/schedule.php?host=BIGPROFITS&sport=ncaafb&period=0'
	books_url = 'http://jimfeist.com/lines/books.php?host=BIGPROFITS'

	def get_odds(self):
		book_id_to_name = self._get_book_id_to_name()
		return self._get_odds(book_id_to_name)

	def _get_book_id_to_name(self):
		books_text = get_text_from_url(self.books_url)
		soup = BeautifulSoup(books_text)
		book_soups = soup.books.findAll('book')
		return dict(
			(book_soup['id'], book_soup['name']) for book_soup in book_soups
		)

	def _get_odds(self, book_id_to_name):
		odds_text = get_text_from_url(self.odds_url)
		soup = BeautifulSoup(odds_text)
		game_soups = soup.odds.league.findAll('game')
		games = []

		for game_soup in game_soups:
			game_time = self._get_gametime_from_game_soup(game_soup)
			teams = []

			for team_soup in game_soup.findAll('team'):
				team = {
					'Opener': team_soup.opener['value'],
					'number': team_soup['number'],
					'name': team_soup['name']
				}
				default_odds = dict((book_name, '') for book_name in book_id_to_name.values())
				team.update(default_odds)
				for odd_soup in team_soup.findAll('line'):
					book_name = book_id_to_name[odd_soup['book']]
					team[book_name] = self._parse_value(odd_soup['value'])
				teams.append(team)

			games.append({'time': game_time, 'teams': teams})
		return games

	def _get_gametime_from_game_soup(self, game_soup):
		game_date_string = game_soup['date']
		game_time_string = game_soup['time']
		game_time = datetime.datetime(
			int(game_date_string[:4]),
			int(game_date_string[4:6]),
			int(game_date_string[6:8]),
			int(game_time_string[:2]),
			int(game_time_string[2:4])
		)
		return game_time

	def _parse_value(self, value_string):
		fraction_keyword = '&frac12;'
		if fraction_keyword in value_string:
			value_string = value_string.rstrip(fraction_keyword)
			value_string += '.5'
		return value_string

