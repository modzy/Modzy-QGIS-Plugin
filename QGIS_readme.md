QGIS Integration

# Mac
- [Install QGIS](https://qgis.org/en/site/forusers/download.html), including Python 3.9 and GDAL.
- Install Modzy-sdk: 
	- in a terminal, execute: `/Applications/QGIS.app/Contents/MacOS/bin/python3 -m pip install modzy-sdk`
  	- To be sure Modzy is installed, open QGIS and open a Python Console window, type `import modzy`. If there are no errors, it is installed!
- Install the Modzy plugin.
	- steps
- Add Credentials
	- Go to Settings > Options > 
	- Choose Authentication
	- Click + 
	- Name: ModzyAPI
	- Resource: https://demo.modzy.engineering/api
	- Basic Authentication
	- Username: Modzy
	- Password: your key



- OLD Install Modzy-SDK: 
  - In QGIS, go to menu Settings > Options and click System in the side bar
  - Scroll down to Environment and view 'Current Environment Variables'
  - Find the 'PATH' variable which should be something like `/Library/Frameworks/Python.framework/Versions/3.9/bin`
  - In a Terminal window, using the path from the previous step, typ `<path_to_python>/python3 -m pip install modzy-sdk`, for example: `/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 -m pip install modzy-sdk`
