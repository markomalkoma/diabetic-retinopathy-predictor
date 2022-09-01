import cv2
import os
import numpy as np

def load(path):
    return cv2.imread(path)

def resize (image,ratio=0.3):
    return cv2.resize(image,(0,0),fx=ratio,fy=ratio)

def model_resize(image):
    return cv2.resize(image,(256,256))    

def show(file,name):
    cv2.imshow(name,file)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def grey(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def masking(image,margin=10):
    rows,cols,_=image.shape
    cells=rows*cols
    pixels = np.reshape(image,(cells,3))
    #print(pixels)
    #print(pixels.shape)
    colors,index,count=np.unique(pixels,axis=0,return_index=True,return_counts=True)
    c=[]
    for i in range (len(colors)):
        condition_1=colors[i][2]>60
        condition_2=colors[i][1]<200
        condition_3=colors[i][0]<200
        if condition_1 and condition_2 and condition_3:
            c.append((count[i],colors[i]))

    sorted_colors = sorted(c,key= lambda x : x[0], reverse=True)
    #print(sorted_colors[0:20])
    main_color=sorted_colors[0][1]
    main_color_low=main_color-margin
    main_color_max=main_color+margin
    mask=cv2.inRange(image,main_color_low,main_color_max)
    result=cv2.bitwise_and(image,image,mask=mask)
    return result

def selector(files,outputs):
    image_names=[]
    for img in files:
        image_names.append(img.split(".")[0])
    test_values=outputs[outputs.image.isin(image_names)]
    return test_values

def files_loader(path):
    files = os.listdir(path)
    return files

def draw_circle(path):
    img = cv2.imread(path)
    img = resize(img, ratio = 0.2)
    img_grey = grey(img)
    rows, cols = img_grey.shape
    
    y_values=[]
    for row in range(int(0.4*rows), int(0.6*rows)):
        distance = 0
        for col in range(cols):
            distance+=1
            if img_grey[row, col] > 30:
                y_values.append((distance,row,col))
                break
    x_values=[]
    for col in range(int(0.4*cols), int(0.6*cols)):
        distance = 0
        for row in range(rows):
            distance+=1
            if img_grey[row, col] > 30:
                x_values.append((distance,row,col))
                break

    center = (min(x_values)[2], min(y_values)[1])
    radius = int(min(x_values)[2] - min(y_values)[2])

    print(center, radius)

    img = cv2.circle(img, center, radius, (250,250,250), 5)

    return show(img, path)

def notch_selector(path):
    img = cv2.imread(path)
    #print(img.shape)
    img_grey = grey(img)
    _, cols = img_grey.shape
    #print(img_grey.shape)
    for row in range(10):
        for col in range(cols):
            if img_grey[row, col] > 30:
                return False
    return True

def filename_sorter(path, phrase):
    if phrase in path:
        return True
    return False

    


