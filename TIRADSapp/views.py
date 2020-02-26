from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.utils.timezone import datetime as dt
from django.contrib import messages

#from .models import thyroidNodule 1
from .models import thyroidNoduleStudy
from .extraFunctions import *
from operator import itemgetter
#from .decryptFunctions import *

import json
import requests
import re
import datetime
import math
import xml.etree.ElementTree as ET

# Create your views here.



def psApi(request, accession, findings, impression):
    username = '###'
    password = '####'

    url = 'http://hostname.site.org/###/###/auth.asmx/SignIn?systemID=1&accessCode=&username=' + str(username) + '&password=' + str(password)
    s = requests.session()
    r = s.get(url)
    apiresponse = r.status_code
    apireason = r.reason
    #print (resp['reportID'])

    r2 = s.get('http://hostname.site.org/###/###/explorer.asmx/SearchByAccession?site=UTSWMC&accessions='+str(accession)+'&sort=')
    apir2 = r2.status_code
    root = ET.fromstring(r2.text)
    repID = root[0][1].text
    #findings api post
    fpayload = {'reportID': repID, 'name': 'tirads_findings', 'value': findings, 'merge': 'true'}
    fpost = s.get('http://hostname.site.org/###/###/customfield.asmx/SetReportCustomFieldByName', params=fpayload)
    #impression api post
    ipayload = {'reportID': repID, 'name': 'tirads_impression', 'value': impression, 'merge': 'true'}
    ipost = s.get('http://hostname.site.org/###/###/customfield.asmx/SetReportCustomFieldByName', params=ipayload)

    fStatus = fpost.status_code
    iStatus = ipost.status_code

    #if fStatus == '200':

    #return render(request, 'TIRADSappTemplate2.html')


def calcTIRADSscore(request):
   #Decrypt Url String
   '''
   pathInfo = request.META['PATH_INFO']
   data = pathInfo
   data = pathInfo[8:-1]
   key = '######'
   iv = '\0' * 16
   dec = decryptor(key,iv)
   byte = dec(data)
   plain = str(byte, 'utf-8')
   pt = re.split('[./]', plain)
   '''
   pt = ['123', '456', '12345', '999999', 'UTSW']
   mrn = pt[0]
   accession = pt[1]
   request.session['userId'] = pt[2]
   request.session['timeStamp'] = pt[3]
   request.session['siteId'] = pt[4]

   #DateTime
   linkDateTime = request.session['timeStamp']
   #dtm = datetime.datetime.strptime(linkDateTime, '%Y%m%d%H%M%S')
   currentTime = datetime.datetime.now()
   #diff = currentTime - dtm
   #diffInSeconds = diff.total_seconds()

   context = mainComputer(request, mrn, accession)
   template = loader.get_template('TIRADSappTemplate2.html')
   '''
   if diffInSeconds > 1800:
      deny = "The link that you are using has EXPIRED.  Please regenerate the link from Epic Workspace to use the TIRADS App Calculator"
      return HttpResponse(deny)
   else:
   '''
   return HttpResponse(template.render(context, request))


def mainComputer(request, mrn, accession):
   # get global variables within scope
   context = {'findings':'','impression':''}
   if request.method == 'GET':
      context.update(fetchAndContextForGet(request, mrn, accession))
      return context
   elif request.method == 'POST':
      if request.POST.get('submit'):
         context.update(processAndContextForSubmit(request))
      elif request.POST.get('reset'):
         request.session['noduleList'] = [initializeNodule(), initializeNodule(), initializeNodule(), initializeNodule()]
         request.session['noduleHasBeenClicked'] = [True, False, False, False]
         request.session['nodIndex'] = 0
         noduleList = request.session['noduleList']
         nodHasBeenClicked = request.session['noduleHasBeenClicked']
         nodIndex = request.session['nodIndex']
         context.update(generateContextDefaults(noduleList[nodIndex]))
         tempKey = 'button' + str(nodIndex+1)
         context[tempKey] = 'active'
      elif request.POST.get('save'):
         tempcontext = processAndContextForSubmit(request)
         context.update(tempcontext)
         tempfindings = tempcontext['findings']
         tempimpression = tempcontext['impression']
         tempacc = request.session['accession']
         saveToDatabase(request)
         #transmit to powerscribe
         psApi(request, tempacc, tempfindings, tempimpression)


      elif request.POST.get('button1'):
         context.update(processAndContextForButton(request, 1))
      elif request.POST.get('button2'):
         context.update(processAndContextForButton(request, 2))
      elif request.POST.get('button3'):
         context.update(processAndContextForButton(request, 3))
      elif request.POST.get('button4'):
         context.update(processAndContextForButton(request, 4))
      else:
         context=generateContextForComputer(request)
         tempKey = 'button' + str(nodIndex+1)
         context[tempKey] = 'active'
   request.session.modified = True
   return context

