#!/usr/bin/env python3
import sys
import urllib.request as request
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from odm2admin.models import CvActionType, CvAggregationStatistic, CvAnnotationType, CvCensorCode, CvDataQualityType,\
    CvDatasetType, CvDirectiveType, CvElevationDatum, CvEquipmentType, CvMedium, CvMethodType, CvOrganizationType,\
    CvPropertyDataType, CvQualityCode, CvReferenceMaterialMedium, CvRelationshipType, CvResultType,\
    CvSamplingFeatureGeoType, CvSamplingFeatureType,CvSiteType, CvSpatialOffsetType, CvSpeciation, CvSpecimenMedium,\
    CvSpecimenType, CvStatus, CvTaxonomicClassifierType, CvUnitsType, CvVariableType, CvVariableName


class Command(BaseCommand):
    help = "Populate Controlled Vocabulary Tables"

    @staticmethod
    def cv_load():
        vocab = [("actionType", CvActionType),
                 ("qualityCode", CvQualityCode),
                 ("samplingFeatureGeoType", CvSamplingFeatureGeoType),
                 ("elevationDatum", CvElevationDatum),
                 ("resultType", CvResultType),
                 ("speciation", CvSpeciation),
                 ("aggregationStatistic", CvAggregationStatistic),
                 ("methodType", CvMethodType),
                 ("taxonomicClassifierType", CvTaxonomicClassifierType),
                 ("siteType", CvSiteType),
                 ("censorCode", CvCensorCode),
                 ("directiveType", CvDirectiveType),
                 ("datasetType",CvDatasetType),
                 ("dataQualityType",CvDataQualityType),
                 ("organizationType", CvOrganizationType),
                 ("status", CvStatus),
                 ("annotationType", CvAnnotationType),
                 ("samplingFeatureType", CvSamplingFeatureType),
                 ("equipmentType", CvEquipmentType),
                 ("specimenMedium", CvSpecimenMedium),
                 ("spatialOffsetType", CvSpatialOffsetType),
                 ("referenceMaterialMedium", CvReferenceMaterialMedium),
                 ("specimenType", CvSpecimenType),
                 ("variableType", CvVariableType),
                 ("variableName", CvVariableName),
                 ("propertyDataType", CvPropertyDataType),
                 ("relationshipType", CvRelationshipType),
                 ("unitsType", CvUnitsType),
                 ("medium", CvMedium)
                 ]

        url = "http://vocabulary.odm2.org/api/v1/%s/?format=skos"

        # XML encodings
        dc = "{http://purl.org/dc/elements/1.1/}%s"
        rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}%s"
        skos = "{http://www.w3.org/2004/02/skos/core#}%s"
        odm2 = "{http://vocabulary.odm2.org/ODM2/ODM2Terms/}%s"

        for (key, value) in enumerate(vocab):
            try:
                data = request.urlopen(url % key).read()
                root = ET.fromstring(data)
                cv_object = value
                objs = []
                for voc in root.findall(rdf % "Description"):
                    obj = cv_object()
                    try:
                        obj.term = voc.attrib[rdf % "about"].split('/')[-1]
                        obj.name = voc.find(skos % "prefLabel").text
                        obj.definition = voc.find(skos % "definition").text.encode('unicode_escape') if voc.find(skos % "definition") is not None else None
                        obj.category = voc.find(odm2 % "category").text if voc.find(odm2 % "category") is not None else None
                        obj.sourceVocabularyURI = voc.attrib[rdf % "about"]
                        objs.append(obj)
                    except Exception as e:
                        objs.roll
                        if obj.Name is not None:
                            print("issue loading single object %s: %s " %(obj.Name, e))
                        pass
                session.add_all(objs)
                if not args.debug:
                   session.commit()
            except Exception as e:
                session.rollback()
                if "Duplicate entry" in e.message:
                    e = "Controlled Vocabulary has already been loaded"
                print("\t...%s Load was unsuccesful: \n%s" % (key, e))
                sys.stdout.write("\n\n... %sLoad was unsuccessful: %s\r"%(key,e))
                sys.stdout.flush()

        update_progress(len(vocab), "CV_Terms")
        sys.stdout.write("\nCV Load has completed\r\n")
        sys.stdout.flush()

