import requests
from PIL import Image
from io import BytesIO
import os
import cv2
import numpy as np


def download_logo(logo_url, save_path):
    try:
        response=requests.get(logo_url)
        response.raise_for_status() #verificare daca cererea a avut succes
        img=Image.open(BytesIO(response.content))
        img.save(save_path)
        print(f"Logo saved to {save_path}")
    except Exception as e:
        print(f"Error downloading logo from {logo_url}: {e}")

def process_image(image_path, output_size=(128,128)):
    try:
        img=cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Could not read image: {image_path}")
            return None

        img=cv2.resize(img, output_size)

        #grayscale
        if len(img.shape)==3:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #delete background
        _, img = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY_INV)

        #save
        cv2.imwrite(image_path, img)
        print(f"Processed image saved to: {image_path}")
        return img
    except Exception as e:
        print(f"Error processing image: {image_path}: {e}")
        return None