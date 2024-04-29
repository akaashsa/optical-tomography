# optical-tomography
Based on the DIY Kitchen based Optical Tomography experiment by Emanuel Larson. This project contains the code for converting your sequential image files to a grey scale, normalized and stacked .tiff format

Principal of Optical Tomography :

Unlike Computerized Tomography, Optical Tomography uses visible light, where the light from an LED source or a torch is passed through an object and it is received on a screen. The projection on the screen is then captured by a camera. The object is rotated with the help of servo motors. The servo motors and camera, in turn are synchronized by a Raspberry Pi.

This code will help you convert all the images into a .tiff file and also visualize a 3D image using Mayavi package in Python. 

The projections.tiff file can be used to process image through a software like Fuji. Fuji will allow you to perform FFT analysis, applying filters and stuff.

Hope you like it! Do leave your feedback!

Note: I ran this project on VSCode, and used a Conda virtual environment. Make sure there are no conflicts between packages installed via pip or Conda
