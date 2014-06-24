========
Triodia
========

Triodia is a Django app for parsing taxonomic names and checking them against the databases of public biodiversity data services. Triodia currently relies on the Global Biodiversity Invormation Facility (GBIF) for its primary API calls and can be considered a partial and incomplete Django/Python wrapper for that API.

Users enter a species name into a form; Triodia queries the GBIF API, parses the results, and returns a list of potential matches, ranked by confidence.


Quick start
-----------

1. Add "triodia" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'triodia',
      )

2. Include the triodia URLconf in your project urls.py like this::

      url(r'^triodia/', include('triodia.urls')),

3. Run `python manage.py syncdb` to create the triodia models.

4. Visit http://127.0.0.1:8000/triodia/ to check a species name.
