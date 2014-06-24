from django.shortcuts import render
from forms import QueryForm
from models import Query, GBIFResponse
from api_utils import species_search, process_response


def index(request):
	return render(request, 'base.html', {})


def query_form(request):
	form = QueryForm()

	if request.method == 'POST':
		form = QueryForm(request.POST)
		if form.is_valid():
			term = form.cleaned_data['term']
			query, created = Query.objects.get_or_create(term=term)
			if not created:  # Increment the access counter if this is a pre existing query
				query.times_accessed += 1
				query.save()
			query.kingdom = form.cleaned_data['kingdom']
			search_request = species_search(query.term, query.kingdom)

			if search_request[0] == 200: # everything was OK
				try:
					note = search_request[1]['note']
				except KeyError:
					note = None

				gbif_response = GBIFResponse(query=query, status=search_request[0], text=search_request[1], note=note)

				results = process_response(gbif_response)
				print results

			elif search_request[0] == 'Timeout':
				results = 'Timeout'

			else:
				results = None

			return render(request, 'query_form.html', {'query_form': form, 'query': query, 'results': results})


	return render(request, 'query_form.html', {'query_form': form})
