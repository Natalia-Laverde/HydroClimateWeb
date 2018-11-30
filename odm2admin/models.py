import re
import uuid
from django.db import models
from urllib.parse import urlparse
from django.core import management


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
        type = None
        if str(self.propertyValue).__len__() > 0:
            if str(
                    self.propertyId) == 'Citation Category - Paper, Book, Talk, Poster, ' \
                                        'Dissertation, Thesis, Undergrad Thesis, Report':
                if str(self.propertyValue) == 'Paper':
                    type = "Paper"
                if str(self.propertyValue) == 'Book':
                    type = "Book"
                if str(self.propertyValue) == 'Talk':
                    type = "Conference"
                if str(self.propertyValue) == 'Poster':
                    type = "Poster"
                if str(self.propertyValue) == 'Dissertation' or str(
                        self.propertyValue) == 'Thesis' or str(self.propertyValue) == 'Undergrad Thesis':
                    type = "Thesis"
                if str(self.propertyValue) == 'Report':
                    type = "Report"
        return type

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
            management.call_command('update_preprocess_process_datalogger_file', link_name, str(file_id)
                                    , str(self.dataBeginsOn), str(self.columnHeadersOn),
                                    str(ftp_frequency_hours), False)
        else:
            management.call_command('ProcessDataLoggerFile', link_name, str(file_id)
                                    , str(self.dataBeginsOn), str(self.columnHeadersOn),
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


