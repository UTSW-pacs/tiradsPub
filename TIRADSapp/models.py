from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class thyroidNoduleStudy(models.Model):
   # MRN, accession ,date
   MRN = models.CharField(max_length=20, default = '')
   accession = models.CharField(max_length=20, default = '')
   datetimeEntry = models.DateTimeField(default=datetime.datetime.now)
   utswId = models.CharField(max_length=20, default = '')
   siteId = models.CharField(max_length=20, default = '')

   # size and location
   Nodule1 = models.BooleanField(default=False)
   Nodule1_location1 = models.CharField(max_length=20, default = '')
   Nodule1_location2 = models.CharField(max_length=20, default = '')
   Nodule1_location3 = models.CharField(max_length=20, default = '')
   Nodule1_location4 = models.CharField(max_length=20, default = '')
   Nodule1_sizeX = models.IntegerField(default=0)
   Nodule1_sizeY = models.IntegerField(default=0)
   Nodule1_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule1_composition = models.IntegerField(default=10)
   Nodule1_echogenicity = models.IntegerField(default=10)
   Nodule1_shape = models.IntegerField(default=10)
   Nodule1_margin = models.IntegerField(default=10)
   Nodule1_cometTail = models.BooleanField(default=False)
   Nodule1_macroCalcification = models.BooleanField(default=False)
   Nodule1_rimCalcification = models.BooleanField(default=False)
   Nodule1_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule1_recScore = models.IntegerField(default=0)

   # size and location
   Nodule2 = models.BooleanField(default=False)
   Nodule2_location1 = models.CharField(max_length=20, default = '')
   Nodule2_location2 = models.CharField(max_length=20, default = '')
   Nodule2_location3 = models.CharField(max_length=20, default = '')
   Nodule2_location4 = models.CharField(max_length=20, default = '')
   Nodule2_sizeX = models.IntegerField(default=0)
   Nodule2_sizeY = models.IntegerField(default=0)
   Nodule2_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule2_composition = models.IntegerField(default=10)
   Nodule2_echogenicity = models.IntegerField(default=10)
   Nodule2_shape = models.IntegerField(default=10)
   Nodule2_margin = models.IntegerField(default=10)
   Nodule2_cometTail = models.BooleanField(default=False)
   Nodule2_macroCalcification = models.BooleanField(default=False)
   Nodule2_rimCalcification = models.BooleanField(default=False)
   Nodule2_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule2_recScore = models.IntegerField(default=0)

   # size and location
   Nodule3 = models.BooleanField(default=False)
   Nodule3_location1 = models.CharField(max_length=20, default = '')
   Nodule3_location2 = models.CharField(max_length=20, default = '')
   Nodule3_location3 = models.CharField(max_length=20, default = '')
   Nodule3_location4 = models.CharField(max_length=20, default = '')
   Nodule3_sizeX = models.IntegerField(default=0)
   Nodule3_sizeY = models.IntegerField(default=0)
   Nodule3_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule3_composition = models.IntegerField(default=10)
   Nodule3_echogenicity = models.IntegerField(default=10)
   Nodule3_shape = models.IntegerField(default=10)
   Nodule3_margin = models.IntegerField(default=10)
   Nodule3_cometTail = models.BooleanField(default=False)
   Nodule3_macroCalcification = models.BooleanField(default=False)
   Nodule3_rimCalcification = models.BooleanField(default=False)
   Nodule3_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule3_recScore = models.IntegerField(default=0)

   # size and location
   Nodule4 = models.BooleanField(default=False)
   Nodule4_location1 = models.CharField(max_length=20, default = '')
   Nodule4_location2 = models.CharField(max_length=20, default = '')
   Nodule4_location3 = models.CharField(max_length=20, default = '')
   Nodule4_location4 = models.CharField(max_length=20, default = '')
   Nodule4_sizeX = models.IntegerField(default=0)
   Nodule4_sizeY = models.IntegerField(default=0)
   Nodule4_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule4_composition = models.IntegerField(default=10)
   Nodule4_echogenicity = models.IntegerField(default=10)
   Nodule4_shape = models.IntegerField(default=10)
   Nodule4_margin = models.IntegerField(default=10)
   Nodule4_cometTail = models.BooleanField(default=False)
   Nodule4_macroCalcification = models.BooleanField(default=False)
   Nodule4_rimCalcification = models.BooleanField(default=False)
   Nodule4_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule4_recScore = models.IntegerField(default=0)
   def __str__(self):
      return self.MRN

