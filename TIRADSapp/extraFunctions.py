from .models import thyroidNoduleStudy
from .models import thyroidNoduleStudy_phhs
#from .decryptFunctions import *
import re
import math

def saveToDatabase(request):
   # if no mrn or accession, just return to prevent error in saving


   if request.session['siteId'] == 'utsw':
       newStudy = thyroidNoduleStudy()
   else:
       newStudy = thyroidNoduleStudy_phhs()

   # MRN, accession ,date
   newStudy.MRN = request.session['mrn']
   newStudy.accession = request.session['accession']
   newStudy.utswId = request.session['userId']
   newStudy.siteId = request.session['siteId']
   noduleList = request.session['noduleList']

   # size and location
   nodule1 = noduleList[0]
   newStudy.Nodule1_location1 = nodule1['location1']
   newStudy.Nodule1_location2 = nodule1['location2']
   newStudy.Nodule1_location3 = nodule1['location3']
   newStudy.Nodule1_location4 = nodule1['location4']
   newStudy.Nodule1_sizeX = nodule1['sizeX']
   newStudy.Nodule1_sizeY = nodule1['sizeY']
   newStudy.Nodule1_sizeZ = nodule1['sizeZ']
   # characteristics. Note 10 is an impossible option.
   newStudy.Nodule1_composition = nodule1['composition']
   newStudy.Nodule1_echogenicity = nodule1['echogenicity']
   newStudy.Nodule1_shape = nodule1['shape']
   newStudy.Nodule1_margin = nodule1['margin']
   newStudy.Nodule1_cometTail = nodule1['cometTail']
   newStudy.Nodule1_macroCalcification = nodule1['macroCalcification']
   newStudy.Nodule1_rimCalcification = nodule1['rimCalcification']
   newStudy.Nodule1_punctateCalcification = nodule1['punctateCalcification']
   # tiradsScore
   newStudy.Nodule1_recScore = nodule1['recScore']

   # size and location
   nodule2 = noduleList[1]
   newStudy.Nodule2_location1 = nodule2['location1']
   newStudy.Nodule2_location2 = nodule2['location2']
   newStudy.Nodule2_location3 = nodule2['location3']
   newStudy.Nodule2_location4 = nodule2['location4']
   newStudy.Nodule2_sizeX = nodule2['sizeX']
   newStudy.Nodule2_sizeY = nodule2['sizeY']
   newStudy.Nodule2_sizeZ = nodule2['sizeZ']
   # characteristics. Note 10 is an impossible option.
   newStudy.Nodule2_composition = nodule2['composition']
   newStudy.Nodule2_echogenicity = nodule2['echogenicity']
   newStudy.Nodule2_shape = nodule2['shape']
   newStudy.Nodule2_margin = nodule2['margin']
   newStudy.Nodule2_cometTail = nodule2['cometTail']
   newStudy.Nodule2_macroCalcification = nodule2['macroCalcification']
   newStudy.Nodule2_rimCalcification = nodule2['rimCalcification']
   newStudy.Nodule2_punctateCalcification = nodule2['punctateCalcification']
   # tiradsScore
   newStudy.Nodule2_recScore = nodule2['recScore']

   # size and location
   nodule3 = noduleList[2]
   newStudy.Nodule3_location1 = nodule3['location1']
   newStudy.Nodule3_location2 = nodule3['location2']
   newStudy.Nodule3_location3 = nodule3['location3']
   newStudy.Nodule3_location4 = nodule3['location4']
   newStudy.Nodule3_sizeX = nodule3['sizeX']
   newStudy.Nodule3_sizeY = nodule3['sizeY']
   newStudy.Nodule3_sizeZ = nodule3['sizeZ']
   # characteristics. Note 10 is an impossible option.
   newStudy.Nodule3_composition = nodule3['composition']
   newStudy.Nodule3_echogenicity = nodule3['echogenicity']
   newStudy.Nodule3_shape = nodule3['shape']
   newStudy.Nodule3_margin = nodule3['margin']
   newStudy.Nodule3_cometTail = nodule3['cometTail']
   newStudy.Nodule3_macroCalcification = nodule3['macroCalcification']
   newStudy.Nodule3_rimCalcification = nodule3['rimCalcification']
   newStudy.Nodule3_punctateCalcification = nodule3['punctateCalcification']
   # tiradsScore
   newStudy.Nodule3_recScore = nodule3['recScore']

   # size and location
   nodule4 = noduleList[3]
   newStudy.Nodule4_location1 = nodule4['location1']
   newStudy.Nodule4_location2 = nodule4['location2']
   newStudy.Nodule4_location3 = nodule4['location3']
   newStudy.Nodule4_location4 = nodule4['location4']
   newStudy.Nodule4_sizeX = nodule4['sizeX']
   newStudy.Nodule4_sizeY = nodule4['sizeY']
   newStudy.Nodule4_sizeZ = nodule4['sizeZ']
   # characteristics. Note 10 is an impossible option.
   newStudy.Nodule4_composition = nodule4['composition']
   newStudy.Nodule4_echogenicity = nodule4['echogenicity']
   newStudy.Nodule4_shape = nodule4['shape']
   newStudy.Nodule4_margin = nodule4['margin']
   newStudy.Nodule4_cometTail = nodule4['cometTail']
   newStudy.Nodule4_macroCalcification = nodule4['macroCalcification']
   newStudy.Nodule4_rimCalcification = nodule4['rimCalcification']
   newStudy.Nodule4_punctateCalcification = nodule4['punctateCalcification']
   # tiradsScore
   newStudy.Nodule4_recScore = nodule4['recScore']

   newStudy.save()
   return

