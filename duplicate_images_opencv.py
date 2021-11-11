#!Aclarar que solo toma formatos png y jpg, pero puede agregarse otros formatos manualmente en el codigo (quizas con el configure?)
"""
Program for a fast comparation of similar features between images in a given path. This code uses concurrent.futures (multiprocesing) and OpenCV as it's main libraries.
"""

# Useful reference links:
# https://pysource.com/2018/07/19/check-if-two-images-are-equal-with-opencv-and-python/ #Check equals imgs
# https://www.youtube.com/watch?v=9mQznoHk4mU #Check if two imgs are similar
# https://www.youtube.com/watch?v=ND5vGDNvN0s #How similar two imgs are
# https://www.youtube.com/watch?v=ADuHe4JNLXs #Porcentual similarity and Optimization

#More complete version than the PIL byte by byte comparation option. This one will recognize not only if two images are the same (this implicitly  means that they must have the same size), but if they are similar based on special algorithms of OpenCV library (filters, resizes and cuts should be recognized by the code!)

#TODO:
#!Autoremove is not implemented (but defined) because of all the problems that imply passing the path at every instance. Can do it easily if I pass another list with complete paths to ImageChecker, but I dont like that idea...

import os
import cv2
import glob
import configparser
import concurrent.futures
from sys import argv


class ImageChecker():
    #Needed variables in all instances
    #!SIMILARITY_RATIO=None #!Roto
    #!MINIMUM_SIMILARITY=None #!Roto
    SIFT = cv2.SIFT_create()
    INDEX_PARAMS = dict(algorithm=0, trees=5)
    SEARCH_PARAMS = dict()
    FLANN = cv2.FlannBasedMatcher(INDEX_PARAMS, SEARCH_PARAMS)#Flann is a faster method provided by cv2 than comparing each descriptor for both images

    def __init__(self, SR, MS, img1, title1):
        #Have to make these variables because class variables or global variables weren't working with multiprocesing
        self.SIMILARITY_RATIO = SR
        self.MINIMUM_SIMILARITY = MS
        #Instance of the main image and it's title (this image is the one that will be compared in series)
        self.img1 = img1
        self.title1 = title1
        self.not_equal = True


    def equalImgs(self,img2,title2) -> bool:
        """This method check if two images have the same size and channels, then substract their pixels and if the substraction is null they are completly equals"""
        if self.img1.shape == img2.shape:
            difference = cv2.subtract(self.img1, img2)
            b,g,r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                self.not_equal = False
                return f"{self.title1} | {title2} : {100}%\n"
            else:
                return None


    def comparationMatches(self,img2,title2):
        """This method uses the OpenCV features idea to check similarity between two images. The comparation is based in the flan algorithm from the same library"""
        kp_1, desc_1 = self.SIFT.detectAndCompute(self.img1, None)
        kp_2, desc_2 = self.SIFT.detectAndCompute(img2, None)
        
        matches = self.FLANN.knnMatch(desc_1, desc_2, k=2)
        good_points = []
        for m,n in matches:
            #!if m.distance < ImageChecker.SIMILARITY_RATIO * n.distance:
            if m.distance < self.SIMILARITY_RATIO * n.distance:
                good_points.append(m)

        if len(kp_1) < len(kp_2):
            similarity = int(len(good_points)/len(kp_1)*100)
        else:
            similarity = int(len(good_points)/len(kp_2)*100)

        #!if ImageChecker.MINIMUM_SIMILARITY <= similarity:
        if self.MINIMUM_SIMILARITY <= similarity:
            return f"{self.title1} | {title2} : {similarity}%\n"


    def main(self,img2title2:tuple): 
        #!
        print(f"Checking {self.title1} vs {img2title2[1]}")
        #!Call first function and make it equal to a bool
        result = self.equalImgs(img2title2[0], img2title2[1])
        #!If that bool is false go to the second function
        if self.not_equal:
            result = self.comparationMatches(img2title2[0], img2title2[1])
        
        return result