def fetchAndContextForGet(request, objMrn, objAccession):
   context = {}
   request.session.set_expiry(3600)
   request.session['mrn']=objMrn
   request.session['accession']=objAccession
   request.session['noduleList'] = [initializeNodule(), initializeNodule(), initializeNodule(), initializeNodule()]
   request.session['noduleHasBeenClicked'] = [True, False, False, False]
   request.session['nodIndex'] = 0
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   # Retrive most recent prior study from database
   studyList = thyroidNoduleStudy.objects.filter(MRN=objMrn).order_by('datetimeEntry')
   if len(studyList)>0:
      oldStudy=studyList[len(studyList)-1]
      # Copy inputs from old study
      nodule1 = noduleList[0]
      nodule1['location1']=oldStudy.Nodule1_location1
      nodule1['location2']=oldStudy.Nodule1_location2
      nodule1['location3']=oldStudy.Nodule1_location3
      nodule1['location4']=oldStudy.Nodule1_location4
      nodule1['sizeX']=str(oldStudy.Nodule1_sizeX)
      nodule1['sizeY']=str(oldStudy.Nodule1_sizeY)
      nodule1['sizeZ']=str(oldStudy.Nodule1_sizeZ)
      nodule1['composition']=str(oldStudy.Nodule1_composition)
      nodule1['echogenicity']=str(oldStudy.Nodule1_echogenicity)
      nodule1['shape']=str(oldStudy.Nodule1_shape)
      nodule1['margin']=str(oldStudy.Nodule1_margin)
      nodule1['cometTail']=oldStudy.Nodule1_cometTail
      nodule1['macroCalcification']=oldStudy.Nodule1_macroCalcification
      nodule1['rimCalcification']=oldStudy.Nodule1_rimCalcification
      nodule1['punctateCalcification']=oldStudy.Nodule1_punctateCalcification
      nodule2 = noduleList[1]
      nodule2['location1']=oldStudy.Nodule2_location1
      nodule2['location2']=oldStudy.Nodule2_location2
      nodule2['location3']=oldStudy.Nodule2_location3
      nodule2['location4']=oldStudy.Nodule2_location4
      nodule2['sizeX']=str(oldStudy.Nodule2_sizeX)
      nodule2['sizeY']=str(oldStudy.Nodule2_sizeY)
      nodule2['sizeZ']=str(oldStudy.Nodule2_sizeZ)
      nodule2['composition']=str(oldStudy.Nodule2_composition)
      nodule2['echogenicity']=str(oldStudy.Nodule2_echogenicity)
      nodule2['shape']=str(oldStudy.Nodule2_shape)
      nodule2['margin']=str(oldStudy.Nodule2_margin)
      nodule2['cometTail']=oldStudy.Nodule2_cometTail
      nodule2['macroCalcification']=oldStudy.Nodule2_macroCalcification
      nodule2['rimCalcification']=oldStudy.Nodule2_rimCalcification
      nodule2['punctateCalcification']=oldStudy.Nodule2_punctateCalcification
      nodule3 = noduleList[2]
      nodule3['location1']=oldStudy.Nodule3_location1
      nodule3['location2']=oldStudy.Nodule3_location2
      nodule3['location3']=oldStudy.Nodule3_location3
      nodule3['location4']=oldStudy.Nodule3_location4
      nodule3['sizeX']=str(oldStudy.Nodule3_sizeX)
      nodule3['sizeY']=str(oldStudy.Nodule3_sizeY)
      nodule3['sizeZ']=str(oldStudy.Nodule3_sizeZ)
      nodule3['composition']=str(oldStudy.Nodule3_composition)
      nodule3['echogenicity']=str(oldStudy.Nodule3_echogenicity)
      nodule3['shape']=str(oldStudy.Nodule3_shape)
      nodule3['margin']=str(oldStudy.Nodule3_margin)
      nodule3['cometTail']=oldStudy.Nodule3_cometTail
      nodule3['macroCalcification']=oldStudy.Nodule3_macroCalcification
      nodule3['rimCalcification']=oldStudy.Nodule3_rimCalcification
      nodule3['punctateCalcification']=oldStudy.Nodule3_punctateCalcification
      nodule4 = noduleList[3]
      nodule4['location1']=oldStudy.Nodule4_location1
      nodule4['location2']=oldStudy.Nodule4_location2
      nodule4['location3']=oldStudy.Nodule4_location3
      nodule4['location4']=oldStudy.Nodule4_location4
      nodule4['sizeX']=str(oldStudy.Nodule4_sizeX)
      nodule4['sizeY']=str(oldStudy.Nodule4_sizeY)
      nodule4['sizeZ']=str(oldStudy.Nodule4_sizeZ)
      nodule4['composition']=str(oldStudy.Nodule4_composition)
      nodule4['echogenicity']=str(oldStudy.Nodule4_echogenicity)
      nodule4['shape']=str(oldStudy.Nodule4_shape)
      nodule4['margin']=str(oldStudy.Nodule4_margin)
      nodule4['cometTail']=oldStudy.Nodule4_cometTail
      nodule4['macroCalcification']=oldStudy.Nodule4_macroCalcification
      nodule4['rimCalcification']=oldStudy.Nodule4_rimCalcification
      nodule4['punctateCalcification']=oldStudy.Nodule4_punctateCalcification
   context.update(generateContextDefaults(noduleList[nodIndex]))
   context.update(generateContextMRN(request))
   tempKey = 'button' + str(nodIndex+1)
   context[tempKey] = 'active'
   request.session.modified = True
   return context

