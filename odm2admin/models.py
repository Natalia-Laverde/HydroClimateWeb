import io
import re
import uuid
import csv
import time
import HydroClimateWeb.settings as settings

from django.db import models
from urllib.parse import urlparse
from django.core import management
from django.core.exceptions import ValidationError


# ======================================================================================================================
# Auxiliary functions
# ======================================================================================================================
def build_citation(s, self):
    result = None
    if hasattr(self.resultId, 'resultId'):
        result = self.resultid.resultid
    else:
        result = Results.objects.get(resultId=self.resultId)
    dataset_results = DatasetsResults.objects.filter(resultId=result)
    ds_citations = DatasetCitations.objects.filter(datasetid__in=dataset_results.values("datasetId"))
    citations = Citations.objects.filter(citationid__in=ds_citations.values("citationId"))

    author_count = 0
    if citations.count() == 0:
        s += ','
        return s
    for citation in citations:
        cited_authors = AuthorLists.objects.filter(citationId=citation.citationId).order_by("authorOrder")
        cited_persons = People.objects.filter(personId__in=cited_authors.values("personId"))
        for cited_author in cited_authors:
            for author in cited_persons:
                if cited_author.personId.personId == author.personId:
                    if author_count == 0:
                        s += ',\" {0}'.format(author.personLastName)
                    else:
                        s += ' {0}'.format(author.personLastName)

                    author_count += 1
                    if author_count == cited_persons.count():
                        s += ' {0}.'.format(author.personFirstName)
                    else:
                        s += ' {0},'.format(author.personFirstName)
        s += ' {0}'.format(citation.title)
        s += '. {0}'.format(citation.publisher)
        s += ', {0}'.format(citation.publicationyear)
        s += ' DOI: {0}\"'.format(citation.citationlink)  # doesn't work not sure why
    return s


