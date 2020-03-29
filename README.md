# fw_core library 

This repository contains commons code to build Flask applications

## How to upload this package to PyPi
Now, the final step has come: uploading your project to PyPi. First, open the command prompt and navigate into your the folder where you have all your files and your package located:
```
cd "YOUR FW_CORE root project"
```
Now, we create a source distribution with the following command:
```
python setup.py sdist
```
You might get a warning stating “Unknown distribution option: ‘install_requires’. Just ignore it.
We will need twine for the upload process, so first install twine via pip:
```
pip install twine
```
Then, run the following command:
```
twine upload dist/*
```
You will be asked to provide your username and password. Provide the credentials you used to register to PyPi earlier.

#### Congratulations, your package is now uploaded! 
Visit https://pypi.org/project/fw_core/ to see your package online! 