def generateContextMRN(request):
   today = dt.today()

   if request.session['mrn'] == '0' or request.session['accession'] == '0':
      contextPtInfo = { 'mrn': mrn,
                     'accession':'NA',
                     'date':today.strftime('%m-%d-%Y')}
   else:
      contextPtInfo = { 'mrn': request.session['mrn'],
                        'accession': request.session['accession'],
                        'date':today.strftime('%m-%d-%Y'),
                        'pathInfo':request.META['PATH_INFO'],
                        'userId': request.session['userId'],
                        'timeStamp': request.session['timeStamp'],
                        'siteId': request.session['siteId'] }
   return contextPtInfo

def processAndContextForButton(request, button):
   index = button-1
   # 1) process inputs
   processInputs(request)
   # 2) update new current nodule nodIndex
   request.session['nodIndex'] = index
   request.session['noduleHasBeenClicked'][index] = True
   # 3) render context (button pressed)
      # grab handlers
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
      # generate context for findings and impression
   computeScores(request)
   context = {'findings':computeFindings(request),'impression':computeImpressions(request)}
      # generate context for selected nodule (i.e. display saved entries)
   context.update(generateContextDefaults(noduleList[nodIndex]))
      # generate context for nodule button (i.e. display page for which nodule)
   tempKey = 'button' + str(index+1)
   context[tempKey] = 'active'
      # generate context for mrn and accession number
   context.update(generateContextMRN(request))
   return context

def processAndContextForSubmit(request):
   # process inputs
   processInputs(request)
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   computeScores(request)
   context = {'findings':computeFindings(request),'impression':computeImpressions(request)}
   context.update(generateContextDefaults(noduleList[nodIndex]))
   tempKey = 'button' + str(nodIndex+1)
   context[tempKey] = 'active'
   context.update(generateContextMRN(request))
   return context

def computeScores(request):
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   for index in range(0,len(noduleList)):
      if checkNoduleCompletion(noduleList[index]):
         noduleList[index]['recScore']=calcRecScore(noduleList[index])
   return

def computeFindings(request):
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   findingsText = ''
   for index in range(0,len(noduleList)):
      if noduleList[index]['recScore'] != '0':
         findingsText = findingsText + '-Nodule ' + str(index+1) +': '
         findingsText = findingsText + computeFindingsForNodule(noduleList[index])
         findingsText += 'ACR TI-RADS: '
         findingsText += trStatementFor(noduleList[index])
         findingsText += recommendationStatementFor(noduleList[index])
         findingsText = findingsText + '\n'
   return findingsText

