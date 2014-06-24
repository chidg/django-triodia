import requests
from requests.exceptions import Timeout
from models import Query, Taxon, GBIFResponse, Match


def species_search(name, kingdom=None):
		""" Searches the GBIF name matching API for the name and returns the result in json format if successful """
		confidence = 99
		payload = {'verbose':'true', 'name': name}
		if kingdom is not None:  # Add the kingdom to the payload if it was selected, otherwise leave blank
			payload['kingdom'] = kingdom

		try:
			r = requests.get('http://api.gbif.org/v0.9/species/match', params=payload, timeout=2)
			text = r.json()
			return [r.status_code, text]
		except Timeout:
			print 'something timedout'
			return ['Timeout']
		except Exception, e:
			print 'exception...'
			print e

			return ['Exception on request: %s' % e]

def process_response(gbif_response):
	""" Processes the results of the species_search method and produces and saves the other classes from it """
	text = gbif_response.text
	print 'in process gbif_response'
	try:
		if text['matchType'] == 'EXACT':  # We have an exact match. Good work.
			matchtype = 'exact'

		elif text['matchType'] == 'FUZZY': # We have a fuzzy match. Almost as good
			if ' sp. ' in gbif_response.query.term:  # Indicates a phrase name, which is not searchable by the GBIF or ALA
				print 'this is a phrase name'
				return "Phrasename"
			else:
				matchtype = 'fuzzy'

		elif text['matchType'] == 'NONE': # No match, that indicates there was no match or multiple equally good matches.
			try:
				if 'Multiple equal matches for' in gbif_response.note:
					matchtype = 'multiple'
				else:
					matchtype = None
			except TypeError:
				matchtype = None

			if ' sp. ' in gbif_response.query.term:  # Indicates a phrase name, which is not searchable by the GBIF or ALA
				print 'this is a phrase name'
				return "Phrasename"

		else:
			matchtype = 'other'

		if matchtype == 'exact' or matchtype == 'fuzzy':
			name = text['canonicalName']

			# Test if name has changed
			if text['synonym'] == True:
				if text['rank'] == 'SPECIES' and text['canonicalName'] != text['species']:
					name = text['species']
					matchtype = 'synonym'

			taxon = Taxon(name=name, rank=text['rank'], key=text['usageKey'], kingdom=text['kingdom'])
			match = Match(taxon=taxon, response=gbif_response, confidence=text['confidence'], matchtype=matchtype)
			matches = [match]
		else:
			matches = []

		try:
			for alt in text['alternatives']:
				matches.append(process_alternatives(alt, gbif_response))

		except KeyError:
			# No alternatives, no problem
			pass
		print matchtype
		return matches

	except KeyError:  # No matchType key present, that probably indicates there was a problem
		print 'none'
		return None



def process_alternatives(alt, gbif_response):
	""" Processes the alternative taxa in a dictionary representing an alternative. """

	taxon = Taxon(name=alt['canonicalName'], rank=alt['rank'], key=alt['usageKey'], kingdom=alt['kingdom'])
	match = Match(taxon=taxon, response=gbif_response, confidence=alt['confidence'], matchtype='alternative')
	return match