def computeFindingsForNodule(tempNodule):
   findingsText = ''
   if checkNoduleCompletion(tempNodule):
      findingsText = findingsText + 'Location: '
      findingsText = findingsText + computeLocationString(tempNodule)
      findingsText = findingsText + computeSizeString(tempNodule)
      findingsText += 'Description: '
      findingsText = findingsText + computeCompositionString(tempNodule)
      findingsText = findingsText + computeEchogenicityString(tempNodule)
      findingsText = findingsText + computeShapeString(tempNodule)
      findingsText = findingsText + computeMarginString(tempNodule)
      findingsText = findingsText + computeEchogenicFociString(tempNodule)
   else:
      findingsText = 'Fields are incomplete.'
   return findingsText

def computeLocationString(tempNodule):
   findingsText = ''
   if tempNodule['location2']:
      findingsText = findingsText + tempNodule['location2'] + ', '
   if tempNodule['location3']:
      findingsText = findingsText + tempNodule['location3'] + ', '
   if tempNodule['location4']:
      findingsText = findingsText + tempNodule['location4'] + ', '
   findingsText = findingsText + tempNodule['location1']
   if tempNodule['location1'] == 'isthmus':
      findingsText += '. '
   else:
      findingsText += ' lobe. '
   return findingsText

def computeSizeString(tempNodule):
   size = []
   if int(tempNodule['sizeX']):
      size.append(tempNodule['sizeX'])
   if int(tempNodule['sizeY']):
      size.append(tempNodule['sizeY'])
   if int(tempNodule['sizeZ']):
      size.append(tempNodule['sizeZ'])

   sizeString='Size: '
   if len(size) == 0:
      sizeString = sizeString + 'NA, '
   elif len(size)==1:
      sizeString = sizeString + size[0] + ' mm. '
   else:
      sizeString = sizeString + size[0]
      for i in range(1,len(size)):
         sizeString = sizeString + ' x ' + size[i]
      sizeString = sizeString + ' mm. '
   return sizeString

def computeCompositionString(tempNodule):
   options = {   '0': 'cystic, ',
         '1': 'almost completely cystic, ',
         '2': 'spongiform, ',
         '3': 'mixed cystic and solid, ',
         '4': 'almost completely solid, ',
         '5': 'solid, ',
         '6': 'composition obscured by calcification, '}
   findingsText = options[tempNodule['composition']]
   return findingsText

def computeEchogenicityString(tempNodule):
   options = {   '0': 'anechoic, ',
         '1': 'solid component is hyperechoic, ',
         '2': 'solid component is isoechoic, ',
         '3': 'solid component is hypoechoic, ',
         '4': 'solid component is very hypoechoic, ',
         '5': 'echogenicity cannot be determined, ',}
   findingsText = options[tempNodule['echogenicity']]
   return findingsText