def computeImpressions(request):
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   # 1) create list of dictionaries
   tempList = []
   for index in range(0, len(noduleList)):
      tempList.append({'index':index, 'recScore':int(noduleList[index]['recScore']), 'maxSize':maxSize(noduleList[index])})
   # 2) sort list
   intermediateList = sorted(tempList, key=itemgetter('maxSize'), reverse=True)
   newList = sorted(intermediateList, key=itemgetter('recScore'), reverse=True)
   # 2) print first Nodule impression
   findingsText = ""
   if int(newList[0]['recScore'])<3:
      findingsText += 'No concerning thyroid nodule\n'
   for ind in range(0, len(newList)):
      if int(newList[ind]['recScore'])>=3:
         findingsText += impressionForSingleNodule(noduleList[int(newList[ind]['index'])])
   findingsText += '\nTessler et al. ACR Thyroid Imaging, Reporting and DataSystem (TIRADS): White Paper of the ACR TI-RADS Committee. J Am Coll Radiol. 2017 May; 14(5): 587-595.'
   # per request of Dr. Fetzer print disclaimer if biopsy is needed
   if int(newList[0]['recScore'])>8:
      findingsText += '\n\nNote: Nodules in patients with significant comorbidities or limited life expectancy may not be clinically relevant and may not require biopsy.\n'
   return findingsText

'''
   mostConcernNod = noduleList[newList[0]['index']]
   secConcernNod = noduleList[newList[1]['index']]
   thirdConcernNod = noduleList[newList[2]['index']]
   findingsText = ''
   if int(mostConcernNod['recScore'])<3:
      findingsText += 'No concerning thyroid nodule'
   elif int(secConcernNod['recScore'])<3:
      findingsText += impressionForSingleNodule(mostConcernNod)
   elif int(thirdConcernNod['recScore'])<3:
      findingsText += impressionsForTwoNodules(mostConcernNod, secConcernNod)
   else:
      findingsText += 'Multiple nodules. Highest scoring is Nodule '
      findingsText += str(newList[0]['index']+1)
      findingsText += ': '
      findingsText += impressionForSingleNodule(mostConcernNod)
      findingsText += 'See report narrative for recommendation of other nodules.'
   findingsText += '\n\nTessler et al. ACR Thyroid Imaging, Reporting and DataSystem (TIRADS): White Paper of the ACR TI-RADS Committee. J Am Coll Radiol. 2017 May; 14(5): 587-595.'
   return findingsText
'''

def impressionForSingleNodule(tempNodule):
   findingsText = ''
   maxSizeInt = maxSize(tempNodule)
   findingsText += 'A ' + str(maxSizeInt) + ' mm '
   if tempNodule['location1'] == 'isthmus':
      findingsText = findingsText + tempNodule['location1'] + ' nodule. '
   else:
      findingsText = findingsText + tempNodule['location1'] + ' lobe nodule. '
   findingsText += trStatementFor(tempNodule)
   findingsText += recommendationStatementFor(tempNodule)
   findingsText += '\n'
   return findingsText

def impressionsForTwoNodules(noduleOne, noduleTwo):
   findingsText = impressionForSingleNodule(noduleOne)
   # print second nodule impression
   findingsText += 'A ' + str(maxSize(noduleTwo)) + ' mm '
   if noduleTwo['location1'] == 'isthmus':
      findingsText = findingsText + noduleTwo['location1'] + ' nodule. '
   else:
      findingsText = findingsText + noduleTwo['location1'] + ' lobe nodule. '
   findingsText += trStatementFor(noduleTwo)
   # figure out the impression for the second nodule
   if (int(noduleOne['recScore'])>5 and int(noduleOne['recScore'])<9 and int(noduleTwo['recScore'])>5 and int(noduleTwo['recScore'])<9):
      findingsText = findingsText + 'Follow up at above intervals.'
   else:
      findingsText = findingsText + recommendationStatementFor(noduleTwo)
      findingsText = findingsText + '\n'
   return findingsText

def maxSize(tempNodule):
   return max(int(tempNodule['sizeX']),int(tempNodule['sizeY']),int(tempNodule['sizeZ']))

