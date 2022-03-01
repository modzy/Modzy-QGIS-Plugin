To see more documentation, please [view this page on Modzy's official documentation site](https://docs.modzy.com/docs/qgis).

# Overview

[Quantum GIS (QGIS)](https://qgis.org)is an open-source [Geographic Information System](https://en.wikipedia.org/wiki/Geographic_information_system) for viewing, editing, and analyzing geospatial data. This plugin allows AI models managed by Modzy to be used seamlessly within QGIS for geospatial analysis from counting cars in satellite imagery to quantifying damage to buildings and communities, to automatically aligning and registering aerial imagery. 

[![Modzy In Action](hhttps://files.readme.io/1a9ebd1-Screen_Shot_2021-07-30_at_8.13.07_AM.png)](https://docs.modzy.com/docs/qgis)

# Integration in Action

With AI power in QGIS, Modzy’s Vehicle Detection model quickly identifies every vehicle in the video. For a human reviewing hundreds of images per day, this is a daunting task—particularly when the images frequently change as vehicles move. Automating vehicle detection with Modzy speeds up this process, while ensuring consistency and accuracy every time.

[![Modzy In Action](https://img.youtube.com/vi/0CjHcPwdA0w/0.jpg)](https://www.youtube.com/watch?v=0CjHcPwdA0w)

# Installation 

- If you have not already, [install QGIS](https://qgis.org/en/site/forusers/download.html), including Python 3.9 and GDAL.
- Install the Modzy SDK to QGIS. 
    - Mac OS X: In a terminal, execute: `/Applications/QGIS.app/Contents/MacOS/bin/python3 -m pip install modzy-sdk`
    - Windows: In a terminal, execute: `C:\OSGeo4W\apps\Python39>pip install modzy-sdk`
    - To verify the Modzy SDK is installed, within QGIS open a Python Console. Type `import modzy` and press enter. If there are no errors, it was successfully installed!
- Install the Modzy Plugin:
    - Download the [stable version from the QGIS plugin repo](https://plugins.qgis.org/plugins/Modzy-QGIS-Plugin-main/) or the latest version [from GitHub](https://github.com/modzy/Modzy-QGIS-Plugin/archive/refs/heads/main.zip).
    - Within QGIS, go to the **Plugins > Manage and Install Plugins...** menu. 
    - Select **Install from ZIP** from the left panel.
    - Use the `...` button to navigate and select the downloaded Plugin zip file, or paste the path to the downloaded zip file into the `ZIP file:` text box. 
    - Click 'Install Plugin'
    - You should receive a 'Plugin installed successfully' message and Modzy will appear in the Processing Toolbox sidebar.
- Add your Modzy credentials.
    - Retrieve the appropriate API Key from your Modzy account. 
         - Log in to your instance of Modzy, or [https://app.modzy.com](https://app.modzy.com) if you are using a Modzy Basic account.
         - [Retrieve an appropriate Modzy API key](https://docs.modzy.com/docs/getting-started#key-download-your-api-key). It is a good idea to [create a new project](https://docs.modzy.com/docs/projects-3) and use the project API key to better organize and monitor activity related to this application.
    - In QGIS, use the **Settings > Options** menu
    - Choose **Authentication** from the left sidebar.
    - Click `+` in the upper right. 
    - Fill in these details to add a new credential: 
        - Name: `ModzyAPI`
        - Resource: `https://demo.modzy.engineering/api` or the url for your instance of Modzy
        - Select `Basic Authentication`
        - Username: `Modzy`
        - Password: Your Modzy API key from the previous step
        - Realm: leave blank.
    - Click `Save`

# Use
Each model may have different requirements and options, and your instance of Modzy may or may not include all GIS-relevant models. 


## Vehicle Detection
Modzy’s [Vehicle Detection model]() quickly identifies every vehicle in aerial imagery. For a human reviewing hundreds of images per day, this is a daunting task—particularly when the images frequently change as vehicles move. Automating vehicle detection with Modzy speeds up this process, while ensuring consistency and accuracy every time.  

The Vehicle Detection algorithm requires overhead imagery sliced into tiles no larger than 416px square. Users of this algorithm can create a VRT of larger imagery by specifying that column size, or may manually slice the imagery. Add those images as layers to QGIS, then:
- select the Vehicle Detection algorithm under Modzy's Satellite imagery toolkit. 
- Select the layer desired to run the count on, or select Run as Batch Process to run on a set of layers.
- Optionally select the Vector output layer. If this is left unspecified, the vectors will be saved in memory.
- Click Run.


## Building Damage classifier




# Modification for your own models

The Modzy plugin is open source with Apache2 license and is intended for repurposing – this plugin is intentionally "incomplete" with room to grow! Check out the [repository on Github](https://github.com/modzy/Modzy-QGIS-Plugin/). 

The best ways to start is to duplicate one of the ModelName_algorithm.py files within the repo and modifying the code inside to access your modelId and version. You will also need to specify the input and output data structures and rendering algorithms per your model's requirements. More help can always be found on our [Discord chat](https://discord.gg/Q7VrCDeW53)!