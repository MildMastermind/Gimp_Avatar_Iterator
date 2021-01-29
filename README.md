# Gimp_Avatar_Iterator
A python-fu script for The GIMP that iterates through every combination of individual layers stored within layer groups, and outputs a .png file for each combination.


This script is intended to create every possible iteration of an avatar (ala www.picrew.me) where each component of the image (eyes, nose, mouth, hair, etc) is contained within a layer group. Any layer named "Background" will be made transparent. An example file would look like:
- hair
- Eyes(group)
  - eyes1
  - eyes2
- Mouths(group)
  - mouth1
  - mouth2
- nose
- face
- Background

Such that in the above example the following files would be created (output file names use the layer names):
eyes1mouth1.png
eyes1mouth2.png
eyes2mouth1.png
eyes2mouth2.png

Earliest GIMP version tested is 2.10.10

Place the entire folder in C:\Users\<USERNAME>\AppData\Roaming\GIMP\2.10\plug-ins
If you only place the .py file there it won't be loaded by GIMP. Probably seems obvious to people who use this a lot, but I had a hell of a time finding that info initially
