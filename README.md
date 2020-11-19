# DentalImplants
Blender plugin for placing dental implants

## Installation
1. Download the Zip file of this code from this repository
![Download Code from Github](https://i.imgur.com/Vw9WkPF.png "Download Code")
2. Extract this file to a location
3. Open Blender Note: This has only been tested on Blender 2.90.1
4. Edit user Preferences
![Edit User Preferences in Blender](https://i.imgur.com/8i1gXpC.png "Edit User Preferences")
5. Navigate to Addons and click Install in the top right corner of the window
![Click Install under Addons Panel](https://i.imgur.com/itKn5UN.png "Click Install")
6. Navigate to the "ui_panel.py" file where you extracted the download
![Navigate to Python File](https://i.imgur.com/Knv6Mem.png "Navigate to python file")
7. Click the checkbox on the Addons window to enable the plugin
![Enable Addon](https://i.imgur.com/fpXJpig.png "Click the checkbox to enable")

## Usage
First Import your folder containing reconstruction data by clicking "Import Mandible" in the top left of the 3d viewer
![Click import Mandible](https://i.imgur.com/9NxjjO2.png "Click Import Mandible in the top left of the 3d viewer")
Click on the 3D Cursor Tool to select it and click anywhere on the mandible or maxilla to place the 3D cursor
![Click 3D Cursor](https://i.imgur.com/YNGspho.png "Click 3D Cursor")
Click Add Dental Implant to add a Dental Implant at the location of the 3D Cusor
![Click Add Dental Implant](https://i.imgur.com/Q2jVRyv.png "Click Add Dental Implant")
More implants can be placed by selecting the 3D cursor and clicking on another spot followed by clicking Add Dental Implant again

Implants can be moved and rotated by clicking the Move and Rotate tools located beneath the 3D Cursor tool in the top left corner of the 3D Viewer


Additional Actions and Data can be accessed via the Object Properties panel, the two important categories are "Dental Implant" and "Implant Orientations"
![Click 3D Cursor](https://i.imgur.com/jrh9BEW.png "Click 3D Cursor")

*Note: you may have to scroll down to see these categories, you can move them to the top by dragging up on the braille-like icon*
### Dental Implant
This provides additional commands such as changing the transparency, duplicating implants, saving implants, and importing teeth

Import Tooth will open a file browser, all teeth files are stored in the STLTeeth folder included with this addon.

### Implant Orientations
This provides a shortcut for viewing the orientation of all implants as well as viewing the difference between implants

## Acknowledgements
Original Tooth models from
[BlueSkyBio](https://en.blueskybioacademia.com/digitalfiles)

Blender 2.90.1 obtained from
[Blender Foundation](https://www.blender.org/)

Images hosted at [Imgur](https://imgur.com/)


