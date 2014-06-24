from django.db import models
from jsonfield import JSONField


# Create your models here.

class Query(models.Model):

    """Represents a search term"""

    KINGDOM_CHOICES = (
        ('All', 'Search all kingdoms'),
        ('Animalia', 'Animals'),
        ('Fungi', 'Fungi'),
        ('Plantae', 'Plants'),
    )

    term = models.CharField(
        max_length=60, help_text='The taxonomic name you are querying.')
    kingdom = models.CharField(
        max_length=8, choices=KINGDOM_CHOICES,
        help_text='Choose a taxonomic kingdom if you wish to limit the search results.',
        default='All', null=True)
    last_query_date = models.DateTimeField(auto_now_add=True)
    times_accessed = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return self.term


class GBIFResponse(models.Model):

    """ Represents a response returned from the requests module htttp request to the species match API """

    query = models.ForeignKey('Query', related_name='gbif_response')
    status = models.PositiveSmallIntegerField(max_length=3)
    text = JSONField(max_length=20000, null=True)
    note = models.CharField(max_length=200, null=True)
    time = models.DateTimeField(auto_now=True)
    #best_result = models.ForeignKey('Taxon', related_name='responses', null=True)

    def __unicode__(self):
        return '%s, made at %s' % (self.status, self.time)


class Taxon(models.Model):

    """
        Represents the basic details of a taxon returned via the Query class,
        which can be queried further using the key field in the GBIF API
    """

    name = models.CharField(max_length=200)
    key = models.PositiveIntegerField(max_length=20)
    kingdom = models.CharField(max_length=20)
    rank = models.CharField(max_length=12)

    def __unicode__(self):
        return '%s, %s' % (self.name, self.kingdom)


class Match(models.Model):

    """
        A through class enabling addition of a confidence ranking and match type
        to the relationship between GBIFResponse and Taxon objects
    """
    MATCH_CHOICES = (
        ('exact', 'Exact'),
        ('fuzzy', 'Fuzzy'),
        ('multiple', 'Multiple'),
        ('synonym', 'Synonym'),
        ('other', 'Other'),
        ('alternative', 'Alternative'),
        (None, 'None')
    )

    response = models.ForeignKey('GBIFResponse', related_name='matches')
    taxon = models.ForeignKey('Taxon', related_name='matches')
    matchtype = models.CharField(max_length=12, choices=MATCH_CHOICES)
    confidence = models.PositiveSmallIntegerField(max_length=3)

    def __unicode__(self):
        return '%s with %s confidence: %s' % (self.matchtype, self.confidence, self.taxon)
