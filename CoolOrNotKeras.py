'''
Created on Nov 6, 2017

Run model on new images to predict classification

@author: mat
'''
import cv2
import time
import numpy as np
import argparse
import shutil
import os
from keras.models import load_model

ImageColors = 3
ImageWidth = 200
ImageHeight = 112

def getImageFileList(path):
    #TODO: probably an os function that returns full path+filename
    fullPathList = []
    filelist = os.listdir(path)
    for f in filelist:
        if(f.upper()).endswith('JPG'):
#             f = path + "\\" + f
            fullPathList.append(f)
    return fullPathList

def getNextBatchImages(fileList, startPos, endPos): 
    return getImages(fileList[startPos:endPos])
    
def getImages(imageFiles):
    imgList = []
    for i in imageFiles:
#         print(args.image + "\\" + i)
        img = cv2.imread(args.image + "\\" + i)#, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (ImageWidth, ImageHeight))
        img = np.float32(img)
        imgList.append(img)
    return np.asarray(imgList)

startTime = time.time()
# import win32api,win32process,win32con
# pid = win32api.GetCurrentProcessId()
# handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
# win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)

parser = argparse.ArgumentParser(description='Decide if an image is cool or not')
parser.add_argument('model', type=str, help='The path for mode file')
parser.add_argument('image', type=str, help='The path for image files')
parser.add_argument('move', type=str, help='move the cool images to cool folder')
args = parser.parse_args()
print('model file: ' + args.model)
model = load_model(args.model)
model.summary()

# Load the image file
# img = scipy.ndimage.imread(args.image, mode="RGB")
# img = cv2.imread(args.image)
# Scale it to 32x32
# img = scipy.misc.imresize(img, (32, 32), interp="bicubic").astype(np.float32, casting='unsafe')
# img = cv2.resize(img, (ImageWidth, ImageHeight))
# img = np.float32(img)
# Predict
imgFileList = getImageFileList(args.image)
imgBatchSize = 20
ctr=0
coolCtr=0
notCoolCtr=0

movePath = os.path.join(args.image, 'cool')
if(args.move.upper()=="MOVE"):
    if not os.path.isdir(movePath):
        os.makedirs(movePath)
# fileList=[]
print("processing in " + args.image)
while(ctr < len(imgFileList)):
#     f = args.image + "\\" + imgList[ctr]
    endPos = min((ctr+imgBatchSize),len(imgFileList))
    batchlist = imgFileList [ctr: endPos]
    imgLst = getImages(batchlist)
    prediction = model.predict(imgLst)
#     print(batchlist)
    for i in range(0, len(prediction)):
#         print (prediction[i][0])
        is_cool = prediction[i][0] == 1
        if is_cool:
            coolCtr=coolCtr+1
            print(batchlist[i] + " is cool! : ",prediction[i])
            if(args.move.upper()=="MOVE"):
                shutil.move(args.image + "\\" + batchlist[i], movePath + '\\' + batchlist[i])
        else:
            print(batchlist[i] + " is not cool: ", prediction[i])
            notCoolCtr=notCoolCtr+1
        print('-------------')

    ctr=ctr+imgBatchSize

    # Check the result.
#     print(prediction[0][0])
#     print(prediction[0][1])
print ('total  time in mins: ' + str((time.time() - startTime)/60.))
print ('total cool: ', coolCtr)
print ('total not cool: ', notCoolCtr)
coolPct =  coolCtr/(coolCtr+notCoolCtr)
print('coolPct: ', coolPct)
