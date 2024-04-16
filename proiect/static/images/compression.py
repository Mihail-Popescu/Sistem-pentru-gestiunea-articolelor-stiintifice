import os
import imageio

original_dir = 'C:\\GitHub Projects\\Licenta\\Sistem-pentru-gestiunea-articolelor-stiintifice\\proiect\\static\\images'
compressed_dir = 'C:\\GitHub Projects\\Licenta\\Sistem-pentru-gestiunea-articolelor-stiintifice\\proiect\\static\\compressed_images'

if not os.path.exists(compressed_dir):
    os.makedirs(compressed_dir)

for filename in os.listdir(original_dir):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):

        img_path = os.path.join(original_dir, filename)
        img = imageio.imread(img_path)

        compressed_path = os.path.join(compressed_dir, filename)
        imageio.imwrite(compressed_path, img, compression='lzw')

print("Compression completed!")