def handle_uploaded_file(f, Id):
    destination = io.open(settings.MEDIA_ROOT + '/resultValues/' + f.name + '.csv', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

    destination.close()
    try:
        with io.open(settings.MEDIA_ROOT + '/resultValues/' + f.name + '.csv', 'rt', encoding='ascii') as f:
            reader = csv.reader(f)
            for row in reader:
                date_t = time.strptime(row[0], "%m/%d/%Y %H:%M")  # '1/1/2013 0:10
                date_str = time.strftime("%Y-%m-%d %H:%M", date_t)
                MeasurementResultValues(resultid=id, datavalue=row[1], valuedatetime=date_str,
                                        valuedatetimeutcoffset=4).save()
    except IndexError:
        raise ValidationError('encountered a problem with row ' + row)


# ======================================================================================================================
# Controlled Vocabularies
# ======================================================================================================================
class CvActionType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvActionType'
        ordering = ['term', 'name']


class CvAggregationStatistic(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvAggregationStatistic'
        ordering = ['term', 'name']


class CvAnnotationType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvAnnotationType'
        ordering = ['term', 'name']


class CvCensorCode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvCensorCode'
        ordering = ['term', 'name']


class CvDataQualityType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvDataQualityType'
        ordering = ['term', 'name']


class CvDatasetTypeCV(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvDatasetTypeCV'
        ordering = ['term', 'name']


class CvDirectiveType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvDirectiveType'
        ordering = ['term', 'name']


class CvElevationDatum(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvElevationDatum'
        verbose_name = 'elevation datum'
        ordering = ['term', 'name']


class CvEquipmentType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvEquipmentType'
        ordering = ['term', 'name']


class CvMethodType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvMethodType'
        ordering = ['term', 'name']


class CvOrganizationType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvOrganizationType'
        ordering = ['term', 'name']


class CvPropertyDataType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvPropertyDataType'
        ordering = ['term', 'name']


class CvQualityCode(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvQualityCode'
        ordering = ['term', 'name']


class CvReferenceMaterialMedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvReferenceMaterialMedium'
        ordering = ['term', 'name']


class CvRelationshipType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvRelationshipType'
        ordering = ['term', 'name']


class CvResultType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'CvResultType'
        ordering = ['term', 'name']


class CvMedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvMedium'
        ordering = ['term', 'name']


class CvSamplingFeatureGeoType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvSamplingFeatureGeoType'
        verbose_name = 'sampling feature geo type'
        ordering = ['term', 'name']


class CvSamplingFeatureType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvSamplingFeatureType'
        verbose_name = 'sampling feature type'
        ordering = ['term', 'name']


class CvSiteType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvSiteType'
        ordering = ['term', 'name']


class CvSpatialOffsetType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvSpatialOffsetType'
        ordering = ['term', 'name']


class CvSpeciation(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvSpeciation'
        ordering = ['term', 'name']


class CvSpecimenMedium(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvMedium'
        ordering = ['term', 'name']


class CvSpecimenType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvSpecimenType'
        ordering = ['term', 'name']


class CvStatus(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvStatus'
        ordering = ['term', 'name']


class CvTaxonomicClassifierType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvTaxonomicClassifierType'
        ordering = ['term', 'name']
        verbose_name = "taxonomic classifier"


class CvUnitsType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvUnitsType'
        ordering = ['term', 'name']


class CvVariableName(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        managed = True
        db_table = 'ODM2.CvVariableName'
        ordering = ['term', 'name']


class CvVariableType(models.Model):
    term = models.CharField(max_length=255)
    name = models.CharField(primary_key=True, max_length=255)
    definition = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    sourceVocabularyURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2.CvVariableType'
        ordering = ['term', 'name']


# ======================================================================================================================
# Action annotation table
# ======================================================================================================================
class ActionAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey('Actions', db_column='actionId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey('Annotations', db_column='annotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.ActionAnnotations'


# ======================================================================================================================
# Action by table
# ======================================================================================================================
class ActionBy(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey('Actions', verbose_name="action", db_column='actionId', on_delete=models.CASCADE)
    affiliationId = models.ForeignKey('Affiliations', verbose_name="person by affiliation",
                                      db_column='affiliationId', on_delete=models.CASCADE)
    isActionLead = models.BooleanField(verbose_name="is lead person on action")
    roleDescription = models.CharField(max_length=5000, verbose_name="person's role on this action",
                                       blank=True)

    def __str__(self):
        s = u"%s" % self.actionId
        if self.affiliationId:
            s += u"- %s" % self.affiliationId
        if self.roleDescription:
            s += u"- %s" % self.roleDescription
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.ActionBy'
        verbose_name = 'action by'
        verbose_name_plural = 'action by'


# ======================================================================================================================
# Action directives table
# ======================================================================================================================
class ActionDirectives(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey('Actions', db_column='actionId', on_delete=models.CASCADE)
    directiveId = models.ForeignKey('Directives', db_column='directiveId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.ActionDirectives'


# ======================================================================================================================
# Action directives table
# ======================================================================================================================
class ActionExtensionPropertyValues(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey('Actions', db_column='actionId', on_delete=models.CASCADE)
    propertyId = models.ForeignKey('ExtensionProperties', db_column='propertyId', on_delete=models.CASCADE)
    propertyValue = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'ODM2.ActionExtensionPropertyValues'


# ======================================================================================================================
# Actions table
# ======================================================================================================================
class Actions(models.Model):
    actionId = models.AutoField(primary_key=True)
    actionType = models.ForeignKey('CvActionType',
                                   help_text='A vocabulary for describing the type of actions performed in making '
                                             'observations. Depending on the action type, the action may or may not '
                                             'produce an observation result. view action type details here '
                                             'http://vocabulary.odm2.org/actiontype/',
                                   db_column='actionTypeCV', on_delete=models.CASCADE)
    method = models.ForeignKey('Methods', db_column='methodId', on_delete=models.CASCADE)
    beginDateTime = models.DateTimeField(verbose_name='begin date time')
    beginDateTimeUtcOffset = models.IntegerField(verbose_name='begin date time clock off set (from GMT)', default=4)
    endDateTime = models.DateTimeField(verbose_name='end date time', blank=True, null=True)
    endDateTimeUtcOffset = models.IntegerField(verbose_name='end date time clock off set (from GMT)', default=4)
    actionDescription = models.CharField(verbose_name='action description', max_length=5000, blank=True)
    actionFileLink = models.CharField(verbose_name='action file link', max_length=255, blank=True)

    def __str__(self):
        s = u"%s" % self.actionType
        if self.method:
            s += u" | %s" % self.method
        if self.method:
            s += u" | %s" % (self.actionDescription[:25])
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Actions'
        verbose_name = 'action'


# ======================================================================================================================
# Affiliations table
# ======================================================================================================================
class Affiliations(models.Model):
    affiliationId = models.AutoField(primary_key=True)
    personId = models.ForeignKey('People', verbose_name='person', db_column='personId', on_delete=models.CASCADE)
    organizationId = models.ForeignKey('Organizations', verbose_name='organization', db_column='organizationId',
                                       blank=True, null=True, on_delete=models.CASCADE)
    isPrimaryOrganizationContact = models.NullBooleanField(verbose_name='primary organization contact? ')
    affiliationStartDate = models.DateField(verbose_name="When affiliation began ")
    affiliationEndDate = models.DateField(verbose_name="When affiliation ended", blank=True, null=True)
    primaryPhone = models.CharField(verbose_name="primary phone", max_length=50, blank=True)
    primaryEmail = models.CharField(verbose_name="primary email", max_length=255)
    primaryAddress = models.CharField(verbose_name="primary address", max_length=255, blank=True)
    personLink = models.CharField(max_length=255, blank=True)

    def __str__(self):
        s = u"%s" % self.personId
        if self.organizationId:
            s += u" | %s" % self.organizationId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Affiliations'
        verbose_name = 'affiliation (relate people and organizations)'
        verbose_name_plural = 'affiliation (relate people and organizations)'
        ordering = ['-primaryEmail']


# ======================================================================================================================
# Annotations table
# ======================================================================================================================
class Annotations(models.Model):
    annotationId = models.AutoField(primary_key=True)
    annotationTypeCV = models.ForeignKey('CvAnnotationType', db_column='annotationTypeCV', on_delete=models.CASCADE)
    annotationCode = models.CharField(max_length=50, blank=True)
    annotationText = models.CharField(max_length=500)
    annotationDateTime = models.DateTimeField(blank=True, null=True)
    annotationUtcOffset = models.IntegerField(blank=True, null=True)
    annotationLink = models.CharField(max_length=255, blank=True)
    annotatorId = models.ForeignKey('People', db_column='annotatorId', blank=True, null=True,
                                    on_delete=models.CASCADE)
    citationId = models.ForeignKey('Citations', db_column='citationId', blank=True, null=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        s = u" %s" % self.annotationText
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Annotations'


# ======================================================================================================================
# Author lists table
# ======================================================================================================================
class AuthorLists(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    citationId = models.ForeignKey('Citations', verbose_name='citation', db_column='citationId',
                                   on_delete=models.CASCADE)
    personId = models.ForeignKey('People', verbose_name='person', db_column='personId', blank=True,
                                 null=True, on_delete=models.CASCADE)
    authorOrder = models.IntegerField(verbose_name='author order', blank=True, null=True)

    def __str__(self):
        s = u"{0} - {1}".format(self.personId, self.authorOrder)
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.AuthorLists'
        verbose_name = 'author list'
        verbose_name_plural = 'author list'

    def csv_header(self):
        s = 'Author ' + str(self.authorOrder) + ','
        return s

    def csv_output(self):
        s = '"' + str(self.personId.personLastName) + ', ' + str(
            self.personId.personFirstName) + ', ' + str(
            self.personId.personMiddleName) + '",'
        return s

    def end_note_export(self):
        s = 'AU  - ' + str(self.personId.personLastName) + "," + str(
            self.personId.personFirstName) + ', ' + str(
            self.personId.personMiddleName) + '\r\n'
        return s


# ======================================================================================================================
# Calibration actions table
# ======================================================================================================================
class CalibrationActions(models.Model):
    actionId = models.OneToOneField(Actions, db_column='actionId', primary_key=True, on_delete=models.CASCADE)
    calibrationCheckValue = models.FloatField(blank=True, null=True)
    instrumentOutputVariableId = models.ForeignKey('InstrumentOutputVariables', db_column='instrumentOutputVariableId',
                                                   on_delete=models.CASCADE)
    calibrationEquation = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.CalibrationActions'


# ======================================================================================================================
# Calibration reference equipment table
# ======================================================================================================================
class CalibrationReferenceEquipment(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey(CalibrationActions, db_column='actionId', on_delete=models.CASCADE)
    equipmentId = models.ForeignKey('Equipment', db_column='equipmentId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.CalibrationReferenceEquipment'


# ======================================================================================================================
# Calibration standards table
# ======================================================================================================================
class CalibrationStandards(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey(CalibrationActions, db_column='actionId', on_delete=models.CASCADE)
    referenceMaterialId = models.ForeignKey('ReferenceMaterials', db_column='referenceMaterialId',
                                            on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.CalibrationStandards'


# ======================================================================================================================
# Categorical results table
# ======================================================================================================================
class CategoricalResults(models.Model):
    resultId = models.OneToOneField('Results', db_column='resultId', primary_key=True, on_delete=models.CASCADE)
    xLocation = models.FloatField(blank=True, null=True)
    xLocationUnitsId = models.IntegerField(blank=True, null=True)
    yLocation = models.FloatField(blank=True, null=True)
    yLocationUnitsId = models.IntegerField(blank=True, null=True)
    zLocation = models.FloatField(blank=True, null=True)
    zLocationUnitsId = models.IntegerField(blank=True, null=True)
    spatialReferenceId = models.ForeignKey('SpatialReferences', db_column='spatialReferenceId', blank=True, null=True,
                                           on_delete=models.CASCADE)
    qualityCodeCV = models.ForeignKey('CvQualityCode', db_column='qualityCodeCV', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.CategoricalResults'


# ======================================================================================================================
# Categorical results value annotations table
# ======================================================================================================================
class CategoricalResultValueAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    valueId = models.ForeignKey('CategoricalResultValues', db_column='valueId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.CategoricalResultValueAnnotations'


# ======================================================================================================================
# Categorical results value table
# ======================================================================================================================
class CategoricalResultValues(models.Model):
    valueId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey(CategoricalResults, db_column='resultId',
                                 on_delete=models.CASCADE)
    dataValue = models.CharField(max_length=255)
    valueDatetime = models.DateTimeField()
    valueDatetimeUtcOffset = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'ODM2.CategoricalResultValues'


# ======================================================================================================================
# Citation extension property values results value table
# ======================================================================================================================
class CitationExtensionPropertyValues(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    citationId = models.ForeignKey('Citations', db_column='citationId', on_delete=models.CASCADE)
    propertyId = models.ForeignKey('ExtensionProperties', db_column='propertyId', on_delete=models.CASCADE)
    propertyValue = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        s = u"%s - %s - %s" % (self.citationId, self.propertyId, self.propertyValue)
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.CitationExtensionPropertyValues'
        verbose_name = 'citation extension property'
        verbose_name_plural = 'citation extension properties'

    def csv_header(self):
        s = '"' + str(self.propertyId) + '",'
        return s

    def csv_output(self):
        s = '"' + str(self.propertyValue) + '",'
        return s

    def pub_type(self):
        p_type = None
        if str(self.propertyValue).__len__() > 0:
            if str(
                    self.propertyId) == 'Citation Category - Paper, Book, Talk, Poster, ' \
                                        'Dissertation, Thesis, Undergrad Thesis, Report':
                if str(self.propertyValue) == 'Paper':
                    p_type = "Paper"
                if str(self.propertyValue) == 'Book':
                    p_type = "Book"
                if str(self.propertyValue) == 'Talk':
                    p_type = "Conference"
                if str(self.propertyValue) == 'Poster':
                    p_type = "Poster"
                if str(self.propertyValue) == 'Dissertation' or str(
                        self.propertyValue) == 'Thesis' or str(self.propertyValue) == 'Undergrad Thesis':
                    p_type = "Thesis"
                if str(self.propertyValue) == 'Report':
                    p_type = "Report"
        return p_type

    def end_note_export(self):
        s = ''
        if str(self.propertyValue).__len__() > 0:
            if str(
                    self.propertyId) == 'Citation Category - Paper, Book, Talk, Poster, ' \
                                        'Dissertation, Thesis, Undergrad Thesis, Report':
                s += 'TY  - '
                if str(self.propertyValue) == 'Paper':
                    s += 'JOUR' + '\r\n'
                if str(self.propertyValue) == 'Book':
                    s += 'BOOK' + '\r\n'
                if str(self.propertyValue) == 'Talk':
                    s += 'CONF' + '\r\n'
                if str(self.propertyValue) == 'Poster':
                    s += 'ABST' + '\r\n'
                if str(self.propertyValue) == 'Dissertation' or str(
                        self.propertyValue) == 'Thesis' or str(self.propertyValue) == 'Undergrad Thesis':
                    s += 'THES' + '\r\n'
                if str(self.propertyValue) == 'Report':
                    s += 'RPRT' + '\r\n'
            s += 'N1  - ' + str(self.propertyId) + ': ' + str(self.propertyValue) + '\r\n'
        else:
            s = ''
        return s


# ======================================================================================================================
# Citation external identifiers table
# ======================================================================================================================
class CitationExternalIdentifiers(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    citationId = models.ForeignKey('Citations', db_column='citationId', on_delete=models.CASCADE)
    externalIdentifierSystemId = models.ForeignKey('ExternalIdentifierSystems', db_column='externalIdentifierSystemId',
                                                   on_delete=models.CASCADE)
    citationExternalIdentifier = models.CharField(max_length=255, db_column="citationExternalIdentifier")
    citationExternalIdentifierURI = models.CharField(max_length=255, blank=True,
                                                     db_column="citationExternalIdentifierURI")

    def __str__(self):
        s = u"{0} - {1}".format(self.externalIdentifierSystemId, self.citationExternalIdentifier)
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.CitationExternalIdentifiers'
        verbose_name = 'citationExternalIdentifier'


# ======================================================================================================================
# Citations table
# ======================================================================================================================
class Citations(models.Model):
    citationId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publicationYear = models.IntegerField(verbose_name='year')
    citationLink = models.CharField(max_length=255, blank=True, verbose_name='Citation Link', )

    def __str__(self):
        s = u"%s" % self.title
        if self.publisher:
            s += u"- %s," % self.publisher
        if self.publicationYear:
            s += u", %s," % self.publicationYear
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Citations'
        ordering = ['title']
        verbose_name = 'citation'

    @staticmethod
    def csv_header():
        s = 'citationId,title,publisher,year,citationLink,'
        return s

    def csv_output(self):
        s = str(self.citationId)
        s += ',"{0}"'.format(self.title)
        s += ',"{0}"'.format(self.publisher)
        s += ', {0}'.format(self.publicationYear)
        s += ', {0},'.format(self.citationLink)
        return s

    @staticmethod
    def end_note_export_header():
        s = 'TI\tPB\tPY\tcitationLink\t'
        return s

    def end_note_export(self):
        property_values = CitationExtensionPropertyValues.objects.filter(citationid=self.citationId)
        pub_type = None
        for propertyValue in property_values:
            if propertyValue.pubType():
                pub_type = propertyValue.pubType()
        if not pub_type:  # "Conference""Poster""Thesis""Report"
            pub_type = "Unknown"
        s = 'TI  - {0}\r\n'.format(self.title)
        if pub_type == "Paper":
            s += 'JO  - {0}\r\n'.format(self.publisher)
        else:
            s += 'PB  - {0}\r\n'.format(self.publisher)
        s += 'PY  - {0}\r\n'.format(self.publicationYear)
        s += 'DI  - {0}\r\n'.format(self.citationLink)
        return s


# ======================================================================================================================
# Data logger file columns table
# ======================================================================================================================
class DataLoggerFileColumns(models.Model):
    dataLoggerFileColumnId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey('Results', verbose_name="result", db_column='resultId', blank=True, null=True,
                                 on_delete=models.CASCADE)
    dataLoggerFileId = models.ForeignKey('DataLoggerFiles', verbose_name="data logger file",
                                         db_column='dataLoggerFileId', on_delete=models.CASCADE)
    instrumentOutputVariableId = models.ForeignKey('InstrumentOutputVariables',
                                                   verbose_name="instrument output variable",
                                                   db_column='instrumentOutputVariableId', on_delete=models.CASCADE)
    columnLabel = models.CharField(verbose_name="column label", max_length=50)
    columnDescription = models.CharField(verbose_name="column description",
                                         help_text="To disble ingestion of a column type skip, " +
                                                   "or to specify a column as the date time enter datetime" +
                                                   " if the datetime is an excel format numeric datetime" +
                                                   " enter exceldatetime",
                                         max_length=5000,
                                         blank=True)
    measurementEquation = models.CharField(verbose_name="measurement equation", max_length=255,
                                           blank=True)
    scanInterval = models.FloatField(verbose_name="scan interval (time)", blank=True, null=True)
    scanIntervalUnitsId = models.ForeignKey('Units', verbose_name="scan interval units",
                                            related_name='relatedScanIntervalUnitsId',
                                            db_column='scanIntervalUnitsId',
                                            blank=True, null=True,
                                            on_delete=models.CASCADE)
    recordingInterval = models.FloatField(verbose_name="recording interval", blank=True, null=True)
    recordingIntervalUnitsId = models.ForeignKey('Units', verbose_name="recording interval units",
                                                 related_name='relatedRecordingIntervalUnitsId',
                                                 db_column='recordingIntervalUnitsId', blank=True,
                                                 null=True,
                                                 on_delete=models.CASCADE)
    aggregationStatisticCV = models.ForeignKey(CvAggregationStatistic,
                                               verbose_name="aggregation statistic",
                                               db_column='aggregationStatisticCV', blank=True,
                                               null=True,
                                               on_delete=models.CASCADE)

    def __str__(self):
        s = u"Label: %s," % self.columnLabel
        # s += u" Description: %s," % (self.columndescription)
        s += u" Result: %s" % self.resultId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.DataLoggerFileColumns'
        verbose_name = 'data logger file column'


# ======================================================================================================================
# Data logger files table
# ======================================================================================================================
class DataLoggerFiles(models.Model):
    dataLoggerFileId = models.AutoField(primary_key=True)
    programId = models.ForeignKey('DataLoggerProgramFiles', db_column='programId', on_delete=models.CASCADE)
    dataLoggerFileName = models.CharField(max_length=255, verbose_name="Data logger file name")
    dataLoggerFileDescription = models.CharField(max_length=5000, blank=True,
                                                 verbose_name="Data logger file description")
    dataLoggerFileLink = models.FileField(upload_to='dataLoggerFiles', verbose_name="Data logger file")  # upload_to='.'

    def data_logger_file_link_name(self):
        return self.dataLoggerFileLink.name

    def __str__(self):
        s = u"%s" % self.dataLoggerFileName
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.DataLoggerFiles'
        verbose_name = 'data logger file'


# ======================================================================================================================
# Process data logger file table
# ======================================================================================================================
class ProcessDataLoggerFile(models.Model):
    processDataLoggerFileId = models.AutoField(primary_key=True)
    dataLoggerFileId = models.ForeignKey(DataLoggerFiles,
                                         help_text="CAUTION data logger file columns must be setup" +
                                                   ", the date and time stamp is expected to " +
                                                   "be the first column, " + " column names must match " +
                                                   "the column name in associated " + "dataLoggerFileColumns.",
                                         verbose_name='data logger file', db_column='dataLoggerFileId',
                                         on_delete=models.CASCADE)
    processingCode = models.CharField(max_length=255, verbose_name='processing code',
                                      help_text="to setup an FTP file download set the processing" +
                                      "code as 'x hours between download' where x is how many hours to " +
                                      "wait between downloading copies of the file from the FTP site. " +
                                      "A data logger file setup for FTP download must have only 1 " +
                                      "process data logger file record.", default="0")
    dataBeginsOn = models.IntegerField(verbose_name="Data begins on this row number", default=2)
    columnHeadersOn = models.IntegerField(
        verbose_name="Column headers matching column labels from data logger columns on row")
    dateProcessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        s = u"%s" % self.dataLoggerFileId
        s += u"- Processed on %s" % self.dateProcessed
        return s

    class Meta:
        managed = True
        db_table = 'ODM2EXTRA.ProcessDataLoggerFile'
        verbose_name = 'process data logger file'

    def save(self, *args, **kwargs):
        link_name = str(self.dataLoggerFileId.dataLoggerFileLink.name)
        file_id = self.dataLoggerFileId.dataLoggerFileId
        ftp_file = self.dataLoggerFileId.dataLoggerFileDescription
        ftp_parse = urlparse(ftp_file)
        if len(ftp_parse.netloc) > 0:
            ftp_frequency_hours = re.findall(r'^\D*(\d+)', self.processingCode)[0]
            management.call_command('update_preprocess_process_datalogger_file', link_name, str(file_id),
                                    str(self.dataBeginsOn), str(self.columnHeadersOn),
                                    str(ftp_frequency_hours), False)
        else:
            management.call_command('ProcessDataLoggerFile', link_name, str(file_id),
                                    str(self.dataBeginsOn), str(self.columnHeadersOn),
                                    False, False, False)
        super(ProcessDataLoggerFile, self).save(*args, **kwargs)


# ======================================================================================================================
# Data logger program files table
# ======================================================================================================================
class DataLoggerProgramFiles(models.Model):
    programId = models.AutoField(primary_key=True)
    affiliationId = models.ForeignKey(Affiliations, db_column='affiliationId', on_delete=models.CASCADE)
    programName = models.CharField(max_length=255)
    programDescription = models.CharField(max_length=5000, blank=True)
    programVersion = models.CharField(max_length=50, blank=True)
    programFileLink = models.FileField(upload_to='dataLoggerProgramFiles')

    # + '/' + programname.__str__() settings.settings.MEDIA_ROOT upload_to='/upfiles/'

    def __str__(self):
        s = u"%s" % self.programName
        s += u"- Version %s" % self.programVersion
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.DataLoggerProgramFiles'
        verbose_name = 'data logger program file'


# ======================================================================================================================
# Data quality table
# ======================================================================================================================
class DataQuality(models.Model):
    dataQualityId = models.AutoField(primary_key=True)
    dataQualityTypeCV = models.ForeignKey(CvDataQualityType, db_column='dataQualityTypeCV',
                                          verbose_name="data quality type", on_delete=models.CASCADE)
    dataQualityCode = models.CharField(max_length=255, verbose_name="data quality code",
                                       help_text="for an alarm test include the word alarm." +
                                                 " for a hard bounds check include the word bound (if a value" +
                                                 " falls below a lower limit, or exceeds a lower limit the " +
                                                 "value will be set to NaN (not a number). ")
    dataQualityValue = models.FloatField(blank=True, null=True, verbose_name="data quality value")
    dataQualityValueUnitsId = models.ForeignKey('Units', related_name='+',
                                                db_column='dataQualityValueUnitsId',
                                                verbose_name="data quality value units", blank=True, null=True,
                                                on_delete=models.CASCADE)
    dataQualityDescription = models.CharField(max_length=5000, blank=True, verbose_name="data quality description")
    dataQualityLink = models.CharField(max_length=255, blank=True, verbose_name="data quality link")

    def __str__(self):
        return u"%s - %s - %s" % (
            self.dataQualityCode, self.dataQualityValue, self.dataQualityValueUnitsId)

    class Meta:
        managed = True
        db_table = 'ODM2.DataQuality'
        verbose_name = 'data quality'
        verbose_name_plural = 'data quality'


# ======================================================================================================================
# Dataset citations table
# ======================================================================================================================
class DatasetCitations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    datasetId = models.ForeignKey('Datasets', verbose_name='dataset', db_column='datasetId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, verbose_name='relationship type',
                                           db_column='relationshipTypeCV', on_delete=models.CASCADE)
    citationId = models.ForeignKey(Citations, db_column='citationId', verbose_name='citation', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.DatasetCitations'
        verbose_name = 'dataset citation'


# ======================================================================================================================
# Datasets table
# ======================================================================================================================
class Datasets(models.Model):
    datasetId = models.AutoField(primary_key=True)
    datasetUUID = models.UUIDField(default=uuid.uuid4, editable=False)
    datasetTypeCV = models.ForeignKey(CvDatasetTypeCV, verbose_name="dataset type",
                                      db_column='datasetTypeCV', on_delete=models.CASCADE)
    datasetCode = models.CharField(verbose_name="dataset code", max_length=50)
    datasetTitle = models.CharField(verbose_name="dataset title", max_length=255)
    datasetAbstract = models.CharField(verbose_name="dataset abstract", max_length=5000)

    def __str__(self):
        s = u"%s" % self.datasetCode
        if self.datasetTitle:
            s += u"- %s" % self.datasetTitle
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Datasets'
        verbose_name = 'dataset'


# ======================================================================================================================
# Dataset results table
# ======================================================================================================================
class DatasetsResults(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    datasetId = models.ForeignKey(Datasets, verbose_name="dataset", db_column='datasetId', on_delete=models.CASCADE)
    resultId = models.ForeignKey('Results', verbose_name="add the dataset to the result", db_column='resultId',
                                 on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s" % self.datasetId
        if self.resultId:
            s += u"- %s" % self.resultId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.DatasetsResults'
        verbose_name = 'dataset result'


# ======================================================================================================================
# Derivation equations table
# ======================================================================================================================
class DerivationEquations(models.Model):
    derivationEquationId = models.AutoField(primary_key=True)
    derivationEquation = models.CharField(max_length=255, verbose_name='derivation equation')

    def __str__(self):
        s = u"%s" % self.derivationEquation
        return s

    class Meta:
        managed = True
        db_table = r'ODM2.DerivationEquations'
        verbose_name = 'derivation equation'


# ======================================================================================================================
# Directives table
# ======================================================================================================================
class Directives(models.Model):
    directiveId = models.AutoField(primary_key=True)
    directiveTypeCV = models.ForeignKey(CvDirectiveType, db_column='directiveTypeCV',
                                        on_delete=models.CASCADE)
    directiveDescription = models.CharField(max_length=500)

    class Meta:
        managed = True
        db_table = 'ODM2.Directives'


# ======================================================================================================================
# Equipment table
# ======================================================================================================================
class Equipment(models.Model):
    equipmentId = models.AutoField(primary_key=True)
    equipmentCode = models.CharField(max_length=50)
    equipmentName = models.CharField(max_length=255)
    equipmentTypeCV = models.ForeignKey(CvEquipmentType, db_column='equipmentTypeCV', on_delete=models.CASCADE)
    equipmentModelId = models.ForeignKey('EquipmentModels', db_column='equipmentModelId', on_delete=models.CASCADE)
    equipmentSerialNumber = models.CharField(max_length=50)
    equipmentOwnerId = models.ForeignKey('People', db_column='equipmentOwnerId', on_delete=models.CASCADE)
    equipmentVendorId = models.ForeignKey('Organizations', db_column='equipmentVendorId', on_delete=models.CASCADE)
    equipmentPurchaseDate = models.DateTimeField()
    equipmentPurchaseOrderNumber = models.CharField(max_length=50, blank=True)
    equipmentDescription = models.CharField(max_length=5000, blank=True)
    equipmentDocumentationLink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.Equipment'


# ======================================================================================================================
# Equipment annotations table
# ======================================================================================================================
class EquipmentAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    equipmentId = models.ForeignKey(Equipment, db_column='equipmentId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId',
                                     on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.EquipmentAnnotations'


# ======================================================================================================================
# Equipment models table
# ======================================================================================================================
class EquipmentModels(models.Model):
    equipmentModelId = models.AutoField(primary_key=True)
    modelManufacturerId = models.ForeignKey('Organizations', verbose_name="model manufacturer",
                                            db_column='modelManufacturerId', on_delete=models.CASCADE)
    modelPartNumber = models.CharField(max_length=50, blank=True, verbose_name="model part number")
    modelName = models.CharField(max_length=255, verbose_name="model name")
    modelDescription = models.CharField(max_length=5000, blank=True, null=True, verbose_name="model description")
    isInstrument = models.BooleanField(verbose_name="Is this an instrument?")
    modelSpecificationsFileLink = models.CharField(max_length=255, verbose_name="link to manual for equipment",
                                                   blank=True)
    modelLink = models.CharField(max_length=255, verbose_name="link to website for model", blank=True)

    def __str__(self):
        s = u"%s" % self.modelName
        if self.modelPartNumber:
            s += u"- %s" % self.modelPartNumber
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.EquipmentModels'
        verbose_name = "equipment model"


# ======================================================================================================================
# Equipment used table
# ======================================================================================================================
class EquipmentUsed(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey(Actions, db_column='actionId', on_delete=models.CASCADE)
    equipmentId = models.ForeignKey(Equipment, db_column='equipmentId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.EquipmentUsed'


# ======================================================================================================================
# Extension properties table
# ======================================================================================================================
class ExtensionProperties(models.Model):
    propertyId = models.AutoField(primary_key=True)
    propertyName = models.CharField(max_length=255, verbose_name="property name")
    propertyDescription = models.CharField(max_length=5000, blank=True, verbose_name="property description")
    propertyDataTypeCV = models.ForeignKey(CvPropertyDataType, db_column='propertyDataTypeCV',
                                           verbose_name="property data type", on_delete=models.CASCADE)
    propertyUnitsId = models.ForeignKey('Units', db_column='propertyUnitsId', blank=True, null=True,
                                        verbose_name="units for property", on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s" % (self.propertyName, self.propertyDescription)

    class Meta:
        managed = True
        db_table = 'ODM2.ExtensionProperties'
        verbose_name = 'extension property'
        verbose_name_plural = 'extension properties'


# ======================================================================================================================
# External identifier systems table
# ======================================================================================================================
class ExternalIdentifierSystems(models.Model):
    externalIdentifierSystemId = models.AutoField(primary_key=True)
    externalIdentifierSystemName = models.CharField(max_length=255)
    identifierSystemOrganizationId = models.ForeignKey('Organizations', db_column='identifierSystemOrganizationId',
                                                       on_delete=models.CASCADE)
    externalIdentifierSystemDescription = models.CharField(max_length=5000, blank=True)
    externalIdentifierSystemURL = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"%s" % self.externalIdentifierSystemName

    class Meta:
        managed = True
        db_table = 'ODM2.ExternalIdentifierSystems'


# ======================================================================================================================
# Feature actions table
# ======================================================================================================================
class FeatureActions(models.Model):
    featureActionId = models.AutoField(primary_key=True, verbose_name="sampling feature action")
    samplingFeatureId = models.ForeignKey('SamplingFeatures', db_column='samplingFeatureId', on_delete=models.CASCADE)
    action = models.ForeignKey(Actions, db_column='actionId', on_delete=models.CASCADE)

    def __str__(self):
        return u"%s- %s - %s" % (self.featureActionId, self.samplingFeatureId, self.action)

    class Meta:
        managed = True
        db_table = 'ODM2.FeatureActions'
        verbose_name = 'action at sampling feature'
        verbose_name_plural = 'action at sampling feature'


# ======================================================================================================================
# Feature actions names table
# ======================================================================================================================
# this class just stores the unicode representation of a featureAction for faster lookup
class FeatureActionsNames(models.Model):
    featureActionNamesId = models.AutoField(primary_key=True)
    featureActionId = models.ForeignKey('FeatureActions', db_column='featureactionId',
                                        on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        managed = True
        db_table = 'ODM2EXTRA.FeatureActionsNames'
        verbose_name = 'feature action names'


# ======================================================================================================================
# Instrument output variables table
# ======================================================================================================================
class InstrumentOutputVariables(models.Model):
    instrumentOutputVariableId = models.AutoField(primary_key=True)
    modelId = models.ForeignKey(EquipmentModels, verbose_name="equipment model", db_column='modelId',
                                on_delete=models.CASCADE)
    variableId = models.ForeignKey('Variables', verbose_name="variable", db_column='variableId',
                                   on_delete=models.CASCADE)
    instrumentMethodId = models.ForeignKey('Methods', verbose_name="instrument method", db_column='instrumentMethodId',
                                           on_delete=models.CASCADE)
    instrumentResolution = models.CharField(max_length=255, verbose_name="instrument resolution", blank=True)
    instrumentAccuracy = models.CharField(max_length=255, verbose_name="instrument accuracy", blank=True)
    instrumentRawOutputUnitsId = models.ForeignKey('Units', related_name='+', verbose_name="instrument raw output unit",
                                                   db_column='instrumentRawOutputUnitsId', on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.modelId
        s += u"- %s" % self.variableId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.InstrumentOutputVariables'
        verbose_name = "instrument output variable"


# ======================================================================================================================
# Maintenance actions table
# ======================================================================================================================
class MaintenanceActions(models.Model):
    actionId = models.OneToOneField(Actions, db_column='actionId', primary_key=True, on_delete=models.CASCADE)
    isFactoryService = models.BooleanField()
    maintenanceCode = models.CharField(max_length=50, blank=True)
    maintenanceReason = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.MaintenanceActions'


# ======================================================================================================================
# Measurement results table
# ======================================================================================================================
class MeasurementResults(models.Model):
    resultId = models.OneToOneField('Results', verbose_name="Result Series", db_column='resultId', primary_key=True,
                                    on_delete=models.CASCADE)
    xLocation = models.FloatField(verbose_name="x location", blank=True, null=True)
    xLocationUnitsId = models.ForeignKey('Units', verbose_name="x location units", related_name='relatedXLocationUnits',
                                         db_column='xLocationUnitsId', blank=True, null=True, on_delete=models.CASCADE)
    yLocation = models.FloatField(blank=True, verbose_name="y location", null=True)
    yLocationUnitsId = models.ForeignKey('Units', verbose_name="y location units", related_name='relatedYLocationUnits',
                                         db_column='yLocationUnitsId', blank=True, null=True, on_delete=models.CASCADE)
    zLocation = models.FloatField(blank=True, verbose_name="z location", null=True)
    zLocationUnitsId = models.ForeignKey('Units', verbose_name="z location units", related_name='relatedZLocationUnits',
                                         db_column='zLocationUnitsId', blank=True, null=True, on_delete=models.CASCADE)
    spatialReferenceId = models.ForeignKey('SpatialReferences', verbose_name="spatial reference",
                                           db_column='spatialReferenceId', blank=True, null=True,
                                           on_delete=models.CASCADE)
    censorCodeCV = models.ForeignKey(CvCensorCode, verbose_name="censor code", db_column='censorCodeCV',
                                     on_delete=models.CASCADE)
    qualityCodeCV = models.ForeignKey(CvQualityCode, verbose_name="quality code", db_column='qualitycodecv',
                                      on_delete=models.CASCADE)
    aggregationStatisticCV = models.ForeignKey(CvAggregationStatistic, verbose_name="aggregation statistic",
                                               db_column='aggregationStatisticCV', on_delete=models.CASCADE)
    timeAggregationInterval = models.FloatField(verbose_name="time aggregation interval")
    timeAggregationIntervalUnitsId = models.ForeignKey('Units',
                                                       verbose_name="time aggregation " +
                                                                    "interval unit",
                                                       related_name='+',
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.resultId
        s += u", %s" % self.qualityCodeCV
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.MeasurementResults'
        ordering = ['censorcodecv', 'resultid']
        verbose_name = 'measurement result'


# ======================================================================================================================
# Measurement results value annotations table
# ======================================================================================================================
class MeasurementResultValueAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    valueId = models.ForeignKey('MeasurementResultValues', db_column='valueId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.MeasurementResultValueAnnotations'


# ======================================================================================================================
# Measurement results values table
# ======================================================================================================================
class MeasurementResultValues(models.Model):
    valueId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey(MeasurementResults, verbose_name='Result Series', db_column='resultid',
                                 on_delete=models.CASCADE)
    dataValue = models.FloatField(verbose_name='data value')
    valueDateTime = models.DateTimeField(verbose_name='value date time')
    valueDateTimeUtcOffset = models.IntegerField(verbose_name='value date time UTC offset', default=-5)

    def __str__(self):
        s = u"%s " % self.resultId
        s += u"- %s" % self.dataValue
        s += u"- %s" % self.valueDateTime
        return s

    @staticmethod
    def csv_header():
        s = 'databaseId,'
        s += 'Date and Time,'
        s += 'sampling feature/location,'
        s += 'time aggregation interval,'
        s += 'time aggregation unit,'
        s += 'citation,'
        return s

    def csv_output(self):
        s = str(self.valueId)
        s += ', {0}'.format(self.valueDateTime)
        s += ',\" {0}\"'.format(self.resultId.resultId.featureActionId.samplingFeatureId.samplingFeatureName)
        s += ', {0}'.format(self.resultId.timeaggregationinterval)
        s += ', {0},'.format(self.resultId.timeaggregationintervalunitsid)
        s = build_citation(s, self)
        return s

    def csv_header_short(self):
        s = '\" {0} -unit-{1}-processing level-{2}\",annotation,'.format(
            self.resultId.resultId.variableId.variableCode,
            self.resultId.resultId.unitsId.unitsName,
            self.resultId.resultId.processing_level)
        return s

    def csv_output_short(self):
        s = '{0}'.format(self.dataValue)
        mrv_annotation = MeasurementResultValueAnnotations.objects.filter(valueId=self.valueId)
        annotations = Annotations.objects.filter(annotationId__in=mrv_annotation)
        s += ',\"'
        for annotation in annotations:
            s += '{0} '.format(annotation)
        s += '\"'
        s += ','
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.MeasurementResultValues'
        verbose_name = 'measurement result value'


# ======================================================================================================================
# Measurement results value file table
# ======================================================================================================================
class MeasurementResultValueFile(models.Model):
    valueFileid = models.AutoField(primary_key=True)
    resultId = models.ForeignKey(MeasurementResults,
                                 help_text="CAUTION saving a measurement " +
                                           "result value file will attempt to " +
                                           "load values into the database.", verbose_name='result',
                                 db_column='resultId',
                                 on_delete=models.CASCADE)
    valueFile = models.FileField(upload_to='resultValues', verbose_name="value file ")

    def __str__(self):
        s = u"%s" % self.resultId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2EXTRA.MeasurementResultValuefile'
        verbose_name = 'measurement result value file'

    def save(self, *args, **kwargs):
        handle_uploaded_file(self.valueFile.file, self.resultid)
        super(MeasurementResultValueFile, self).save(*args, **kwargs)


# ======================================================================================================================
# Method annotations table
# ======================================================================================================================
class MethodAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    methodId = models.ForeignKey('Methods', db_column='methodId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.MethodAnnotations'


# ======================================================================================================================
# Method citations table
# ======================================================================================================================
class MethodCitations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    methodId = models.ForeignKey('Methods', db_column='methodId', verbose_name='method', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV',
                                           verbose_name='relationship type', on_delete=models.CASCADE)
    citationId = models.ForeignKey(Citations, db_column='citationId', verbose_name='citation', on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.methodId
        s += u"-, %s" % self.citationId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.MethodCitations'
        verbose_name = 'method citation'


# ======================================================================================================================
# Method extension property values table
# ======================================================================================================================
class MethodExtensionPropertyValues(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    methodId = models.ForeignKey('Methods', db_column='methodId', on_delete=models.CASCADE)
    propertyId = models.ForeignKey(ExtensionProperties, db_column='propertyId', on_delete=models.CASCADE)
    propertyValue = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'ODM2.MethodExtensionPropertyValues'


# ======================================================================================================================
# Method external identifiers values table
# ======================================================================================================================
class MethodExternalIdentifiers(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    methodId = models.ForeignKey('Methods', db_column='methodId', on_delete=models.CASCADE)
    externalIdentifierSystemId = models.ForeignKey(ExternalIdentifierSystems, db_column='externalIdentifierSystemId',
                                                   on_delete=models.CASCADE)
    methodExternalIdentifier = models.CharField(max_length=255)
    methodExternalIdentifierURI = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.MethodExternalIdentifiers'


# ======================================================================================================================
# Methods table
# ======================================================================================================================
class Methods(models.Model):
    methodId = models.AutoField(primary_key=True)
    methodTypeCV = models.ForeignKey(CvMethodType, verbose_name='method type',
                                     help_text='A vocabulary for describing types of Methods '
                                               'associated with creating observations. '
                                               'MethodTypes correspond with ActionTypes in ODM2. '
                                               'An Action must be performed using an '
                                               'appropriate MethodType - e.g., a specimen '
                                               'collection Action should be associated with a '
                                               'specimen collection method. details for '
                                               'individual values '
                                               'here: http://vocabulary.odm2.org/methodtype/',
                                     db_column='methodTypeCV', on_delete=models.CASCADE)
    methodCode = models.CharField(verbose_name='method code', max_length=50)
    methodName = models.CharField(verbose_name='method name', max_length=255)
    methodDescription = models.CharField(verbose_name='method description', max_length=5000,
                                         blank=True)
    methodLink = models.CharField(verbose_name='web link for method', max_length=255, blank=True)
    organizationId = models.ForeignKey('Organizations', verbose_name='organization', db_column='organizationId',
                                       blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.methodCode
        if self.methodTypeCV:
            s += u", %s" % self.methodTypeCV
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Methods'
        verbose_name = 'method'
        ordering = ["methodName"]


# ======================================================================================================================
# Model affiliations table
# ======================================================================================================================
class ModelAffiliations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    modelId = models.ForeignKey('Models', db_column='modelId', on_delete=models.CASCADE)
    affiliationId = models.ForeignKey(Affiliations, db_column='affiliationId', on_delete=models.CASCADE)
    isPrimary = models.BooleanField()
    roleDescription = models.CharField(max_length=5000, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.ModelAffiliations'


# ======================================================================================================================
# Models table
# ======================================================================================================================
class Models(models.Model):
    modelId = models.AutoField(primary_key=True)
    modelCode = models.CharField(max_length=50)
    modelName = models.CharField(max_length=255)
    modelDescription = models.CharField(max_length=5000, blank=True)
    version = models.CharField(max_length=255, blank=True)
    modelLink = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.Models'


# ======================================================================================================================
# Organizations table
# ======================================================================================================================
class Organizations(models.Model):
    organizationId = models.AutoField(primary_key=True)
    organizationTypeCV = models.ForeignKey(CvOrganizationType, verbose_name="organization type",
                                           db_column='organizationTypeCV', on_delete=models.CASCADE)
    organizationCode = models.CharField(verbose_name="organization code", max_length=50)
    organizationName = models.CharField(verbose_name="organization name", max_length=255)
    organizationDescription = models.CharField(verbose_name="organization description", max_length=5000, blank=True)
    organizationLink = models.CharField(verbose_name="organization web link", max_length=255, blank=True)
    parentOrganizationId = models.ForeignKey('self', verbose_name="parent organization",
                                             db_column='parentOrganizationId', blank=True, null=True, default=1,
                                             on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s" % self.organizationCode
        if self.organizationName:
            s += u", %s" % self.organizationName
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.Organizations'
        verbose_name = 'Organization'


# ======================================================================================================================
# People table
# ======================================================================================================================
class People(models.Model):
    personId = models.AutoField(primary_key=True)
    personFirstName = models.CharField(max_length=255, verbose_name="first name")
    personMiddleName = models.CharField(max_length=255, verbose_name="middle name", blank=True)
    personLastName = models.CharField(max_length=255, verbose_name="last name")

    def __str__(self):
        s = u"%s" % self.personLastName
        if self.personFirstName:
            s += u", %s" % self.personFirstName
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.People'
        verbose_name = 'people'
        verbose_name_plural = 'people'
        ordering = ["personLastName"]


# ======================================================================================================================
# Person external identifiers table
# ======================================================================================================================
class PersonExternalIdentifiers(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    personId = models.ForeignKey(People, db_column='personId', on_delete=models.CASCADE)
    externalIdentifierSystemId = models.ForeignKey(ExternalIdentifierSystems, db_column='externalIdentifierSystemId',
                                                   on_delete=models.CASCADE)
    personExternalIdentifier = models.CharField(max_length=255)
    personExternalIdentifierURI = models.CharField(max_length=255, blank=True)

    def __str__(self):
        s = u"%s - %s - %s - %s" % (
            self.personId, self.externalIdentifierSystemId, self.personExternalIdentifier,
            self.personExternalIdentifierURI)
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.PersonExternalIdentifiers'
        verbose_name_plural = 'ORC ID (Person Unique Identifier)'


# ======================================================================================================================
# Point coverage results table
# ======================================================================================================================
class PointCoverageResults(models.Model):
    resultId = models.OneToOneField('Results', db_column='resultid', primary_key=True, on_delete=models.CASCADE)
    zLocation = models.FloatField(blank=True, null=True)
    zLocationUnitsId = models.ForeignKey('Units', related_name='+', db_column='zLocationUnitsId', blank=True, null=True,
                                         on_delete=models.CASCADE)
    spatialReferenceId = models.ForeignKey('SpatialReferences', db_column='spatialReferenceId', blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedXSpacing = models.FloatField(blank=True, null=True)
    intendedXSpacingUnitsId = models.ForeignKey('Units', related_name='+', db_column='intendedXSpacingUnitsId',
                                                blank=True, null=True, on_delete=models.CASCADE)
    intendedYSpacing = models.FloatField(blank=True, null=True)
    intendedYSpacingUnitsId = models.ForeignKey('Units', related_name='+', db_column='intendedYSpacingUnitsId',
                                                blank=True, null=True, on_delete=models.CASCADE)
    aggregationStatisticCV = models.ForeignKey(CvAggregationStatistic, db_column='aggregationStatisticCV',
                                               on_delete=models.CASCADE)
    timeAggregationInterval = models.FloatField()
    timeAggregationIntervalUnitsId = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'ODM2.PointCoverageResults'


# ======================================================================================================================
# Point coverage result value annotations table
# ======================================================================================================================
class PointCoverageResultValueAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    valueId = models.ForeignKey('PointCoverageResultValues', db_column='valueId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.PointCoverageResultValueAnnotations'


# ======================================================================================================================
# Point coverage result value annotations table
# ======================================================================================================================
class PointCoverageResultValues(models.Model):
    valueId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey(PointCoverageResults, db_column='resultId', on_delete=models.CASCADE)
    dataValue = models.BigIntegerField()
    valueDateTime = models.DateTimeField()
    valueDateTimeUtcOffset = models.IntegerField()
    xLocation = models.FloatField()
    xLocationUnitsId = models.ForeignKey('Units', related_name='+', db_column='xLocationUnitsId',
                                         on_delete=models.CASCADE)
    yLocation = models.FloatField()
    yLocationUnitsId = models.ForeignKey('Units', related_name='+', db_column='yLocationUnitsId',
                                          on_delete=models.CASCADE)
    censorCodeCV = models.ForeignKey(CvCensorCode, db_column='censorCodeCV', on_delete=models.CASCADE)
    qualityCodeCV = models.ForeignKey(CvQualityCode, db_column='qualityCodeCV', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.PointCoverageResultValues'


# ======================================================================================================================
# Processing levels table
# ======================================================================================================================
class ProcessingLevels(models.Model):
    processingLevelId = models.AutoField(primary_key=True)
    processingLevelCode = models.CharField(verbose_name='processing level code', max_length=50)
    definition = models.CharField(max_length=5000, blank=True)
    explanation = models.CharField(max_length=5000, blank=True)

    def __str__(self):
        s = u"%s " % self.processingLevelCode
        if self.definition:
            s += u", %s" % self.definition
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.ProcessingLevels'
        verbose_name = 'processing level'


# ======================================================================================================================
# Profile results table
# ======================================================================================================================
class ProfileResults(models.Model):
    resultId = models.OneToOneField('Results', verbose_name='result', db_column='resultid',
                                    primary_key=True,
                                    on_delete=models.CASCADE)
    xLocation = models.FloatField(blank=True, verbose_name='x location', null=True)
    xLocationUnitsId = models.ForeignKey('Units', verbose_name='x location units', related_name='+',
                                         db_column='xLocationUnitsId', blank=True, null=True, on_delete=models.CASCADE)
    yLocation = models.FloatField(blank=True, verbose_name='y location', null=True)
    yLocationUnitsId = models.ForeignKey('Units', related_name='+', verbose_name='y location units',
                                         db_column='yLocationUnitsId', blank=True, null=True, on_delete=models.CASCADE)
    spatialReferenceId = models.ForeignKey('SpatialReferences', verbose_name='spatial reference',
                                           db_column='spatialReferenceId', blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedZSpacing = models.FloatField(blank=True, verbose_name='intended depth', null=True)
    intendedZSpacingUnitsId = models.ForeignKey('Units', verbose_name='intended depth units', related_name='+',
                                                db_column='intendedzspacingunitsid', blank=True, null=True,
                                                on_delete=models.CASCADE)
    intendedTimeSpacing = models.FloatField(blank=True, null=True, verbose_name='intended time spacing')
    intendedTimeSpacingUnitsId = models.ForeignKey('Units', verbose_name='intended time spacing unit', related_name='+',
                                                   db_column='intendedTimeSpacingUnitsId', blank=True, null=True,
                                                   on_delete=models.CASCADE)
    aggregationStatisticCV = models.ForeignKey(CvAggregationStatistic, verbose_name='aggregation statistic',
                                               db_column='aggregationStatisticCV', on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s" % self.resultId
        if self.xLocation:
            s += u"- %s" % self.xLocation
        if self.xLocationUnitsId:
            s += u", %s" % self.xLocationUnitsId
        if self.yLocation:
            s += u"- %s" % self.yLocation
        if self.yLocationUnitsId:
            s += u", %s" % self.yLocationUnitsId
        if self.intendedZSpacing:
            s += u"- %s" % self.intendedZSpacing
        if self.intendedZSpacingUnitsId:
            s += u", %s" % self.intendedZSpacingUnitsId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.ProfileResults'
        verbose_name = 'profile result'


# ======================================================================================================================
# Profile result value annotations table
# ======================================================================================================================
class ProfileResultValueAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    valueId = models.ForeignKey('ProfileResultValues', db_column='valueId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.ProfileResultValueAnnotations'


# ======================================================================================================================
# Profile result values table
# ======================================================================================================================
class ProfileResultValues(models.Model):
    valueId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey(ProfileResults, db_column='resultid', on_delete=models.CASCADE)
    dataValue = models.FloatField(verbose_name='data value')
    valueDateTime = models.DateTimeField(verbose_name='value date and time', blank=True, null=True)
    valueDateTimeUtcOffset = models.IntegerField(verbose_name='value date and time UTC offset', blank=True, null=True)
    zLocation = models.FloatField(verbose_name='z location', blank=True, null=True)
    zAggregationInterval = models.FloatField(verbose_name='z aggregation interval', blank=True, null=True)
    zLocationUnitsId = models.ForeignKey('Units', verbose_name='z location unit', related_name='+',
                                         db_column='zlocationunitsid', blank=True, null=True, on_delete=models.CASCADE)
    censorCodeCV = models.ForeignKey(CvCensorCode, verbose_name='censor code', db_column='censorcodecv',
                                     on_delete=models.CASCADE)
    qualityCodeCV = models.ForeignKey(CvQualityCode, verbose_name='quality code', db_column='qualitycodecv',
                                      on_delete=models.CASCADE)
    timeAggregationInterval = models.FloatField(verbose_name='time aggregation interval', blank=True, null=True)
    timeAggregationIntervalUnitsId = models.ForeignKey('Units',
                                                       verbose_name='time aggregation interval unit',
                                                       related_name='+',
                                                       db_column='timeAggregationIntervalUnitsId',
                                                       blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.resultId
        s += u", %s" % self.dataValue
        s += u", %s" % self.zLocation
        s += u", %s" % self.zLocationUnitsId
        return s

    @staticmethod
    def csv_header():
        s = 'databaseId,'
        s += 'depth,'
        s += 'sampling feature/location,'
        s += 'sampling feature uri,'
        s += 'method,'
        s += 'citation'
        return s

    def cite(self):
        s = build_citation('', self)
        return s

    def csv_header_short(self):
        s = ',\" {0} -unit-{1}-processing level-{2}\"'.format(
            self.resultId.resultId.variableId.variableCode,
            self.resultId.resultId.unitsId.unitsName,
            self.resultId.resultId.processing_level)
        return s

    def csv_output(self):
        s = '{0}'.format(self.resultId.resultId.resultId)
        s += ', {0}-{1} {2} '.format((self.zLocation - self.zAggregationInterval), self.zLocation,
                                     self.zLocationUnitsId)
        s += ',\" {0}\"'.format(self.resultId.resultId.featureActionId.samplingFeatureId.samplingFeatureName)
        try:
            ss = SamplingFeatureExternalIdentifiers.objects.filter(
                samplingfeatureid=self.resultId.resultId.featureActionId.samplingFeatureId).get()
            s += ', {0}'.format(ss.samplingFeatureExternalIdentifierURI)
        except SamplingFeatureExternalIdentifiers.DoesNotExist:
            s += ','
        s += ',\" {0}\"'.format(self.resultId.resultId.featureActionId.action.method.methodDescription)
        s = build_citation(s, self)
        s += ','
        return s

    def csv_output_short(self):
        s = '{0}'.format(self.dataValue)
        s += ','
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.ProfileResultValues'
        verbose_name = 'profile result value'


# ======================================================================================================================
# Reference material external identifiers table
# ======================================================================================================================
class ReferenceMaterialExternalIdentifiers(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    referenceMaterialId = models.ForeignKey('ReferenceMaterials', db_column='referenceMaterialId',
                                             on_delete=models.CASCADE)
    externalIdentifierSystemId = models.ForeignKey(ExternalIdentifierSystems, db_column='externalIdentifierSystemId',
                                                   on_delete=models.CASCADE)
    referenceMaterialExternalIdentifier = models.CharField(max_length=255)
    referenceMaterialExternalIdentifierURI = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.ReferenceMaterialExternalIdentifiers'


# ======================================================================================================================
# Reference material external identifiers table
# ======================================================================================================================
class ReferenceMaterials(models.Model):
    referenceMaterialId = models.AutoField(primary_key=True)
    referenceMaterialMediumCV = models.ForeignKey(CvReferenceMaterialMedium, db_column='referenceMaterialMediumCV',
                                                  on_delete=models.CASCADE)
    referenceMaterialOrganizationId = models.ForeignKey(Organizations, db_column='referenceMaterialOrganizationId',
                                                        on_delete=models.CASCADE)
    referenceMaterialCode = models.CharField(max_length=50)
    referenceMaterialLotCode = models.CharField(max_length=255, blank=True)
    referenceMaterialPurchaseDate = models.DateTimeField(blank=True, null=True)
    referenceMaterialExpirationDate = models.DateTimeField(blank=True, null=True)
    referenceMaterialCertificateLink = models.CharField(max_length=255, blank=True)
    samplingFeatureId = models.ForeignKey('SamplingFeatures', db_column='samplingFeatureId', blank=True, null=True,
                                          on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.ReferenceMaterials'


# ======================================================================================================================
# Reference material values table
# ======================================================================================================================
class ReferenceMaterialValues(models.Model):
    referenceMaterialValueId = models.AutoField(primary_key=True)
    referenceMaterialId = models.ForeignKey(ReferenceMaterials, db_column='referencematerialId',
                                            on_delete=models.CASCADE)
    referenceMaterialValue = models.FloatField()
    referenceMaterialAccuracy = models.FloatField(blank=True, null=True)
    variableId = models.ForeignKey('Variables', db_column='variableId', on_delete=models.CASCADE)
    unitsId = models.ForeignKey('Units', related_name='+', db_column='unitsId', on_delete=models.CASCADE)
    citationId = models.ForeignKey(Citations, db_column='citationid', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.ReferenceMaterialValues'


# ======================================================================================================================
# Related actions table
# ======================================================================================================================
class RelatedActions(models.Model):
    relationId = models.AutoField(primary_key=True)
    actionId = models.ForeignKey(Actions, verbose_name='action', db_column='actionId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, verbose_name='relationship type',
                                           db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedActionId = models.ForeignKey(Actions, verbose_name='related action', related_name='RelatedActions',
                                        db_column='relatedActionId', on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s" % self.actionId
        if self.relationshipTypeCV:
            s += u", %s" % self.relationshipTypeCV
        if self.relatedActionId:
            s += u", %s" % self.relatedActionId
        return s

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedActions'
        verbose_name = 'related action (associates one action with another)'
        verbose_name_plural = 'related action (associates one action with another)'


# ======================================================================================================================
# Related annotations table
# ======================================================================================================================
class RelatedAnnotations(models.Model):
    relationId = models.AutoField(primary_key=True)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedAnnotationId = models.ForeignKey(Annotations, related_name='RelatedAnnotations',
                                            db_column='relatedAnnotationId', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedAnnotations'


# ======================================================================================================================
# Related citations table
# ======================================================================================================================
class RelatedCitations(models.Model):
    relationId = models.AutoField(primary_key=True)
    citationId = models.ForeignKey(Citations, db_column='citationId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedCitationId = models.ForeignKey(Citations, related_name='RelatedCitations', db_column='relatedCitationId',
                                          on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedCitations'


# ======================================================================================================================
# Related datasets table
# ======================================================================================================================
class RelatedDatasets(models.Model):
    relationId = models.AutoField(primary_key=True)
    datasetId = models.ForeignKey(Datasets, db_column='datasetId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedDatasetId = models.ForeignKey(Datasets, related_name='relatedDataset', db_column='relatedDatasetId',
                                         on_delete=models.CASCADE)
    versionCode = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedDatasets'


# ======================================================================================================================
# Related equipment table
# ======================================================================================================================
class RelatedEquipment(models.Model):
    relationId = models.AutoField(primary_key=True)
    equipmentId = models.ForeignKey(Equipment, db_column='equipmentId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedEquipmentId = models.ForeignKey(Equipment, related_name='relatedEquipment', db_column='relatedEquipmentId',
                                           on_delete=models.CASCADE)
    relationshipStartDateTime = models.DateTimeField()
    relationshipStartDateTimeUtcOffset = models.IntegerField()
    relationshipEndDateTime = models.DateTimeField(blank=True, null=True)
    relationshipEndDateTimeUtcOffset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedEquipment'


# ======================================================================================================================
# Related Features table
# ======================================================================================================================
class RelatedFeatures(models.Model):
    relationId = models.AutoField(primary_key=True)
    samplingFeatureId = models.ForeignKey('SamplingFeatures', verbose_name="first feature",
                                          db_column='samplingFeatureId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, verbose_name="relationship type",
                                           db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedFeatureId = models.ForeignKey('SamplingFeatures', verbose_name="second feature",
                                         related_name='RelatedFeatures', db_column='relatedFeatureId',
                                         on_delete=models.CASCADE)
    spatialOffsetId = models.ForeignKey('SpatialOffsets', verbose_name="spatial offset", db_column='spatialOffsetId',
                                        blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s - %s" % (self.samplingFeatureId, self.relationshipTypeCV, self.relatedFeatureId)

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedFeatures'
        verbose_name = 'relate two feature'


# ======================================================================================================================
# Related models table
# ======================================================================================================================
class RelatedModels(models.Model):
    relatedId = models.AutoField(primary_key=True)
    modelId = models.ForeignKey(Models, db_column='modelId', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV', on_delete=models.CASCADE)
    relatedModelId = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedModels'


# ======================================================================================================================
# Related results table
# ======================================================================================================================
class RelatedResults(models.Model):
    relationId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey('Results', db_column='resultId', verbose_name='data result', on_delete=models.CASCADE)
    relationshipTypeCV = models.ForeignKey(CvRelationshipType, db_column='relationshipTypeCV',
                                           verbose_name='relationship type', on_delete=models.CASCADE)
    relatedResultId = models.ForeignKey('Results', related_name='relatedResult', db_column='relatedResultId',
                                        verbose_name='related data result', on_delete=models.CASCADE)
    versionCode = models.CharField(max_length=50, blank=True, verbose_name='version code')
    relatedResultSequenceNumber = models.IntegerField(blank=True, null=True,
                                                      verbose_name='related result sequence number')

    def __str__(self):
        return u"%s - %s - %s" % (
            self.resultId, self.relationshipTypeCV, self.relatedResultId)

    class Meta:
        managed = True
        db_table = 'ODM2.RelatedResults'
        verbose_name = 'related result'


# ======================================================================================================================
# Related annotations table
# ======================================================================================================================
class ResultAnnotations(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey('Results', db_column='resultId', on_delete=models.CASCADE)
    annotationId = models.ForeignKey(Annotations, db_column='annotationId', on_delete=models.CASCADE)
    beginDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'ODM2.ResultAnnotations'


# ======================================================================================================================
# Result derivation equations table
# ======================================================================================================================
class ResultDerivationEquations(models.Model):
    resultId = models.OneToOneField('Results', db_column='resultId', verbose_name='data result', primary_key=True,
                                    on_delete=models.CASCADE)
    derivationEquationId = models.ForeignKey(DerivationEquations, db_column='derivationEquationId',
                                             on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s" % (self.resultId, self.derivationEquationId)

    class Meta:
        managed = True
        db_table = 'ODM2.ResultDerivationEquations'
        verbose_name= 'result derivation equation'


# ======================================================================================================================
# Result extension property values table
# ======================================================================================================================
class ResultExtensionPropertyValues(models.Model):
    bridgeId = models.AutoField(primary_key=True)
    resultId = models.ForeignKey('Results', db_column='resultId', on_delete=models.CASCADE)
    propertyId = models.ForeignKey(ExtensionProperties, db_column='propertyId', on_delete=models.CASCADE)
    propertyValue = models.CharField(max_length=255)

    def __str__(self):
        return u"%s - %s: value %s" % (self.resultId, self.propertyId, self.propertyValue)

    class Meta:
        managed = True
        db_table = 'ODM2.ResultExtensionPropertyValues'


# ======================================================================================================================
# Result normalization values table
# ======================================================================================================================
class ResultNormalizationValues(models.Model):
    resultId = models.OneToOneField('Results', db_column='resultId', primary_key=True, on_delete=models.CASCADE)
    normalizedByReferenceMaterialValueId = models.ForeignKey(ReferenceMaterialValues,
                                                             db_column='normalizedByReferenceMaterialValueId',
                                                             on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ODM2.ResultNormalizationValues'


# ======================================================================================================================
# Results table
# ======================================================================================================================
@python_2_unicode_compatible
class Results(models.Model):
    resultId = models.AutoField(primary_key=True, verbose_name="data result")
    resultUUID = models.UUIDField(default=uuid.uuid4, editable=False)
    featureActionId = models.ForeignKey(FeatureActions, related_name="feature_actions",
                                        verbose_name="sampling feature action", db_column='featureactionid',
                                        on_delete=models.CASCADE)
    resultType = models.ForeignKey(CvResultType, verbose_name='result type', db_column='resultTypeCV',
                                   on_delete=models.CASCADE)
    variableId = models.ForeignKey('Variables', verbose_name='variable', db_column='variableid',
                                   on_delete=models.CASCADE)
    unitsId = models.ForeignKey('Units', verbose_name='units', related_name='+', db_column='unitsId',
                                 on_delete=models.CASCADE)
    taxonomicClassifierId = models.ForeignKey('Taxonomicclassifiers', verbose_name='taxonomic classifier',
                                              db_column='taxonomicclassifierid', blank=True, null=True,
                                              on_delete=models.CASCADE)
    processing_level = models.ForeignKey(Processinglevels, db_column='processinglevelid',
                                         on_delete=models.CASCADE)
    resultdatetime = models.DateTimeField(verbose_name='Start result date time', blank=True,
                                          null=True)
    resultdatetimeutcoffset = models.BigIntegerField(
        verbose_name='Start result date time UTC offset', default=4,
        null=True)
    # validdatetime>> Date and time for which the result is valid (e.g., for a forecast result).
    # Should probably be expressed as a duration
    validdatetime = models.DateTimeField(
        verbose_name='valid date time- Date and time for which the result is valid',
        blank=True, null=True)
    validdatetimeutcoffset = models.BigIntegerField(verbose_name='valid date time UTC offset',
                                                    default=4, null=True)
    statuscv = models.ForeignKey(CvStatus, verbose_name='status', db_column='statuscv', blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)
    sampledmediumcv = models.ForeignKey(CvMedium, verbose_name='sampled medium',
                                        db_column='sampledmediumcv',
                                        blank=True, null=True,
                                        on_delete=models.CASCADE)
    valuecount = models.IntegerField(verbose_name='number of recorded values')

    # def __str__(self):
    #    return u'%s - %s' % (self.resultid, self.feature_action)
    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        s += 'time aggregation interval,'
        s += 'time aggregation unit,'
        # s += 'citation,'

        return s

    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.variableid.variablecode,
            self.unitsid.unitsname,
            self.processing_level.processinglevelcode)
        return s

    def csvheaderShort(self):
        s = '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.variableid.variablecode,
            self.unitsid.unitsabbreviation,
            self.processing_level.processinglevelcode)
        return s

    def __str__(self):
        return "%s - %s - ID: %s" % (self.variableid, self.featureactionid, self.resultid)

    class Meta:
        managed = True


            db_table = r'Results'

            db_table = r'results'
        verbose_name = 'data result'
        ordering = ["variableid"]


class Resultsdataquality(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Results, db_column='resultid', verbose_name='result',
                                 on_delete=models.CASCADE)
    dataqualityid = models.ForeignKey(Dataquality, db_column='dataqualityid',
                                      verbose_name='data quality',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s" % (self.resultid, self.dataqualityid)

    class Meta:
        managed = True


            db_table = r'ResultsDataQuality'

            db_table = r'resultsdataquality'
        verbose_name = 'results data quality'
        verbose_name_plural = 'results data quality'


class Samplingfeatureannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid',
                                           on_delete=models.CASCADE)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid',
                                     on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s" % self.samplingfeatureid
        if self.annotationid:
            s += u"- %s" % self.annotationid
        return s

    class Meta:
        managed = True


            db_table = r'SamplingFeatureAnnotations'

            db_table = r'samplingfeatureannotations'


class Samplingfeatureextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid',
                                           on_delete=models.CASCADE)
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid',
                                   on_delete=models.CASCADE)
    propertyvalue = models.CharField(max_length=255)

    def __str__(self):
        s = u"%s" % self.samplingfeatureid
        if self.propertyvalue:
            s += u"- %s - %s%s" % (
            self.propertyid.propertyname, self.propertyvalue, self.propertyid.propertyunitsid.unitsabbreviation)
        return s

    class Meta:
        managed = True


            db_table = r'SamplingFeatureExtensionPropertyValues'

            db_table = r'samplingfeatureextensionpropertyvalues'


class SamplingFeatureExternalIdentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey('Samplingfeatures', db_column='samplingfeatureid',
                                           on_delete=models.CASCADE)
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid',
                                                   on_delete=models.CASCADE)
    samplingfeatureexternalidentifier = models.CharField(max_length=255)
    samplingfeatureexternalidentifieruri = models.CharField(max_length=255, blank=True)

    def __str__(self):
        s = u"%s - %s - %s - %s" % (
            self.samplingfeatureid, self.externalidentifiersystemid,
            self.samplingfeatureexternalidentifier,
            self.samplingfeatureexternalidentifieruri)
        return s

    class Meta:
        managed = True


            db_table = r'SamplingFeatureExternalIdentifiers'

            db_table = r'samplingfeatureexternalidentifiers'


class Samplingfeatures(models.Model):
    samplingfeatureid = models.AutoField(primary_key=True)
    samplingfeatureuuid = UUIDField(default=uuid.uuid4, editable=False)
    sampling_feature_type = models.ForeignKey(CvSamplingfeaturetype,
                                              db_column='samplingfeaturetypecv',
                                              on_delete=models.CASCADE)
    samplingfeaturecode = models.CharField(verbose_name='sampling feature or location code', max_length=50)
    samplingfeaturename = models.CharField(verbose_name='sampling feature or location name', max_length=255,
                                           blank=True, null=True)
    samplingfeaturedescription = models.CharField(verbose_name='sampling feature or location description',
                                                  max_length=5000,
                                                  blank=True)
    sampling_feature_geo_type = models.ForeignKey(CvSamplingfeaturegeotype,
                                                  db_column='samplingfeaturegeotypecv',
                                                  default="Point", null=True,
                                                  on_delete=models.CASCADE)
    featuregeometry = models.TextField(verbose_name='feature geometry', blank=True,
                                       null=True)  # GeometryField This field type is a guess.
    elevation_m = models.FloatField(verbose_name='elevation', blank=True, null=True)
    elevation_datum = models.ForeignKey(CvElevationdatum, db_column='elevationdatumcv', blank=True,
                                        null=True,
                                        on_delete=models.CASCADE)

    objects = GeoManager()

    def featuregeometrywkt(self):
        return GEOSGeometry(self.featuregeometry)

    def __str__(self):
        s = u"%s - %s- %s" % (
            self.samplingfeaturecode, self.samplingfeatureid, self.sampling_feature_type)
        if self.samplingfeaturename:
            s += u" - %s" % self.samplingfeaturename
        return s

    class Meta:
        managed = True

        print(_exportdb)

            db_table = r'SamplingFeatures'

            db_table = r'samplingfeatures'
        ordering = ('sampling_feature_type', 'samplingfeaturename',)
        verbose_name = 'sampling feature (location)'


class Sectionresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True,
                                    on_delete=models.CASCADE)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                         blank=True, null=True,
                                         on_delete=models.CASCADE)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid',
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedxspacing = models.FloatField(blank=True, null=True)
    intendedxspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='intendedxspacingunitsid',
                                                blank=True, null=True,
                                                on_delete=models.CASCADE)
    intendedzspacing = models.FloatField(blank=True, null=True)
    intendedzspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='intendedzspacingunitsid',
                                                blank=True, null=True,
                                                on_delete=models.CASCADE)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True,
                                                   on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SectionResults'

            db_table = r'sectionresults'


class Sectionresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Sectionresultvalues', db_column='valueid',
                                 on_delete=models.CASCADE)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid',
                                     on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SectionResultValueAnnotations'

            db_table = r'sectionresultvalueannotations'


class Sectionresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Sectionresults, db_column='resultid',
                                 on_delete=models.CASCADE)
    datavalue = models.FloatField()
    valuedatetime = models.BigIntegerField()
    valuedatetimeutcoffset = models.BigIntegerField()
    xlocation = models.FloatField()
    xaggregationinterval = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                          on_delete=models.CASCADE)
    zlocation = models.BigIntegerField()
    zaggregationinterval = models.FloatField()
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                          on_delete=models.CASCADE)
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.CASCADE)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                      on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SectionResultValues'

            db_table = r'sectionresultvalues'


class Simulations(models.Model):
    simulationid = models.AutoField(primary_key=True)
    actionid = models.ForeignKey(Actions, db_column='actionid',
                                 on_delete=models.CASCADE)
    simulationname = models.CharField(max_length=255)
    simulationdescription = models.CharField(max_length=5000, blank=True)
    simulationstartdatetime = models.DateTimeField()
    simulationstartdatetimeutcoffset = models.IntegerField()
    simulationenddatetime = models.DateTimeField()
    simulationenddatetimeutcoffset = models.IntegerField()
    timestepvalue = models.FloatField()
    timestepunitsid = models.IntegerField()
    inputdatasetid = models.IntegerField(blank=True, null=True)
    modelid = models.ForeignKey(Models, db_column='modelid',
                                on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'Simulations'

            db_table = r'simulations'


class Sites(models.Model):
    samplingfeatureid = models.OneToOneField(Samplingfeatures, db_column='samplingfeatureid',
                                             primary_key=True, verbose_name='sampling feature',
                                             on_delete=models.CASCADE)
    sitetypecv = models.ForeignKey(CvSitetype, db_column='sitetypecv',
                                   on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    spatialreferenceid = models.ForeignKey('Spatialreferences', verbose_name='spatial reference id',
                                           db_column='spatialreferenceid',
                                           on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = 'Site'


            db_table = r'Sites'

            db_table = r'sites'

    def __str__(self):
        s = u"%s" % self.samplingfeatureid
        s += u"- %s" % self.sitetypecv
        return s


class Spatialoffsets(models.Model):
    spatialoffsetid = models.AutoField(primary_key=True)
    spatialoffsettypecv = models.ForeignKey(CvSpatialoffsettype, db_column='spatialoffsettypecv',
                                            on_delete=models.CASCADE)
    offset1value = models.FloatField()
    offset1unitid = models.ForeignKey('Units', related_name='+', db_column='offset1unitid',
                                       on_delete=models.CASCADE)
    offset2value = models.FloatField(blank=True, null=True)
    offset2unitid = models.ForeignKey('Units', related_name='+', db_column='offset2unitid',
                                      blank=True, null=True,
                                      on_delete=models.CASCADE)
    offset3value = models.FloatField(blank=True, null=True)
    offset3unitid = models.ForeignKey('Units', related_name='+', db_column='offset3unitid',
                                      blank=True, null=True,
                                      on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SpatialOffsets'

            db_table = r'spatialoffsets'


class Spatialreferenceexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    spatialreferenceid = models.ForeignKey('Spatialreferences', db_column='spatialreferenceid',
                                            on_delete=models.CASCADE)
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid',
                                                   on_delete=models.CASCADE)
    spatialreferenceexternalidentifier = models.CharField(max_length=255)
    spatialreferenceexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True


            db_table = r'SpatialReferenceExternalIdentifiers'

            db_table = r'spatialreferenceexternalidentifiers'


class Spatialreferences(models.Model):
    spatialreferenceid = models.AutoField(primary_key=True, verbose_name='spatial reference id')
    srscode = models.CharField(max_length=50, blank=True, verbose_name='spatial reference code')
    srsname = models.CharField(max_length=255, verbose_name='spatial reference name')
    srsdescription = models.CharField(max_length=5000, blank=True,
                                      verbose_name='spatial reference description')
    srslink = models.CharField(max_length=255, blank=True, verbose_name='spatial reference link')

    class Meta:
        managed = True
        verbose_name = 'Spatial reference'


            db_table = r'SpatialReferences'

            db_table = r'spatialreferences'

    def __str__(self):
        if self.srscode:
            s = u"%s" % self.srscode
        s += u"- %s" % self.srsname
        return s


class Specimenbatchpostions(models.Model):
    featureactionid = models.OneToOneField(Featureactions, db_column='featureactionid',
                                           primary_key=True,
                                           on_delete=models.CASCADE)
    batchpositionnumber = models.IntegerField()
    batchpositionlabel = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True


            db_table = r'SpecimenBatchPostions'

            db_table = r'specimenbatchpostions'


class Specimens(models.Model):
    samplingfeatureid = models.OneToOneField(Samplingfeatures, db_column='samplingfeatureid',
                                             primary_key=True,
                                             on_delete=models.CASCADE)
    specimentypecv = models.ForeignKey(CvSpecimentype, db_column='specimentypecv',
                                       on_delete=models.CASCADE)
    specimenmediumcv = models.ForeignKey(CvSpecimenmedium, db_column='specimenmediumcv',
                                         on_delete=models.CASCADE)
    isfieldspecimen = models.BooleanField()

    def __unicode__(self):
        return u'{spectypecv} - {specmedcv}'.format(spectypecv=self.specimentypecv,
                                                    specmedcv=self.specimenmediumcv)

    class Meta:
        managed = True


            db_table = r'Specimens'

            db_table = r'specimens'
        verbose_name = 'Specimen'



class Specimentaxonomicclassifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    samplingfeatureid = models.ForeignKey(Specimens, db_column='samplingfeatureid',
                                          on_delete=models.CASCADE)
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers',
                                              db_column='taxonomicclassifierid',
                                              on_delete=models.CASCADE)
    citationid = models.ForeignKey(Citations, db_column='citationid', blank=True, null=True,
                                   on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SpecimenTaxonomicClassifiers'

            db_table = r'specimentaxonomicclassifiers'


class Spectraresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True,
                                    on_delete=models.CASCADE)
    xlocation = models.FloatField(blank=True, null=True)
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                         blank=True, null=True,
                                         on_delete=models.CASCADE)
    ylocation = models.FloatField(blank=True, null=True)
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                         blank=True, null=True,
                                         on_delete=models.CASCADE)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         blank=True, null=True,
                                         on_delete=models.CASCADE)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedwavelengthspacing = models.FloatField(blank=True, null=True)
    intendedwavelengthspacingunitsid = models.ForeignKey(
        'Units',
        related_name='+',
        db_column='intendedwavelengthspacingunitsid',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SpectraResults'

            db_table = r'spectraresults'


class Spectraresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Spectraresultvalues', db_column='valueid',
                                 on_delete=models.CASCADE)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid',
                                     on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SpectraResultValueAnnotations'

            db_table = r'spectraresultvalueannotations'


class Spectraresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Spectraresults, db_column='resultid',
                                 on_delete=models.CASCADE)
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    excitationwavelength = models.FloatField()
    emissionwavelength = models.FloatField()
    wavelengthunitsid = models.ForeignKey('Units', related_name='+', db_column='wavelengthunitsid',
                                           on_delete=models.CASCADE)
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.CASCADE)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                      on_delete=models.CASCADE)
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'SpectraResultValues'

            db_table = r'spectraresultvalues'


class Taxonomicclassifierexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    taxonomicclassifierid = models.ForeignKey('Taxonomicclassifiers',
                                              db_column='taxonomicclassifierid',
                                              on_delete=models.CASCADE)
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid',
                                                   on_delete=models.CASCADE)
    taxonomicclassifierexternalidentifier = models.CharField(max_length=255)
    taxonomicclassifierexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True


            db_table = r'TaxonomicClassifierExternalIdentifiers'

            db_table = r'taxonomicclassifierexternalidentifiers'

            # I needed to add a sequence and set it as the default for the primary
            #  key to make the Taxonomic Classifiers class work
            # this is the SQL

            # CREATE SEQUENCE odm2.taxonomicclassifiers_taxonomicclassifiersid_seq
            #   INCREMENT 1
            #   MINVALUE 2
            #   MAXVALUE 9223372036854775807
            #   START 3
            #   CACHE 1;
            # ALTER TABLE odm2.taxonomicclassifiers_taxonomicclassifiersid_seq
            #   OWNER TO postgres;

            # ALTER TABLE odm2.taxonomicclassifiers
            #  ALTER COLUMN taxonomicclassifierid SET DEFAULT nextval
            # ('odm2.taxonomicclassifiers_taxonomicclassifiersid_seq'::regclass);


class Taxonomicclassifiers(models.Model):
    taxonomicclassifierid = models.AutoField(primary_key=True)
    taxonomic_classifier_type = models.ForeignKey(CvTaxonomicclassifiertype,
                                                  db_column='taxonomicclassifiertypecv',
                                                  help_text="A vocabulary for describing "
                                                            "types of taxonomies from which "
                                                            "descriptive terms used "
                                                            "in an ODM2 database have been drawn. "
                                                            "Taxonomic classifiers provide "
                                                            "a way to classify"
                                                            " Results and Specimens "
                                                            "according to terms from a formal "
                                                            "taxonomy.. Check "
                                                            "http://vocabulary.odm2.org/"
                                                            "taxonomicclassifiertype/  "
                                                            "for more info",
                                                  on_delete=models.CASCADE)
    taxonomicclassifiername = models.CharField(verbose_name='taxonomic classifier name',
                                               max_length=255)
    taxonomicclassifiercommonname = models.CharField(
        verbose_name='taxonomic classifier common name', max_length=255,
        blank=True)
    taxonomicclassifierdescription = models.CharField(
        verbose_name='taxonomic classifier description', max_length=5000,
        blank=True)
    parent_taxonomic_classifier = models.ForeignKey('self', db_column='parenttaxonomicclassifierid',
                                                    blank=True,
                                                    null=True,
                                                    on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s" % self.taxonomicclassifiername
        if self.taxonomicclassifiercommonname:
            s += u"- %s" % self.taxonomicclassifiercommonname
        return s

    class Meta:
        managed = True


            db_table = r'TaxonomicClassifiers'

            db_table = r'taxonomicclassifiers'
        verbose_name = 'taxonomic classifier'


class Timeseriesresults(models.Model):
    resultid = models.OneToOneField(Results, verbose_name="Result Series", db_column='resultid',
                                    primary_key=True,
                                    on_delete=models.CASCADE)
    xlocation = models.FloatField(blank=True, null=True, verbose_name="x location")
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                         blank=True, null=True, verbose_name="x location units",
                                         on_delete=models.CASCADE)
    ylocation = models.FloatField(blank=True, null=True, verbose_name="y location")
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                         verbose_name="y location units", blank=True, null=True,
                                         on_delete=models.CASCADE)
    zlocation = models.FloatField(blank=True, null=True, verbose_name="z location")
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         verbose_name="z location units", blank=True, null=True,
                                         on_delete=models.CASCADE)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           verbose_name="spatial reference",
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedtimespacing = models.FloatField(blank=True, null=True, verbose_name="Intended time spacing",
                                            help_text="time between measurements")
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   help_text="Units of time between measurements. This defines the time"
                                                             " series 1 hour, or 15 minutes for example.",
                                                   verbose_name="Time Units",
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True,
                                                   on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.resultid
        s += u", %s" % self.intendedtimespacing
        s += u", %s" % self.intendedtimespacingunitsid
        return s

    class Meta:
        managed = True



            db_table = r'TimeSeriesResults'

            db_table = r'timeseriesresults'
        ordering = ['resultid']
        verbose_name = 'time series result'


class Timeseriesresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Timeseriesresultvalues', db_column='valueid',
                                 on_delete=models.CASCADE)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid',
                                     on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'TimeSeriesResultValueAnnotations'

            db_table = r'timeseriesresultvalueannotations'


class Timeseriesresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Timeseriesresults, db_column='resultid',
                                 on_delete=models.CASCADE)
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.CASCADE)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                      on_delete=models.CASCADE)
    timeaggregationinterval = models.FloatField(verbose_name="Time Interval")
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       verbose_name="Time Units",
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.CASCADE)

    def __str__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.qualitycodecv
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        # s += 'time aggregation interval,'
        # s += 'time aggregation unit,'
        s += 'citation,'

        return s

    def csvoutput(self):
        s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s += ', {0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename)
        # s += ', {0}'.format(self.timeaggregationinterval)
        # s += ', {0},'.format(self.timeaggregationintervalunitsid)
        s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s

    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.resultid.resultid.variableid.variablecode,
            self.resultid.resultid.unitsid.unitsname,
            self.resultid.resultid.processing_level.processinglevelcode)
        return s

    def csvheaderShort(self):
        # s = 'method,'
        s = '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.resultid.resultid.variableid.variablecode,
            self.resultid.resultid.unitsid.unitsname,
            self.resultid.resultid.processing_level.processinglevelcode)
        s += 'quality code,'
        s += 'annotation,'
        return s

    def csvoutputShort(self):
        # s = '\" {0}\",'.format(
        #    self.resultid.resultid.featureactionid.action.method.methodcode)
        s = '{0},'.format(self.datavalue)
        s += '{0}'.format(self.qualitycodecv)
        trvannotation = Timeseriesresultvalueannotations.objects.filter(valueid=self.valueid)
        annotations = Annotations.objects.filter(annotationid__in=trvannotation)
        s += ',\"'
        for anno in annotations:
            s += '{0} '.format(anno)
        s += '\"'
        s += ','
        return s

    class Meta:
        managed = True


            db_table = r'TimeSeriesResultValues'

            db_table = r'timeseriesresultvalues'
        verbose_name = 'time series result value'


class Timeseriesresultvaluesext(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Timeseriesresults, db_column='resultid',
                                 on_delete=models.DO_NOTHING)
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.DO_NOTHING)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                      on_delete=models.DO_NOTHING)
    timeaggregationinterval = models.FloatField(verbose_name="Time Interval")
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       verbose_name="Time Units",
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.DO_NOTHING)
    samplingfeaturename = models.CharField(verbose_name='sampling feature name',
                                           max_length=255, blank=True, null=True)
    sampling_feature_type = models.ForeignKey(CvSamplingfeaturetype,
                                              db_column='samplingfeaturetypecv',
                                              on_delete=models.DO_NOTHING)
    processinglevelcode = models.CharField(verbose_name='processing level code', max_length=50)
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    aggregationstatisticname = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.qualitycodecv
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        s = 'databaseid,'
        # s+='Value,'
        s += 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        # s += 'time aggregation interval,'
        # s += 'time aggregation unit,'
        # s += 'citation,'

        return s

    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'location- {0}'.format(self.samplingfeaturename)
        return s

    def csvheaderShort(self):
        s = 'method,'
        s += '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'quality code,'
        return s

    def csvoutput(self):
        s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s += ', {0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.samplingfeaturename)
        # s += ', {0}'.format(self.timeaggregationinterval)
        # s += ', {0},'.format(self.timeaggregationintervalunitsid)
        # s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s

    def csvoutputShort(self):
        s = '\" {0}\",'.format(
            self.resultid.resultid.featureactionid.action.method.methodcode)
        s += '{0},'.format(self.datavalue)
        s += '{0},'.format(self.qualitycodecv)
        return s

    class Meta:
        managed = True
        db_table = r'odm2extra"."timeseriesresultvaluesext'
        verbose_name = 'time series result value'


class Timeseriesresultvaluesextwannotations(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.IntegerField()
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    censorcodecv = models.CharField(max_length=255)
    qualitycodecv = models.CharField(max_length=255)
    timeaggregationinterval = models.FloatField(verbose_name="Time Interval")
    timeaggregationintervalunitsid = models.IntegerField()
    samplingfeaturename = models.CharField(verbose_name='sampling feature name',
                                           max_length=255, blank=True, null=True)
    samplingfeaturetypecv = models.CharField(max_length=255)
    processinglevelcode = models.CharField(verbose_name='processing level code', max_length=50)
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    aggregationstatisticname = models.CharField(primary_key=True, max_length=255)
    annotationtext = models.CharField(max_length=500)

    def __str__(self):
        s = u"%s " % self.resultid
        s += u"- %s" % self.datavalue
        s += u"- %s" % self.qualitycodecv
        s += u"- %s" % self.valuedatetime
        return s

    @staticmethod
    def csvheader():
        # s = 'databaseid,'
        # s+='Value,'
        s = 'Date and Time,'
        # s += 'Variable Name,'
        # s += 'Unit Name,'
        # s += 'processing level,'
        s += 'sampling feature/location,'
        # s += 'time aggregation interval,'
        # s += 'time aggregation unit,'
        s += 'citation,'
        return s

    def csvoutput(self):
        # s = str(self.valueid)
        # s += ', {0}'.format(self.datavalue)
        s = '{0}'.format(self.valuedatetime)
        # s += ',\" {0}\"'.format(self.resultid.resultid.variableid.variablecode)
        # s += ',\" {0}\"'.format(self.resultid.resultid.unitsid.unitsname)
        # s += ',\" {0}\"'.format(self.resultid.resultid.processing_level)
        s += ',\" {0}\"'.format(
            self.samplingfeaturename)
        s += ','
        # s += ', {0}'.format(self.timeaggregationinterval)
        # s += ', {0},'.format(self.timeaggregationintervalunitsid)
        s = buildCitation(s, self)

        # s += ' {0}\"'.format(citation.citationlink)
        return s

    def email_text(self):
        s = '{0} -unit-{1}-processing level-{2} '.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'location- {0}'.format(self.samplingfeaturename)
        return s

    def csvheaderShort(self):
        # s = 'method,'
        s = '\" {0} -unit-{1}-processing level-{2}\",'.format(
            self.variablecode,
            self.unitsabbreviation,
            self.processinglevelcode)
        s += 'quality code,'
        s += 'quality annotation,'
        return s

    def csvoutputShort(self):
        # result = Results.objects.get(resultid=self.resultid)
        # s = '\" {0}\",'.format(
        #     result.featureactionid.action.method.methodcode)
        s = '{0},'.format(self.datavalue)
        s += '{0},'.format(self.qualitycodecv)
        if self.annotationtext:
            s += '\"{0} \",'.format(self.annotationtext)

            s += ','
        return s

    class Meta:
        managed = True
        db_table = r'odm2extra"."timeseriesresultvaluesextwannotations'
        verbose_name = 'time series result value'


class Trajectoryresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True,
                                    on_delete=models.CASCADE)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedtrajectoryspacing = models.FloatField(blank=True, null=True)
    intendedtrajectoryspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                         db_column='intendedtrajec'
                                                                   'toryspacingunitsid',
                                                         blank=True,
                                                         null=True,
                                                         on_delete=models.CASCADE)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True,
                                                   on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)

    class Meta:
        managed = True



            db_table = r'TrajectoryResults'

            db_table = r'trajectoryresults'


class Trajectoryresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Trajectoryresultvalues', db_column='valueid',
                                 on_delete=models.CASCADE)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid',
                                     on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'TrajectoryResultValueAnnotations'

            db_table = r'trajectoryresultvalueannotations'


class Trajectoryresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Trajectoryresults, db_column='resultid',
                                 on_delete=models.CASCADE)
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.IntegerField()
    xlocation = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                 on_delete=models.CASCADE)
    ylocation = models.FloatField()
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                 on_delete=models.CASCADE)
    zlocation = models.FloatField()
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                 on_delete=models.CASCADE)
    trajectorydistance = models.FloatField()
    trajectorydistanceaggregationinterval = models.FloatField()
    trajectorydistanceunitsid = models.ForeignKey('Units', related_name='+',
                                                  db_column='trajectorydistanceunitsid',
                                                  on_delete=models.CASCADE)
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.CASCADE)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                      on_delete=models.CASCADE)
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.CASCADE)

    class Meta:
        managed = True



            db_table = r'TrajectoryResultValues'

            db_table = r'trajectoryresultvalues'


class Transectresults(models.Model):
    resultid = models.OneToOneField(Results, db_column='resultid', primary_key=True,
                                    on_delete=models.CASCADE)
    zlocation = models.FloatField(blank=True, null=True)
    zlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='zlocationunitsid',
                                         blank=True, null=True,
                                         on_delete=models.CASCADE)
    spatialreferenceid = models.ForeignKey(Spatialreferences, db_column='spatialreferenceid',
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    intendedtransectspacing = models.FloatField(blank=True, null=True)
    intendedtransectspacingunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='intendedtransectspacingunitsid',
                                                       blank=True,
                                                       null=True,
                                                       on_delete=models.CASCADE)
    intendedtimespacing = models.FloatField(blank=True, null=True)
    intendedtimespacingunitsid = models.ForeignKey('Units', related_name='+',
                                                   db_column='intendedtimespacingunitsid',
                                                   blank=True, null=True,
                                                   on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)

    class Meta:
        managed = True



            db_table = r'TransectResults'

            db_table = r'transectresults'


class Transectresultvalueannotations(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    valueid = models.ForeignKey('Transectresultvalues', db_column='valueid',
                                 on_delete=models.CASCADE)
    annotationid = models.ForeignKey(Annotations, db_column='annotationid',
                                     on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'TransectResultValueAnnotations'

            db_table = r'transectresultvalueannotations'


class Transectresultvalues(models.Model):
    valueid = models.AutoField(primary_key=True)
    resultid = models.ForeignKey(Transectresults, db_column='resultid',
                                 on_delete=models.CASCADE)
    datavalue = models.FloatField()
    valuedatetime = models.DateTimeField()
    valuedatetimeutcoffset = models.DateTimeField()
    xlocation = models.FloatField()
    xlocationunitsid = models.ForeignKey('Units', related_name='+', db_column='xlocationunitsid',
                                 on_delete=models.CASCADE)
    ylocation = models.FloatField()
    ylocationunitsid = models.ForeignKey('Units', related_name='+', db_column='ylocationunitsid',
                                 on_delete=models.CASCADE)
    transectdistance = models.FloatField()
    transectdistanceaggregationinterval = models.FloatField()
    transectdistanceunitsid = models.ForeignKey('Units', related_name='+',
                                                db_column='transectdistanceunitsid',
                                                on_delete=models.CASCADE)
    censorcodecv = models.ForeignKey(CvCensorcode, db_column='censorcodecv',
                                     on_delete=models.CASCADE)
    qualitycodecv = models.ForeignKey(CvQualitycode, db_column='qualitycodecv',
                                 on_delete=models.CASCADE)
    aggregationstatisticcv = models.ForeignKey(CvAggregationstatistic,
                                               db_column='aggregationstatisticcv',
                                               on_delete=models.CASCADE)
    timeaggregationinterval = models.FloatField()
    timeaggregationintervalunitsid = models.ForeignKey('Units', related_name='+',
                                                       db_column='timeaggregationintervalunitsid',
                                                       on_delete=models.CASCADE)

    class Meta:
        managed = True


            db_table = r'TransectResultValues'

            db_table = r'transectresultvalues'


class Units(models.Model):
    unitsid = models.AutoField(primary_key=True)
    unit_type = models.ForeignKey(CvUnitstype,
                                  help_text="A vocabulary for describing the type of the Unit "
                                            "or the more general quantity that the Unit "
                                            "represents. View unit type details here "
                                            "http://vocabulary.odm2.org/unitstype/",
                                  db_column='unitstypecv',
                                  on_delete=models.CASCADE)
    unitsabbreviation = models.CharField(verbose_name='unit abbreviation', max_length=50)
    unitsname = models.CharField(verbose_name='unit name', max_length=255)
    unitslink = models.CharField(verbose_name='reference for the unit (web link)',
                                 max_length=255,
                                 blank=True)

    def __str__(self):
        s = u"%s" % self.unitsabbreviation
        # if self.unit_type:
        #    s = u"- %s" % (self.unit_type)
        if self.unitsname:
            s += u"- %s" % self.unitsname
        return s

    class Meta:
        managed = True
        ordering = ('unitsabbreviation', 'unitsname',)


            db_table = r'Units'

            db_table = r'units'
        verbose_name = 'unit'


class Variableextensionpropertyvalues(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    variableid = models.ForeignKey('Variables', db_column='variableid',
                                    on_delete=models.CASCADE)
    propertyid = models.ForeignKey(Extensionproperties, db_column='propertyid',
                                   on_delete=models.CASCADE)
    propertyvalue = models.CharField(max_length=255)

    class Meta:
        managed = True


            db_table = r'VariableExtensionPropertyValues'

            db_table = r'variableextensionpropertyvalues'


class Variableexternalidentifiers(models.Model):
    bridgeid = models.AutoField(primary_key=True)
    variableid = models.ForeignKey('Variables', db_column='variableid',
                                    on_delete=models.CASCADE)
    externalidentifiersystemid = models.ForeignKey(Externalidentifiersystems,
                                                   db_column='externalidentifiersystemid',
                                                   on_delete=models.CASCADE)
    variableexternalidentifier = models.CharField(max_length=255)
    variableexternalidentifieruri = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = True


            db_table = r'VariableExternalIdentifiers'

            db_table = r'variableexternalidentifiers'


class Variables(models.Model):
    variableid = models.AutoField(primary_key=True)
    variable_type = models.ForeignKey(CvVariabletype,
                                      help_text="view variable types here "
                                                "http://vocabulary.odm2.org/variabletype/ ",
                                      db_column='variabletypecv',
                                      on_delete=models.CASCADE)
    # variabletypecv = models.ModelChoiceField(CvVariabletype, db_column='variabletypecv')
    variablecode = models.CharField(verbose_name='variable code', max_length=50)
    variable_name = models.ForeignKey(CvVariablename,
                                      help_text="view variable names here "
                                                "http://vocabulary.odm2.org/variablename/",
                                      db_column='variablenamecv',
                                      on_delete=models.CASCADE)
    variabledefinition = models.CharField(verbose_name='variable definition', max_length=500,
                                          blank=True)
    # variabledefinition.name = 'variable_definition'
    speciation = models.ForeignKey(CvSpeciation, db_column='speciationcv', blank=True, null=True,
                                   on_delete=models.CASCADE)
    nodatavalue = models.FloatField(verbose_name='no data value')

    def __str__(self):
        s = "%s" % self.variablecode
        if self.variabledefinition:
            s += " - %s" % self.variabledefinition[:20]
        return s

    class Meta:
        managed = True
        ordering = ('variablecode', 'variable_name',)


            db_table = r'Variables'

            db_table = r'variables'
        verbose_name = 'variable'
