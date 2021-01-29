#!/usr/bin/env python

# avatars
# Ver1.0
# Created by MildMastermind
#
# This script is intended to create every possible iteration of an avatar where each component of the image (eyes, nose, mouth, hair, etc)
# is contained within a layer group. Any layer named "Background" will be made transparent. An example file would look like:
# >hair
# >Eyes(group)
#  >>eyes1
#  >>eyes2
# >Mouths(group)
#  >>mouth1
#  >>mouth2
# >nose
# >face
# >Background
#
# Such that in the above example the following files would be created (output file names use the layer names):
# eyes1mouth1.png
# eyes1mouth2.png
# eyes2mouth1.png
# eyes2mouth2.png
# 
# Credit to the tutorial https://jacksonbates.wordpress.com/2015/09/14/python-fu-5-automating-workflows-coding-a-complete-plug-in/
# for helping me figure out how the hell to get this working as a plugin
#
# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
#
# ------------
#| Change Log |
# ------------
# V1.0: Initial release.

import string
import traceback
from gimpfu import *
from array import array

groupList = []

def python_avatar(image, activelayer, savePath):

    pdb.gimp_image_undo_group_start(image)
    
    try:
        for pos,layerOrGroup in enumerate(image.layers): #Start by setting all layers within groups to hidden
           if layerOrGroup.name == "Background":
               pdb.gimp_layer_set_opacity(layerOrGroup, 0) #make sure the background Layer is transparent
           if isinstance(layerOrGroup,gimp.GroupLayer):
               groupList.append(layerOrGroup) #get a global list of all layer groups
               for p,layer in enumerate(layerOrGroup.layers):
                   pdb.gimp_item_set_visible(layer, FALSE) #set all layers within groups to hidden
        doLayers(image,"",0,savePath)
    except Exception as e:
        #trace(e.args[0]) #caused issues
        gimp.message(e.args[0])#+':'+traceback.format_exc())	

    gimp.message("Complete")

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()

def doLayers(image,name,num,savePath):
    for pos,layer in enumerate(groupList[num].layers):
        pdb.gimp_item_set_visible(layer, TRUE)
        if num == len(groupList)-1:
            #save
            new_image = pdb.gimp_image_duplicate(image)
            new_layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
            pdb.file_png_save_defaults(image, new_layer, savePath+name+layer.name+".png", savePath+name+layer.name+"_raw.png")
            pdb.gimp_image_delete(new_image)
        else:
            doLayers(image,name+layer.name,num+1,savePath)
        pdb.gimp_item_set_visible(layer, FALSE)


register(
    "python-fu-avatar",
    "Iterates through each grouped layer and generates a png of every combination", #tooltip on dropdown
    "Make Avatars...",
    "MildMastermind",
    "MildMastermind",
    "2021",
    "Make Avatars...", #Dropdown menu text
    "*", 
    [
    (PF_IMAGE,"image", "Image:", None),
    (PF_DRAWABLE, "drawable", "Drawable:", None),
    (PF_STRING, "savePath", "Folder to Save to:", "C:\\Temp\\")
    ],
    [],
    python_avatar,
    menu="<Image>/Avatars"
)

main()