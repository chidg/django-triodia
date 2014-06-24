from django.test import TestCase
from taxon_checker.models import Query, GBIFResponse
from taxon_checker.api_utils import species_search, process_response


class GBIFNameQueryTest(TestCase):
	
	valid_names = {'matchtype': 'exact', 'names': ['Acacia acuminata', 'Eucalyptus marginata', 'Baeckea crispiflora', 'Thryptomene decussata', 'Hemigenia sericea', 'Ptilotus obovatus']}
	mispelled_names = {'matchtype': 'fuzzy', 'names': ['Ecualyptus marginata', 'Acacia acminata'] }
	names = [valid_names, mispelled_names]


	def setUp(self):
		for name_types in self.names:
			for namex in name_types['names']:
				Query.objects.create(term=namex)


	def testNames(self, kingdom=None):
		for q in Query.objects.all():
			search_request = species_search(q.term, kingdom)
			if search_request[0] == 200: # everything was OK
				try:
					note = search_request[1]['note']
				except KeyError:
					note = None

				gbif_response = GBIFResponse(query=q, status=search_request[0], text=search_request[1], note=note)
				results = process_response(gbif_response)

				matchtype = None

				for value in self.names:
					if q.term in value['names']:
						matchtype = value['matchtype']
						self.assertEqual(results[0].matchtype, matchtype)
