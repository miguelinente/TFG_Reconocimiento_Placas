import os
import shutil
import random
from PIL import Image, ImageOps

def create_dirs(base_dir):
    sets = ['train', 'validation', 'test']
    categories = ['clean', 'dirty']
    for set_name in sets:
        for category in categories:
            os.makedirs(os.path.join(base_dir, set_name, category), exist_ok=True)

def augment_image(img):
    # Realizar una rotación aleatoria de la imagen
    img = img.rotate(random.uniform(90, 270))
    # Aplicar espejado horizontal con probabilidad de 50%
    if random.random() > 0.5:
        img = ImageOps.mirror(img)
    return img

def split_data(source_dir, dest_dir, split_ratios):
    create_dirs(dest_dir)
    
    for category in ['Clean', 'Dirty']:
        category_path = os.path.join(source_dir, category)
        images = os.listdir(category_path)
        
        # Filtrar solo archivos que sean imágenes
        images = [img for img in images if os.path.isfile(os.path.join(category_path, img))]
        
        random.shuffle(images)
        
        train_split = int(split_ratios['train'] * len(images))
        val_split = int(split_ratios['validation'] * len(images))
        
        train_images = images[:train_split]
        val_images = images[train_split:train_split + val_split]
        test_images = images[train_split + val_split:]
        
        print(f"Category: {category}")
        print(f"Total images: {len(images)}")
        print(f"Train images: {len(train_images)}")
        print(f"Validation images: {len(val_images)}")
        print(f"Test images: {len(test_images)}")
        
        move_images(train_images, category_path, os.path.join(dest_dir, 'train', category.lower()), augment=True)
        move_images(val_images, category_path, os.path.join(dest_dir, 'validation', category.lower()))
        move_images(test_images, category_path, os.path.join(dest_dir, 'test', category.lower()))

def move_images(images, src_dir, dst_dir, augment=False):
    for image in images:
        src_path = os.path.join(src_dir, image)
        dst_path = os.path.join(dst_dir, image)
        
        # Copiar la imagen original
        shutil.copy(src_path, dst_path)
        
        if augment:
            # Guardar una versión aumentada de la imagen
            img = Image.open(src_path)
            img = augment_image(img)
            img = img.convert("RGB")
            # Crear un nuevo nombre para la imagen aumentada
            base, ext = os.path.splitext(image)
            augmented_image_path = os.path.join(dst_dir, f"{base}_augmented{ext}")
            img.save(augmented_image_path)
            

if __name__ == "__main__":
    source_directory = 'D:\Documents\Estudios\TFG\TensorFlow\Data'
    destination_directory = 'D:\Documents\Estudios\TFG\TensorFlow\Data_sorted'
    split_ratios = {'train': 0.7, 'validation': 0.15, 'test': 0.15}
    
    split_data(source_directory, destination_directory, split_ratios)
