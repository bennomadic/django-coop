# -*- coding:utf-8 -*-
from django.db import models
from django_extensions.db import fields as exfields
from django.utils.translation import ugettext_lazy as _
from extended_choices import Choices

#Based on SKOS+XL model

LABEL_TYPES = Choices(
    ('PREF',    0,  'PrefLabel'),
    ('ALT',     1,  'AltLabel'),
    ('HIDDEN',  2,  'HiddenLabel'),
)

MATCH_TYPES = Choices(
    ('EXACT',   0,  'exactMatch'),
    ('CLOSE',   1,  'closeMatch'),
    ('BROAD',   2,  'broadMatch'),
    ('NARROW',  3,  'narrowMatch'),
    ('RELATED', 4,  'relatedMatch'),    
)

REL_TYPES = Choices(
    ('BROAD',   0,  'broader'),
    ('NARROW',  1,  'narrower'),
    ('RELATED', 2,  'related'),    
)

LANG_LABELS = (
    ('@fr','Français'),
    ('@en','Anglais'),
    ('@es','Espagnol'),
    ('@it','Italien'),
)

# Le terme c'est le "tag" brut
# Le but c'est de pouvoir appeler tag.concept

class Concept(models.Model):
    definition = models.TextField(blank=True)
    changenote = models.TextField(blank=True)
    created = exfields.CreationDateTimeField(_(u'date de création'))
    modified = exfields.ModificationDateTimeField(_(u'date de modification'))
    author = models.CharField(_(u'Auteur'),blank=True, max_length=250, editable=False)
    sem_relations = models.ManyToManyField("self",symmetrical=False,through='SemRelation')

    def __unicode__(self):
        preflabel = Label.objects.filter(type=LABEL_TYPES.PREF,term__language='@fr')[0].term.literal
        return unicode(preflabel)
    

class Term(models.Model):
    literal = models.CharField(_(u'Forme literale'),max_length=255)
    slug = exfields.AutoSlugField(populate_from=('literal'))
    language= models.CharField(_(u'Langue'),max_length=10, choices=LANG_LABELS, default='@fr')
    created = exfields.CreationDateTimeField(_(u'date de création'))
    modified = exfields.ModificationDateTimeField(_(u'Mdate de modification'))
    author = models.CharField(_(u'Auteur'),blank=True, max_length=250, editable=False)
    concept = models.ManyToManyField(Concept,through='Label')
    
    def __unicode__(self):
        return unicode(self.literal)
    #createConcept from Term -> pas automatique , demande une revue
    class Meta: 
        verbose_name = _(u'Terme')

class Vocabulary(models.Model):
    name = models.CharField(max_length=100)
    info_url = models.URLField(blank=True, verify_exists=False)
    class Meta: 
        verbose_name = _(u'Vocabulaire')
    def __unicode__(self):
        return self.name
        
class Label(models.Model):
    term = models.ForeignKey(Term)         
    concept = models.ForeignKey(Concept)
    type = models.PositiveSmallIntegerField( _(u'Type de label'),
                                                    choices=LABEL_TYPES.CHOICES, 
                                                    default=LABEL_TYPES.PREF)
    # a la sauvergarde, verifier qu'il n'y a qu'un preflabel par langue                                      
    class Meta: 
        verbose_name = _(u'Libellé')


class SemRelation(models.Model):
    origin_concept = models.ForeignKey(Concept,related_name='origin')
    target_concept = models.ForeignKey(Concept,related_name='target')
    type = models.PositiveSmallIntegerField( _(u'Type de label'),
                                                    choices=REL_TYPES.CHOICES, 
                                                    default=REL_TYPES.RELATED)
    class Meta: 
        verbose_name = _(u'Relation Sémantique')
        verbose_name_plural = _(u'Relations Sémantiques')
        
        
class SimilarConcept(models.Model):
    similar_to = models.ForeignKey(Concept)
    Preflabel = models.CharField(_(u'Libellé préféré'),max_length=255)
    uri = models.CharField(_(u'Concept URI'), max_length=250)
    voc = models.ForeignKey(Vocabulary)
    match_type = models.PositiveSmallIntegerField( _(u'Type de correspondance'),
                                                    choices=MATCH_TYPES.CHOICES, 
                                                    default=MATCH_TYPES.EXACT)
    class Meta: 
        verbose_name = _(u'Concept similaire')
        verbose_name_plural = _(u'Concepts similaires')
    
