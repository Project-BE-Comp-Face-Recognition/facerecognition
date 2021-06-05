import cv2
import dlib
import os
import sys
   
#cam = cv2.VideoCapture(1)
detector = dlib.get_frontal_face_detector()

def faceDetector(teacherId): 
    detector = dlib.get_frontal_face_detector()

    detectedFaces=0
    facenumber=0
    currentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    imageFolder = os.path.join(currentDir, "identify/")
    imageFolder = os.path.join(imageFolder,teacherId)
    print(imageFolder)
    for filename in os.listdir(imageFolder):
        print(imageFolder+  './'+filename)
        img=cv2.imread(imageFolder+'./'+filename)
        dets = detector(img, 1)
        print("detected = {}".format(len(dets)))
        
        if not os.path.exists(currentDir+'./croppedimages'):
            os.makedirs(currentDir+'./croppedimages')
        target=os.path.join(currentDir,'croppedimages')
        
        if not os.path.exists(target+"./"+teacherId):
            os.makedirs(target+"./"+teacherId)
        cropped=os.path.join(target,teacherId)
        
        
        for i, d in enumerate(dets):
            facenumber+=1
            cv2.imwrite(cropped+"/face" + str(facenumber) + 
            '.jpg', img[d.top():d.bottom(), d.left():d.right()])
        detectedFaces+=len(dets)

        print(cropped)
    return (cropped)


if __name__ == "__main__":
    abc=faceDetector(teacherId)