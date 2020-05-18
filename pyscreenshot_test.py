import pyscreenshot as ImageGrab
import numpy as np
import os
import time
import PIL


def screengrab():
    boxt = (209, 600, 280, 638)  # Chiffre centaines
    box3 = (209, 600, 234, 638)  # Chiffre centaines
    box2 = (232, 600, 257, 638)  # Chiffre dizaines
    box1=  (255, 600, 280, 638)  # Chiffre

    imt=  ImageGrab.grab(boxt)
    im1 = ImageGrab.grab(box1)
    im2 = ImageGrab.grab(box2)
    im3 = ImageGrab.grab(box3)

    im1.save('/home/jphe/PycharmProjects/Captures/unites'+str(int(time.time()))+'.png','PNG')
    im2.save('/home/jphe/PycharmProjects/Captures/dizaines' + str(int(time.time())) + '.png', 'PNG')
    im3.save('/home/jphe/PycharmProjects/Captures/centaines' + str(int(time.time())) + '.png', 'PNG')
    imt.save('/home/jphe/PycharmProjects/Captures/total'+str(int(time.time()))+'.png','PNG')
    return im1,im2,im3

def screengrab2():
     boxt = (209, 600, 280, 638)
     imt=  ImageGrab.grab(boxt)
     file_adress='/home/jphe/PycharmProjects/Captures/total'+str(int(time.time()))+'.png'
     imt.save(file_adress,'PNG')
     return file_adress


if __name__ == '__main__':

    
    im1,im2,im3=screengrab()
    im = PIL.Image.open('../Captures/3.png')	# Ouverture
    T = np.array(im)
    print(T)
    T1= np.array(im1)
    T2= np.array(im2)
    T3= np.array(im3) 
    print('t1.shape',T1.shape)
    st1=np.sum(T1)
    print ('sum1',st1)

    st2=np.sum(T2)
    print ('sum2',st2)

    st3=np.sum(T3)
    print ('sum3',st3)

    st4=np.sum(T3+T1)

    print ('sum4',st4)
    
    #print(T2-T3)

    
    # print (T1-T2)


#        from PIL import Image
from PIL import ImageChops

# image_one = Image.open(path_one)
# image_two = Image.open(path_two)

diff = ImageChops.difference(im1, im1)

if diff.getbbox():
    print("images are different")
else:
    print("images are the same")