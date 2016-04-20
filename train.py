import os
from sklearn.linear_model import LogisticRegression
import numpy

def processFile(dir,processFunction):
    directory = os.path.join(dir)
    fileMap = {}
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith('.txt') or file.endswith('.txt'):
                f=open(dir+'/'+file,'r')
                result = processFunction(f)
                fileMap[file.replace(dir,'').replace('.txt','')] = result
    return fileMap

def processInput(f):
    pixels = []
    threshold = 100
    for line in f:
        row = line.split(' ')
        if(len(row) == 2):
            pass
        else:
            pixel = [ sum(map(int,i.split(',')))/3  for i in row]
            pixels.append(pixel)

    pixels = [[(255 if j > threshold else 0) for j in i]for i in pixels]
    return pixels

def processOutput(f):
    result = ''
    for line in f:
        result = line.replace('\n','')
    return result

def prepareTrainingData(input,output):
    train_x = []
    train_y = []
    #set a threshold for value to remove the background
    for d in input.keys():
        img = numpy.array(input[d],numpy.uint8)
        out = list(output[d])
        i=0
        #cut the image into 5 pices !
        startLocX = 7
        endLocX = 21
        startLocY = 6
        increment = 8
        for i in range(5):
            char = img[startLocX:endLocX,startLocY:startLocY+increment]
            startLocY = startLocY + increment + 1

            train_x.append(char.ravel())
            train_y.append(out[i])
    return (train_x,train_y)

input = processFile('input',processInput)
output = processFile('output',processOutput)
data = prepareTrainingData(input,output)
clf = LogisticRegression()
clf.fit(data[0], data[1])

f = open('input/input01.txt','r')
inp = processInput(f)
img = numpy.array(inp,numpy.uint8)
startLocX = 7
endLocX = 21
startLocY = 6
increment = 8
predict_x = []
for i in range(5):
    char = img[startLocX:endLocX,startLocY:startLocY+increment]
    startLocY = startLocY + increment + 1
    predict_x.append(char.ravel())
print clf.predict(predict_x)