def computeShapeString(tempNodule):
   options = {   '0': '','1': 'not taller-than-wide, ', '2':'taller-than-wide, '}
   findingsText = options[tempNodule['shape']]
   return findingsText

def computeMarginString(tempNodule):
   options = {   '0': 'smooth margins, ',
         '1': 'ill-defined margins, ',
         '2': 'lobulated margins, ',
         '3': 'irregular margins, ',
         '4': 'extra-thyroidal extension, ',
         '5': 'margins cannot be determined, ',}
   findingsText = options[tempNodule['margin']]
   return findingsText

def computeEchogenicFociString(tempNodule):
   echoFoci = []
   if tempNodule['cometTail']:
      echoFoci.append('comet-tail artifacts')
   if tempNodule['macroCalcification']:
      echoFoci.append('macrocalcification')
   if tempNodule['rimCalcification']:
      echoFoci.append('peripheral (rim) calcifications')
   if tempNodule['punctateCalcification']:
      echoFoci.append('punctate echogenic foci')

   if len(echoFoci) == 0:
      return 'without suspicious echogenic foci. '
   else:
      findingsText=''
      for text in echoFoci:
         findingsText = findingsText + ', ' + text
      findingsText = findingsText[2:]
      return 'with ' + findingsText + '. '

def calcRecScore(tempNodule):
   size =  max(int(tempNodule['sizeX']), int(tempNodule['sizeY']), int(tempNodule['sizeZ']))
   score = calcScore(tempNodule)
   if score == 0 or score == 1:
      return '1'
   elif score == 2:
      return '2'
   elif score == 3:
      if size >= 25:
         return '9'
      elif size >= 15:
         return '6'
      else:
         return '3'
   elif score >=4 and score <=6:
      if size >= 15:
         return '10'
      elif size >= 10:
         return '7'
      else:
         return '4'
   else:
      if size >= 10:
         return '11'
      elif size >= 5:
         return '8'
      else:
         return '5'

def calcScore(tempNodule):
   scoreComposition = {'0': 0, '1': 0, '2': 0, '3': 1, '4': 2, '5': 2, '6': 2}
   scoreEchogenicity = {'0': 0, '1': 1, '2': 1, '3': 2, '4': 3, '5': 1}
   scoreShape = {'0': 0, '1': 0, '2':3,}
   scoreMargin = {'0': 0, '1': 0, '2': 2, '3': 2, '4': 3, '5': 0}

   totalScore = scoreComposition[tempNodule['composition']] + scoreEchogenicity[tempNodule['echogenicity']] + scoreShape[tempNodule['shape']] + scoreMargin[tempNodule['margin']]
   if tempNodule['macroCalcification']:
      totalScore = totalScore + 1
   if tempNodule['rimCalcification']:
      totalScore = totalScore + 2
   if tempNodule['punctateCalcification']:
      totalScore = totalScore + 3

   # idiosyncracy - if spongiform then is benign...
   if tempNodule['composition'] == '2':
      totalScore = 0

   return totalScore

def checkNoduleCompletion(tempNodule):
   completion = True
   if tempNodule['location1']=='':
      completion = False
   size = int(tempNodule['sizeX']) + int(tempNodule['sizeY']) + int(tempNodule['sizeZ'])
   if size == 0:
      completion = False
   if tempNodule['composition'] == '10':
      completion = False
   if tempNodule['echogenicity'] == '10':
      completion = False
   if tempNodule['shape'] == '10':
      completion = False
   if tempNodule['margin'] == '10':
      completion = False
   return completion

