from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils import simplejson 

from random import randrange
from Face import Face
import math
import cStringIO
import urllib, urllib2
import Image as PilImage 
from social_auth.models import UserSocialAuth
from facegraph import Graph


def myphotos(request):
    
    photo_list = []
    if request.user.is_authenticated():
        userInstance = UserSocialAuth.objects.filter(user=request.user).get()
        photo_list = getFacebookPhotos(userInstance)
        username = request.user.get_full_name()
    else:
        return HttpResponseRedirect('/login/?next=%s' % request.path)
        
    photo = photo_list[0]
    my_data_dictionary = {'photo_list':photo_list,'photo':photo,'username':username}
    return render_to_response('myphotos.html',
                          my_data_dictionary,
                          context_instance=RequestContext(request))

def base(request):
    
    if  request.user.is_authenticated():
        username = request.user.get_full_name()
    else:
        username = None
        
    my_data_dictionary = {'username':username}
    return render_to_response('index.html',
                          my_data_dictionary,
                          context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')

#def logout_view(request):
#    logout(request)
#    return HttpResponseRedirect("/")
#def getPhotosJson(request):
#    photo_list = []
#    if not request.user.is_authenticated():
#        return HttpResponseRedirect('/login/?next=%s' % request.path)
#    else:
#        userInstance = UserSocialAuth.objects.filter(user=request.user).get()
#        photo_list = getFacebookPhotos(userInstance)
#        
#    return sendObjectAsJson(photo_list)
        
def getFacebookPhotos(userInstance):
    access_token = userInstance.tokens['access_token']
    graphObject = Graph(access_token)
    facebookPhotos = graphObject['me'].photos(limit=0)
    
    photoSources = []
    photoTitles = []
    
    for photo in facebookPhotos.data:
        
        if photo.has_key('name'):
            photoTitle = photo['name']
        else:
            photoTitle =  ''
        
        myPhoto = {'url' :photo['source'], 'title': photoTitle}
        photoSources.append(myPhoto)
#        photoTitles.append(photo['name'])
#        photoSources.append(photo['source'])
    return photoSources
    
def somePrivateMethod(request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        userInstance = UserSocialAuth.objects.filter(user=request.user).get()
        access_token = userInstance.tokens['access_token']
        
        graphObject = Graph(access_token)
        facebookPhotos = graphObject['me'].photos(limit=20)
        
        returnObject = {'first_name':request.user.first_name,'last_name': request.user.last_name ,'access_token': access_token, 'status':'success','photos': facebookPhotos}
        response = sendObjectAsJson(returnObject)
    return response

def sendObjectAsJson(myObjectDict):
    data = simplejson.dumps(myObjectDict, indent=4) 
    print 'returning: %s' % data
    resp = HttpResponse(data, mimetype='application/json')
    resp['Access-Control-Allow-Headers'] = '*'
    return resp

def getFacegetImage(request):
    response = {};
    if (request.GET.has_key('urls')):
        imageUrl = request.GET.get('urls')
        response = getFace(imageUrl)
    
    return sendObjectAsJson(response)
    
def getFace(imageUrl):
    webAdress = 'http://open.liorkirsch.webfactional.com/o/detectObjects?urls=%s' % imageUrl
    req = urllib2.Request(webAdress)
    opener = urllib2.build_opener()
    f = opener.open(req)
    return simplejson.load(f)
        
def placeImageWithMashape(origPilImage,origImageUrl,imageHat, personIndex):
##################MASHAPE
    client = Face("1vgorh7zmjvdnjq2xjwqq6xnwm6xa4", "zhyjc7xytpu3rcwjy3akzzqiirb3ev")
    faceData = client.detect(images='http://www.taipeitimes.com/images/2012/11/08/thumbs/P03-121108-1.jpg')
    numberOfObjects = len(faceData.body['photos'][0]['tags'])
    if (personIndex is not None) and (0 <= personIndex < numberOfObjects):
        faceIndex = personIndex
    else:
        faceIndex = randrange(numberOfObjects)

    singleFaceData = faceData.body['photos'][0]['tags'][faceIndex]
    faceWidth = singleFaceData['width']
    faceHeight = singleFaceData['height']
    faceXcord = singleFaceData['center']['x'] 
    faceYcord = singleFaceData['center']['y']
    hatWidth = int(math.floor(faceWidth * 2))
    ratio = float(hatWidth) /float(imageHat.size[0])
    hatHeight = int(math.floor(imageHat.size[1] *ratio))  
    imageHatResized = imageHat.resize((hatWidth, hatHeight),PilImage.ANTIALIAS)
    faceX = int(math.floor(faceXcord - imageHatResized.size[0]/2.0))
    faceY = int(math.floor(faceYcord - imageHatResized.size[1]/2.0 - faceHeight/2.0*0.3 ))
    faceY = faceY - faceHeight/2 
    origPilImage.paste(imageHatResized, (faceX, faceY), imageHatResized)
    return (origPilImage , faceIndex)

def placeImageWithOpenCv(origPilImage,origImageUrl,imageHat, personIndex):
################## OPENCV
    faceData = getFace(origImageUrl)
    numberOfObjects = len(faceData['images'][0]['versions'][0]['objects'])
    if (personIndex is not None) and (0 <= personIndex < numberOfObjects):
        faceIndex = personIndex
    else:
        faceIndex = randrange(numberOfObjects)

    singleFaceData = faceData['images'][0]['versions'][0]['objects'][faceIndex]
    faceWidth = int(math.floor(singleFaceData['width'] * origPilImage.size[0]))
    faceHeight = int(math.floor(singleFaceData['height'] * origPilImage.size[1]))
    faceXcord = int(math.floor(singleFaceData['center']['x'] * origPilImage.size[0]))
    faceYcord = int(math.floor(   singleFaceData['center']['y'] * origPilImage.size[1])) 
    hatWidth = int(math.floor(faceWidth * 2.4))
    ratio = float(hatWidth) /float(imageHat.size[0])  
    hatHeight = int(math.floor(imageHat.size[1] *ratio))
    imageHatResized = imageHat.resize((hatWidth, hatHeight),PilImage.ANTIALIAS)
    
    faceX = int(math.floor(faceXcord - imageHatResized.size[0]/2.0))
    faceY = int(math.floor(faceYcord - imageHatResized.size[1]/2.0 - faceHeight/2.0*0.3 ))
    faceY = faceY - faceHeight/2 
    origPilImage.paste(imageHatResized, (faceX, faceY), imageHatResized)
    
    return (origPilImage ,faceIndex)

def placeImage(origPilImage,origImageUrl,finalImageHeight, personIndex):
    #
    imageHat = PilImage.open('inception/viet_hat_stright.png')
    #imageHat = PilImage.open('inception/farmer.png')
    #imageHat = PilImage.open('inception/viet_hat.png')

    #(modifiedImage, faceIndex) = placeImageWithMashape(origPilImage,origImageUrl,imageHat, personIndex)
    (modifiedImage, faceIndex) = placeImageWithOpenCv(origPilImage,origImageUrl,imageHat, personIndex)
    
    if (finalImageHeight is not None):
        ratio = float(finalImageHeight) /float(modifiedImage.size[1])  
        finalImageWidth = int(math.floor(ratio * modifiedImage.size[0] ))
        finalImageResized = modifiedImage.resize((finalImageWidth, finalImageHeight),PilImage.ANTIALIAS)
    else:
        finalImageResized = modifiedImage
     
    return (finalImageResized, faceIndex) 

def changeImage(request):
    imageUrl = request.GET.get('url')
    if ('height' in request.GET):
        finalImageHeight = int(request.GET.get('height'))
    else:
        finalImageHeight = None
        
    if ('index' in request.GET):
        personIndex = int(request.GET.get('index'))
    else:
        personIndex = None

    fp = urllib.urlopen(imageUrl)
    imageFile = cStringIO.StringIO(fp.read()) # constructs a StringIO holding the image
    theImage = PilImage.open(imageFile)
    
    (theImage, faceIndex) = placeImage(theImage,imageUrl,finalImageHeight, personIndex)
    
    response = HttpResponse(mimetype="image/png")
    theImage.save(response, "PNG")
    
    return response
    