def trStatementFor(tempNodule):
   # recScore - made up score that helps with prioritizing impressions
   # 1:TR1, 2:TR2, 3:TR3, 4:TR4, 5:TR5, 6:TR3F, 7:TR4F, 8:TR5F, 9:TR3B, 10:TR4B, 11:TR5B
   tiradsScore = {'1': 'TR1. ',            #TR1
         '2': 'TR2. ',             #TR2
         '3': 'TR3. ',                             #TR3
         '4': 'TR4. ',                             #TR4
         '5': 'TR5. ',                             #TR5
         '6': 'TR3. ',          #TR3F
         '7': 'TR4. ',      #TR4F
         '8': 'TR5. ',          #TR5F
         '9': 'TR3. ',          		   #TR3B- Removed 'mildly suspicious' due to request from Dr. Fetzer
         '10': 'TR4. ',     #TR4B
         '11': 'TR5. ',         #TR5B
         }
   return tiradsScore[tempNodule['recScore']]

def recommendationStatementFor(tempNodule):
   rec = {'1': 'No further follow up is needed.',                       #TR1
         '2': 'No further follow up is needed.',                        #TR2
         '3': 'No further follow up is needed.',                        #TR3
         '4': 'No further follow up is needed due to its small size.',  #TR4
         '5': 'No further follow up is needed due to its small size.',  #TR5
         '6': 'Follow up in 1, 3, and 5 years is recommended.',         #TR3F
         '7': 'Follow up in 1, 2, 3, and 5 years is recommended.',      #TR4F
         '8': 'Follow up yearly for 5 years is recommended.',           #TR5F
         '9': 'FNA biopsy is recommended.',                             #TR3B
         '10': 'FNA biopsy is recommended.',                            #TR4B
         '11': 'FNA biopsy is recommended.',                            #TR5B
         }
   return rec[tempNodule['recScore']]

'''
def computeImpressions(request):
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   findingsText = ''
   for index in range(0,len(noduleList)):
      if noduleList[index]['recScore'] != '0':
         findingsText = findingsText + 'Nodule ' + str(index+1) +': '
         findingsText = findingsText + computeImpressionForNodule(noduleList[index])
         findingsText = findingsText + '\n'
   return findingsText'''

def processInputs(request):
   noduleList = request.session['noduleList']
   nodHasBeenClicked = request.session['noduleHasBeenClicked']
   nodIndex = request.session['nodIndex']
   if 'location1' in request.POST:
      noduleList[nodIndex]['location1'] = request.POST['location1']
   if 'location2' in request.POST:
      noduleList[nodIndex]['location2'] = request.POST['location2']
   if 'location3' in request.POST:
      noduleList[nodIndex]['location3'] = request.POST['location3']
   if 'location4' in request.POST:
      noduleList[nodIndex]['location4'] = request.POST['location4']

   if request.POST['size1'] == '':
      noduleList[nodIndex]['sizeX'] = '0'
   else:
      noduleList[nodIndex]['sizeX'] = request.POST['size1']

   if request.POST['size2'] == '':
      noduleList[nodIndex]['sizeY'] = '0'
   else:
      noduleList[nodIndex]['sizeY'] = request.POST['size2']

   if request.POST['size3'] == '':
      noduleList[nodIndex]['sizeZ'] = '0'
   else:
      noduleList[nodIndex]['sizeZ'] = request.POST['size3']

   if 'composition' in request.POST:
      noduleList[nodIndex]['composition'] = request.POST['composition']
   if 'echogenicity' in request.POST:
      noduleList[nodIndex]['echogenicity'] = request.POST['echogenicity']
   if 'shape' in request.POST:
      noduleList[nodIndex]['shape'] = request.POST['shape']
   if 'margin' in request.POST:
      noduleList[nodIndex]['margin'] = request.POST['margin']

   noduleList[nodIndex]['noFoci'] = 'noFoci' in request.POST
   noduleList[nodIndex]['cometTail'] = 'cometTail' in request.POST
   noduleList[nodIndex]['macroCalcification'] = 'macroCalcification' in request.POST
   noduleList[nodIndex]['rimCalcification'] = 'rimCalcification' in request.POST
   noduleList[nodIndex]['punctateCalcification'] = 'punctateCalcification' in request.POST
   return