def generateContextDefaults(tempNodule):
   defaultContext = {'button1':'', 'button2':'', 'button3':'', 'button4':'',
                     'element111':'','element112':'','element113':'',
                     'element121':'','element122':'','element123':'',
                     'element131':'','element132':'',
                     'element141':'','element142':'',
                     'element21':'','element22':'','element23':'',
                     'element30':'','element31':'','element32':'','element33':'','element34':'','element35':'','element36':'',
                     'element40':'','element41':'','element42':'','element43':'','element44':'','element45':'',
                     'element50':'','element51':'','element52':'',
                     'element60':'','element61':'','element62':'','element63':'','element64':'','element65':'',
                     'element70':'','element71':'','element72':'','element73':'','element74':'',}

   if tempNodule['location1']=='right':
      defaultContext['element111']='checked="checked"'
   if tempNodule['location1']=='left':
      defaultContext['element112']='checked="checked"'
   if tempNodule['location1']=='isthmus':
      defaultContext['element113']='checked="checked"'

   if tempNodule['location2']=='upper':
      defaultContext['element121']='checked="checked"'
   if tempNodule['location2']=='mid':
      defaultContext['element122']='checked="checked"'
   if tempNodule['location2']=='lower':
      defaultContext['element123']='checked="checked"'

   if tempNodule['location3']=='lateral':
      defaultContext['element131']='checked="checked"'
   if tempNodule['location3']=='medial':
      defaultContext['element132']='checked="checked"'

   if tempNodule['location4']=='anterior':
      defaultContext['element141']='checked="checked"'
   if tempNodule['location4']=='posterior':
      defaultContext['element142']='checked="checked"'

   defaultContext['element21']=str(tempNodule['sizeX'])
   defaultContext['element22']=str(tempNodule['sizeY'])
   defaultContext['element23']=str(tempNodule['sizeZ'])

   if tempNodule['composition']=='0':
      defaultContext['element30']='checked="checked"'
   if tempNodule['composition']=='1':
      defaultContext['element31']='checked="checked"'
   if tempNodule['composition']=='2':
      defaultContext['element32']='checked="checked"'
   if tempNodule['composition']=='3':
      defaultContext['element33']='checked="checked"'
   if tempNodule['composition']=='4':
      defaultContext['element34']='checked="checked"'
   if tempNodule['composition']=='5':
      defaultContext['element35']='checked="checked"'
   if tempNodule['composition']=='6':
      defaultContext['element36']='checked="checked"'

   if tempNodule['echogenicity']=='0':
      defaultContext['element40']='checked="checked"'
   if tempNodule['echogenicity']=='1':
      defaultContext['element41']='checked="checked"'
   if tempNodule['echogenicity']=='2':
      defaultContext['element42']='checked="checked"'
   if tempNodule['echogenicity']=='3':
      defaultContext['element43']='checked="checked"'
   if tempNodule['echogenicity']=='4':
      defaultContext['element44']='checked="checked"'
   if tempNodule['echogenicity']=='5':
      defaultContext['element45']='checked="checked"'

   if tempNodule['shape']=='0':
      defaultContext['element50']='checked="checked"'
   if tempNodule['shape']=='1':
      defaultContext['element51']='checked="checked"'
   if tempNodule['shape']=='2':
      defaultContext['element52']='checked="checked"'

   if tempNodule['margin']=='0':
      defaultContext['element60']='checked="checked"'
   if tempNodule['margin']=='1':
      defaultContext['element61']='checked="checked"'
   if tempNodule['margin']=='2':
      defaultContext['element62']='checked="checked"'
   if tempNodule['margin']=='3':
      defaultContext['element63']='checked="checked"'
   if tempNodule['margin']=='4':
      defaultContext['element64']='checked="checked"'
   if tempNodule['margin']=='5':
      defaultContext['element65']='checked="checked"'

   if tempNodule['noFoci']:
      defaultContext['element70']='checked="checked"'
   if tempNodule['cometTail']:
      defaultContext['element71']='checked="checked"'
   if tempNodule['macroCalcification']:
      defaultContext['element72']='checked="checked"'
   if tempNodule['rimCalcification']:
      defaultContext['element73']='checked="checked"'
   if tempNodule['punctateCalcification']:
      defaultContext['element74']='checked="checked"'

   return defaultContext

def initializeNodule():
   tempNodule = { 'location1':'',
                  'location2':'',
                  'location3':'',
                  'location4':'',
                  'sizeX':'0',
                  'sizeY':'0',
                  'sizeZ':'0',
                  'composition':'10',
                  'echogenicity':'10',
                  'shape':'10',
                  'margin':'10',
                  'noFoci':False,
                  'cometTail':False,
                  'macroCalcification':False,
                  'rimCalcification':False,
                  'punctateCalcification':False,
                  'recScore':'0',}
   return tempNodule