class thyroidNoduleStudy_phhs(models.Model):
   # MRN, accession ,date
   MRN = models.CharField(max_length=20, default = '')
   accession = models.CharField(max_length=20, default = '')
   datetimeEntry = models.DateTimeField(default=datetime.datetime.now)
   phhsId = models.CharField(max_length=20, default = '')
   siteId = models.CharField(max_length=20, default = '')

   # size and location
   Nodule1 = models.BooleanField(default=False)
   Nodule1_location1 = models.CharField(max_length=20, default = '')
   Nodule1_location2 = models.CharField(max_length=20, default = '')
   Nodule1_location3 = models.CharField(max_length=20, default = '')
   Nodule1_location4 = models.CharField(max_length=20, default = '')
   Nodule1_sizeX = models.IntegerField(default=0)
   Nodule1_sizeY = models.IntegerField(default=0)
   Nodule1_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule1_composition = models.IntegerField(default=10)
   Nodule1_echogenicity = models.IntegerField(default=10)
   Nodule1_shape = models.IntegerField(default=10)
   Nodule1_margin = models.IntegerField(default=10)
   Nodule1_cometTail = models.BooleanField(default=False)
   Nodule1_macroCalcification = models.BooleanField(default=False)
   Nodule1_rimCalcification = models.BooleanField(default=False)
   Nodule1_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule1_recScore = models.IntegerField(default=0)

   # size and location
   Nodule2 = models.BooleanField(default=False)
   Nodule2_location1 = models.CharField(max_length=20, default = '')
   Nodule2_location2 = models.CharField(max_length=20, default = '')
   Nodule2_location3 = models.CharField(max_length=20, default = '')
   Nodule2_location4 = models.CharField(max_length=20, default = '')
   Nodule2_sizeX = models.IntegerField(default=0)
   Nodule2_sizeY = models.IntegerField(default=0)
   Nodule2_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule2_composition = models.IntegerField(default=10)
   Nodule2_echogenicity = models.IntegerField(default=10)
   Nodule2_shape = models.IntegerField(default=10)
   Nodule2_margin = models.IntegerField(default=10)
   Nodule2_cometTail = models.BooleanField(default=False)
   Nodule2_macroCalcification = models.BooleanField(default=False)
   Nodule2_rimCalcification = models.BooleanField(default=False)
   Nodule2_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule2_recScore = models.IntegerField(default=0)

   # size and location
   Nodule3 = models.BooleanField(default=False)
   Nodule3_location1 = models.CharField(max_length=20, default = '')
   Nodule3_location2 = models.CharField(max_length=20, default = '')
   Nodule3_location3 = models.CharField(max_length=20, default = '')
   Nodule3_location4 = models.CharField(max_length=20, default = '')
   Nodule3_sizeX = models.IntegerField(default=0)
   Nodule3_sizeY = models.IntegerField(default=0)
   Nodule3_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule3_composition = models.IntegerField(default=10)
   Nodule3_echogenicity = models.IntegerField(default=10)
   Nodule3_shape = models.IntegerField(default=10)
   Nodule3_margin = models.IntegerField(default=10)
   Nodule3_cometTail = models.BooleanField(default=False)
   Nodule3_macroCalcification = models.BooleanField(default=False)
   Nodule3_rimCalcification = models.BooleanField(default=False)
   Nodule3_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule3_recScore = models.IntegerField(default=0)

   # size and location
   Nodule4 = models.BooleanField(default=False)
   Nodule4_location1 = models.CharField(max_length=20, default = '')
   Nodule4_location2 = models.CharField(max_length=20, default = '')
   Nodule4_location3 = models.CharField(max_length=20, default = '')
   Nodule4_location4 = models.CharField(max_length=20, default = '')
   Nodule4_sizeX = models.IntegerField(default=0)
   Nodule4_sizeY = models.IntegerField(default=0)
   Nodule4_sizeZ = models.IntegerField(default=0)
   # characteristics. Note 10 is an impossible option.
   Nodule4_composition = models.IntegerField(default=10)
   Nodule4_echogenicity = models.IntegerField(default=10)
   Nodule4_shape = models.IntegerField(default=10)
   Nodule4_margin = models.IntegerField(default=10)
   Nodule4_cometTail = models.BooleanField(default=False)
   Nodule4_macroCalcification = models.BooleanField(default=False)
   Nodule4_rimCalcification = models.BooleanField(default=False)
   Nodule4_punctateCalcification = models.BooleanField(default=False)
   # tiradsScore
   Nodule4_recScore = models.IntegerField(default=0)   
