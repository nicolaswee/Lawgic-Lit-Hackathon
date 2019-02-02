import requests
import urllib2
import xmltodict, json
import json

API_KEY = 'API KEY HERE'
URL = 'SEARCH URL HERE'
HEADERS = {'Content-Type': ' application/x-www-form-urlencoded', 'cache-control':'no-cache', 'x-api-key':API_KEY}

LIMIT = 3

L2CAT = ['r1c1']
L3CAT = ['r1c1sc17','r1c1sc2', 'r1c1sc118', 'r1c1sc11', 'r1c1sc7', 'r1c1sc10', 'r1c1sc5', 'r1c1sc6', '#r1c1', 'r1c1sc119', 'r1c1sc13', 'r1c1sc1', 'r1c1sc8', 'r1c1sc16', 'r1c1sc15', 'r1c1sc4', 'r1c1sc14', 'r1c1sc12', 'r1c1sc3', 'r1c1sc9']

L3COURT = ['Youth Court', 'Small Claims Tribunal', 'Small Claims Tribunal', 'Singapore International Commercial Court', 'Privy Council', 'Military Court of Appeal', 'Magistrates Court', 'Juvenile Court', 'Judgments', 'High Court (Registrar)', 'High Court (Family)', 'High Court', 'Federal Court', 'Family Court', 'District Court (Family)', 'District Court', 'Court of Three Judges', 'Court of Appeal (SICC)', 'Court of Appeal', 'Constitutional Tribunal']


def getInfo(name):
    data = {}
    data['name'] = name
    
    #data['l3cat'] = {}
    L3count = 0
    
    for l3 in L3CAT:
        DATA = 'apikey=' + API_KEY + '&cats=r1&l2cats=r1c1&l3cats=' + l3 + '&searchTerm=' + name +'&page=1&maxperpage=' + str(LIMIT) + '&orderBy=date-des&surroundingWords=1000'

        l3 = l3.replace('#','')
        # get requests 
        req = urllib2.Request(URL, DATA, HEADERS)
        content = urllib2.urlopen(req).read()
        dictionary = xmltodict.parse(content)
        #print json.dumps(dictionary)
        
        data[l3] = {}
        data[l3]['cat'] = l3
        
        data[l3]['courtname'] = ''.join(L3COURT[L3count])
        L3count = L3count + 1
        try:
            # load data
            total = dictionary['searchResponse']['searchStatistic']['total']
            data[l3]['totalAppearances'] = str(total)
                    
            resultList = dictionary['searchResponse']['searchResults']['resultList']['result']
        
            if len(resultList) == 3 or len(resultList) == 2:
                count = 1
                data[l3]['result'] = {}
                for result in resultList:
                    rname = 'result' + str(count)
                    
                    data[l3]['result'][rname] = {}
                    
                    date = result['documentTooltipHolder']['date']
                    data[l3]['result'][rname]['date'] = str(date)
                    
                    documentID = result['documentId']
                    data[l3]['result'][rname]['documentId'] = str(documentID)
                    
                    data[l3]['result'][rname]['caseno'] = str(result['documentTooltipHolder']['caseno'])
                    
                    data[l3]['document'] = {}
                    data[l3]['document']['title'] = str(result['document']['Title'])
                    data[l3]['document']['citation'] = str(result['document']['Citation'])
                    
                    count = count + 1
                    
            else:
                data[l3]['result'] = {}
                data[l3]['result']['result1'] = {}
                data[l3]['result']['result1']['date'] = str(resultList['documentTooltipHolder']['date'])
                data[l3]['result']['result1']['documentId'] = str(resultList['documentId'])
                data[l3]['result'][rname]['caseno'] = str(resultList['documentTooltipHolder']['caseno'])
                data[l3]['document'] = {}
                data[l3]['document']['title'] = str(resultList['document']['Title'])
                data[l3]['document']['citation'] = str(resultList['document']['Citation'])
        except Exception as e:
            #print str(e)
            data[l3]['result'] = {}
        
    
    jdata = json.dumps(data)
    return json.loads(jdata)
    
def getCatchword(name):
    data = {}
    data['name'] = name
    pagination = []
    
    for l3 in L3CAT:
        DATA = 'apikey=' + API_KEY + '&cats=r1&l2cats=r1c1&l3cats=' + l3 + '&searchTerm=' + name +'&page=1&maxperpage=100&orderBy=date-des&surroundingWords=1000'
        
        l3 = l3.replace('#','')
        # get requests 
        req = urllib2.Request(URL, DATA, HEADERS)
        content = urllib2.urlopen(req).read()
        dictionary = xmltodict.parse(content)
        
        try:
            # load data
            total = str(dictionary['searchResponse']['searchStatistic']['total'])
            pagination.append(total)
            
        except Exception as e:
            print str(e)
            
    c = 0
    print pagination
    
    for l3 in L3CAT:
        if int(pagination[c]) == 0:
            c = c + 1
            continue
        else:
            DATA = 'apikey=' + API_KEY + '&cats=r1&l2cats=r1c1&l3cats=' + l3 + '&searchTerm=' + name +'&page=1&maxperpage=' + pagination[c] + '&orderBy=date-des&surroundingWords=1000'
            
            l3 = l3.replace('#','')
            # get requests 
            req = urllib2.Request(URL, DATA, HEADERS)
            content = urllib2.urlopen(req).read()
            dictionary = xmltodict.parse(content)
            
            #print json.dumps(dictionary)
            data[l3] = {}
            data[l3]['cat'] = l3
            data[l3]['name'] = ''.join(L3COURT[c])
            total = dictionary['searchResponse']['searchStatistic']['total']
            data[l3]['totalAppearances'] = str(total)
            
            try:
                # load data
                resultList = dictionary['searchResponse']['searchResults']['resultList']['result']
                if int(pagination[c]) >= 2:
                    for result in resultList:
                        clist = []
                        catchword = str(result['documentTooltipHolder']['catchword'])
                        if catchword == 'No catchword':
                            continue
                        else: 
                            clist = catchword.split(',')
                            
                        for word in clist:
                            word = word.strip().lower()
                            if word in data[l3].keys():
                                data[l3][word] = data[l3][word] + 1
                            else:
                                data[l3][word] = 1
                        
                        #print str(data[l3][catchword]) + ' ' + str(catchword)
                        
                else:
                    catchword = resultList['documentTooltipHolder']['catchword']
                    clist = []
                    if catchword == 'No catchword':
                            continue
                    else: 
                        clist = catchword.split(',')
                        
                    for word in clist:
                        word = word.strip().lower()
                        if word in data[l3].keys():
                            data[l3][word] = data[l3][word] + 1
                        else:
                            data[l3][word] = 1
                    
            except Exception as e:
                print str(e)
        
        c = c + 1
        
    jdata = json.dumps(data)
    #print jdata
    return json.loads(jdata)
        
if __name__ == "__main__":
    getCatchword('subhas+anandan')
