import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

def crop(img,xyxy):
    x1, y1 ,x2, y2 = map(int,xyxy)
    return img[y1:y2 ,x1:x2, :]

def main(img_path, label_path):
    global count
    img = cv2.imread(img_path)
    h, w, _ = img.shape 
    with open(label_path) as file:
        content=file.readlines()
    for i in range(len(content)):
        c = content[i].split(' ')[0]
        xywh = content[i].split(' ')[1:]
        xywh = [xywh[0], xywh[1], xywh[2], xywh[3][:-2]]
        xywh = [float(j) for j in xywh]
        xywh = [xywh[0]*w, xywh[1]*h, xywh[2]*w, xywh[3]*h]
        xyxy = [xywh[0]-xywh[2]/2, xywh[1]-xywh[3]/2, xywh[0]+xywh[2]/2, xywh[1]+xywh[3]/2]
        crop_img = crop(img, xyxy)
        count += 1
        if not os.path.isdir(f'../dataset/{c}/'):
            os.mkdir(f'../dataset/{c}/')
        cv2.imwrite(f'../dataset/{c}/{count}.jpg',crop_img)

count = 0
img_path = '/home3/HWGroup/liujy/agent_4mission_detection/resnet18/graph/images/6eaf7db3e02fee0933668638120e8b8_jpg.rf.5d48192022d32f4ad01d21b5b4a8c11f.jpg'
label_path = '/home3/HWGroup/liujy/agent_4mission_detection/resnet18/graph/labels/6eaf7db3e02fee0933668638120e8b8_jpg.rf.5d48192022d32f4ad01d21b5b4a8c11f.txt'
root = '/home3/HWGroup/liujy/agent_4mission_detection/resnet18/graph'
img_paths = sorted(os.listdir(os.path.join(root,'images')))
label_paths = sorted(os.listdir(os.path.join(root,'labels')))
for i in range(len(img_paths)):
    main(os.path.join(root,'images', img_paths[i]), os.path.join(root,'labels', label_paths[i]))