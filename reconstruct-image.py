#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to reconstruct 2D optical tomography projections and save as multi-page TIFF files.
"""

import glob
import numpy as np
import os
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize
import tifffile
import tomopy

from mayavi import mlab

def read_and_preprocess_images(directory):
    """ Reads and preprocesses images, converting to grayscale and resizing. """
    file_paths = sorted(glob.glob(f"{directory}/image_*.jpg"), key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))
    images = []
    for file_path in file_paths:
        img = imread(file_path)
        img_gray = rgb2gray(img)
        img_resized = resize(img_gray, (img_gray.shape[0] // 4, img_gray.shape[1] // 4), anti_aliasing=True)
        images.append(img_resized)
    return np.stack(images, axis=0).astype('float32')

def normalize_images(images):
    """ Normalizes images using a flat field correction. """
    flat = np.mean(images, axis=0)
    return images / flat

def reconstruct_tomography(images, angles, center):
    """ Reconstructs a 3D volume from 2D projections. """
    images = tomopy.minus_log(images)
    theta = tomopy.angles(len(images), angles[0], angles[1])
    recon = tomopy.recon(images, theta, center=center, algorithm='gridrec')
    return tomopy.circ_mask(recon, axis=0, ratio=0.95)

def ensure_directory_exists(file_path):
    """ Ensures the directory for the specified file path exists. """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_tiff_stack(data, file_path):
    """ Saves an array of images to a multi-page TIFF file. """
    ensure_directory_exists(file_path)
    tifffile.imsave(file_path, data.astype('float32'), photometric='minisblack')
    
def visualize_volume(data):
    """ Visualizes a 3D volume using Mayavi's contour3d. """
    mlab.figure(bgcolor=(0, 0, 0))
    mlab.contour3d(data, contours=10, transparent=True, opacity=0.5)
    mlab.colorbar(orientation='vertical', title='Intensity')
    print('Here at visualization')
    mlab.show()


def main():
    directory = <enter-path-to-directory-containing-image> # Path to the directory containing images
    output_projections = <enter-path-for-projections> # Path to projections tiff file
    output_volume = <enter-path-for-volume> # Path to volume tiff file
    angles = (0, 360)
    center = 180  # Adjust the center of rotation if necessary

    # Process images
    images = read_and_preprocess_images(directory)
    normalized_images = normalize_images(images)

    # Save all normalized projections as a TIFF file
    save_tiff_stack(normalized_images, output_projections)

    # Reconstruct the volume and save it
    reconstructed_volume = reconstruct_tomography(normalized_images, angles, center)
    save_tiff_stack(reconstructed_volume, output_volume)
    
    visualize_volume(reconstructed_volume)

if __name__ == "__main__":
    main()
