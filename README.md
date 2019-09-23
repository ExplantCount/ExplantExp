# Image Labeling and count explants
Separate explants on the grid, label them from left to right, top to bottom. 
Find the feature (area in terms of number of pixels and center) for each explant. 

### To install the dependencies using pip.
To install the dependencies using pip, run the command -
```bash
pip install -r requirements.txt
```

### Create an output folder in the ExplantCount folder using the command -
```bash
mkdir output
```
(this commands works for the unix and MAC OS system)


### To run the scripts for a single RGB image and hyperspectral matrix pair, use the command:
```bash
python main.py --rgb-img rgb_image_name_with_path --rgb
```
Example:
```bash
python main.py --rgb-img='./rgbimages/GWS5_I2.0_F1.9_L80_113040_3_0_3_rgb.jpg' --rgb
```

### To run for all the images in a directory.
Run the script using the command - 
```bash
python main.py --dir dirname
```
Example:
```bash
python main.py --dir rgbimages
```

### The directory structure before running the scripts should look like -
ExplantCount

+-- config.py

+-- rgbimages (Folder where RGB images are stored.)

|   +-- RGB_image file

+-- Output (Target directory where output will be stored.)

+-- utils.py

+-- README.md

+-- main.py
        

See directories rgbimages and output for example images.
