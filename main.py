import cv2
import argparse
import numpy as np
from utils import RGBPreprocess
from matplotlib import pyplot as plt
import os
import pandas
from PIL import Image
from config import config as cfg

RGB_IMG = './rgbimages/GWS4_I2.0_F1.9_L80_110410_12_2_0_rgb.jpg' 
RGB_DIR = 'rgbimages/'

def get_arguments():
    """
        Parse all the command line arguments.
    """
    parser = argparse.ArgumentParser(description="label-components")
    parser.add_argument("--rgb-img", type=str, default=RGB_IMG, help="RGB image")
    parser.add_argument("--rgb", action='store_true', help="run for single rgb file.")
    parser.add_argument("--dir", type=str, default=RGB_DIR, help="Directory for RGB images")
    return parser.parse_args()

def main():
    print("Arguments: ")
    args = get_arguments()
    
    if args.rgb:
        rgb_path = args.rgb_img.replace("'","")
        print("RGB image: ", rgb_path)
        currdir = os.getcwd()
        file_name = os.path.join(os.path.join(currdir,'output'), '.'.join(rgb_path.split('/')[-1].split('.')[:-1]) + '.csv')
        output_name = os.path.join(os.path.join(currdir,'output'), '.'.join(rgb_path.split('/')[-1].split('.')[:-1]) + '.png')
        
        # Process the image
        rgb = RGBPreprocess()
        rgb_img = cv2.imread(rgb_path)        
        label, data = rgb.process_img(rgb_img)
        print(data)
        data.to_csv(path_or_buf=file_name, sep=',', index=False)
        
        # save the labeled image
        im = Image.fromarray(label)
        im.putpalette(cfg.colormap)
        im.save(output_name)

    else:
        print("Reading files from directory: ", args.dir)
        currdir = os.getcwd()
        dir_name = os.path.join(currdir, args.dir) 
        file_list = os.listdir(dir_name)
        print(file_list)

        for rgbfile in file_list:

            file_name = os.path.join(os.path.join(currdir,'output'), '.'.join(rgbfile.split('/')[-1].split('.')[:-1]) + '.csv')
            output_name = os.path.join(os.path.join(currdir,'output'), '.'.join(rgbfile.split('/')[-1].split('.')[:-1]) + '.png')
            rgbfile = os.path.join(dir_name, rgbfile)
            print("RGB image: ", rgbfile)
            
            # Process each image
            rgb = RGBPreprocess()
            rgb_img = cv2.imread(rgbfile)
            label, data = rgb.process_img(rgb_img)
            print(data)
            data.to_csv(path_or_buf=file_name, sep=',', index=False)
        
            # save the labeled image
            im = Image.fromarray(label)
            im.putpalette(cfg.colormap)
            im.save(output_name)

if __name__ == '__main__':
    main()
