## Introduction:
This is a program made with the idea of providing a "fast comparation of similar features between images in a given path".
This code uses concurrent.futures (multiprocesing) and OpenCV as it's main libraries.

## Instalation:
You only need:
* A python compiler 
* Have installed python-OpenCV library (check requirements.txt)

## Usage:
* The program is ready to run from the get go if you just *establish a path in the ConfigFile.ini*. Now you don't actually need to do this, *if you let path empty in the ConfigFile you can pass the path as the first argument when you call the program* (**python ./duplicate_images_opencv.py "path"**). Alternatively, if you don't define a path and neither give it to the program as an argument, it will run the program in the working directory of the session console you are using for calling the program.
* If you define the recursive option in the ConfigFile.ini as True, then it will look for images in the subdirectories of the provided path.
* **Similarity_ratio** option is an internal variable to work with the "distance between common features". The lower the value, the more similar the images will need to be for the program to recognize the similarities between them (setting it to low may cause that the program won't recognize an image that have been re-escalated too much). This variable can go from 0 to 1 been 0.6 an excellent value for it. \[*Fallback=0.6*]
* **Minimum_similarity** option is a floor to decide which pairs of images should be taken into account when writing them into the Similarities.txt. This value can go from 0 to 100, and in my tests between 30~50 was a good range for this variable. \[*Fallback=50*]
* **Processors** is a numerical variable that will tell the program how many processors would you like to assign to the program \[*Fallback=4*]

## Recomendations:
The processes of comparing images is quite taxing so I recommend:
    * Don't use all your processors unless you aren't going to use the computer while the code is running (you can decide the number of processors in the ConfigFile->processors variable)
    * Try to not use the recursive functionality, as it will reduce the performance quite significatly (Has to be checked again)

## Notes:
* The program only looks for .jpg and .png formats. If you want another format to be taken into account look for the comment: '#Generate lists containing cv2.imread() and titles.' and add another loop with the same format as the two presents but with the format that you want to be included.
* #!I'm trying to get a formula for a "spected required time" in base of the number of files and the size of the folder, but this is actually a really brute aproach with only two of the main variables of the problem, as the processor, hard drivde/ssd, number of available processors for the code to run in, and if you are using or not your computer, all of them have high impact on the result. But if we establish a base processor of 3.4Ghz and a simple SSD for testing, a constant number of avaliable processors for the program, and a computer who is only used for the program while this one is running we can have a really good representation of the problem and get a good estimate of the required time.