def settingConfiguration(config:configparser.ConfigParser):
    """Function in charge of setting the Optional configuration from the ConfigFile.ini"""
    if config['Options']['path']:
        path = config['Options']['path']
        if path[-1] != os.sep:
            path += os.sep
    elif len(argv) > 1:
        path = argv[1]
        if path[-1] != os.sep:
            path += os.sep
    else:
        path = f'.{os.sep}'
    
    try:
        autoremove = config['Options'].getboolean('autoremove')
    except ValueError:
        print(f"ValueError in ConfigParser -> autoremove is not a bool! (True or False)")
        print("The code will proceed with the default fallback value:")
        autoremove = False
    
    try:
        recursive = config['Options'].getboolean('recursive')
    except ValueError:
        print(f"ValueError in ConfigParser -> recursive is not a bool! (True or False)")
        print("The code will proceed with the default fallback value:")
        recursive = False
    
    try:
        #!ImageChecker.SIMILARITY_RATIO = config['Options'].getfloat('similarity_ratio')
        SIMILARITY_RATIO = config['Options'].getfloat('similarity_ratio')
    except ValueError:
        print(f"ValueError in ConfigParser -> SIMILARITY_RATIO is not a valid numerical value!")
        print("The code will proceed with the default fallback value:")
        #!ImageChecker.SIMILARITY_RATIO = 0.6
        SIMILARITY_RATIO = 0.6

    try:
        #!ImageChecker.MINIMUM_SIMILARITY = config['Options'].getint('minimum_similarity')
        MINIMUM_SIMILARITY = config['Options'].getint('minimum_similarity')
    except ValueError:
        print(f"ValueError in ConfigParser -> MINIMUM_SIMILARITY is not a valid numerical value!")
        print("The code will proceed with the default fallback value:")
        #!ImageChecker.MINIMUM_SIMILARITY = 50
        MINIMUM_SIMILARITY = 50
    
    return SIMILARITY_RATIO, MINIMUM_SIMILARITY, path, autoremove, recursive


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('ConfigFile.ini')
    try:
        SR, MS, path, autoremove, recursive = settingConfiguration(config)
    except KeyError:
        aux = argv[0].split(os.sep)
        aux.pop()
        aux = os.sep.join(aux)
        config.read(f'{aux}{os.sep}ConfigFile.ini')      
        SR, MS, path, autoremove, recursive = settingConfiguration(config)

    #Generate lists containing cv2.imread() and titles.
    all_images = []
    images_names = []
    if not recursive:
        for f in glob.iglob(f'{path}*.jpg'):
            image = cv2.imread(f)
            images_names.append(''.join(f.split(path)[1]))
            all_images.append(image)
        for f in glob.iglob(f'{path}*.png'):
            image = cv2.imread(f)
            images_names.append(''.join(f.split(path)[1]))
            all_images.append(image)
    else:
        for f in glob.iglob(f'{path}**{os.sep}*.jpg', recursive=True):
            image = cv2.imread(f)
            images_names.append(''.join(f.split(path)[1]))
            all_images.append(image)
        for f in glob.iglob(f'{path}**{os.sep}*.png', recursive=True):
            image = cv2.imread(f)
            images_names.append(''.join(f.split(path)[1]))
            all_images.append(image)

    #Opening writing file
    with open(f'{path}Similarities.txt','w', encoding='utf-8-sig') as file:
        #Main loop
        for i in range(len(all_images)):
            img1 = all_images[i]
            title1 = images_names[i]
            inst = ImageChecker(SR, MS, img1, title1)
            with concurrent.futures.ProcessPoolExecutor() as executor:
                processes = executor.map(inst.main,((img2,title2) for img2,title2 in zip(all_images[i+1:],images_names[i+1:])))
                for result in processes:
                    try:
                        file.write(result)
                    except TypeError:
                        pass

