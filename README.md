# python-fun
Experimenting with python and image classification 

This is a work in progress to get a feeling machine learning.  I'm using the keras library to read in a set of images and classify them as interesting or not.  Why?  I have a "game camera" set up to watch an alleyway behind my backyard.  I usually take out the SD card once a week to look over the images.  There are a lot of "false positives" that I have to skip through since the camera is motion triggered and the trees usually create lot of "junk" images.  So, the whole idea with this ML model is to tell me if an image is "cool" (usually because it has a person or car in it) vs "notcool".  

The code has some hardcoded paths (sorry) and assumes you have both a test and training directory.  Under test and training, it assumes you have 2 more paths under each called "cool" and "notcool".  
