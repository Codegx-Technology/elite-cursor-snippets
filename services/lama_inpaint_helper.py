import argparse
from pathlib import Path
from PIL import Image
import numpy as np
from lama_cleaner.model.lama import LaMa
import torch

def main():
    parser = argparse.ArgumentParser(description='Inpaint an image with LaMa Cleaner.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    parser.add_argument('mask_path', type=str, help='Path to the mask image.')
    parser.add_argument('output_path', type=str, help='Path to save the output image.')
    args = parser.parse_args()

    image = Image.open(args.image_path).convert('RGB')
    mask = Image.open(args.mask_path).convert('L')

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = LaMa(device=device)

    image_np = np.array(image)
    mask_np = np.array(mask)

    inpainted_image_np = model(image_np, mask_np)

    inpainted_image = Image.fromarray(inpainted_image_np)
    inpainted_image.save(args.output_path)

    print(args.output_path)

if __name__ == '__main__':
    main()
