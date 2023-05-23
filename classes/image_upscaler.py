import os
from PIL import Image


class ImageUpscaler:
    def __init__(self, image_path, scale_factor):
        self.image_path = image_path
        self.scale_factor = scale_factor

    def upscale_image(self, image_file):
        # Open the image
        image = Image.open(image_file)

        # Calculate the new dimensions
        width, height = image.size
        new_width = int(width * self.scale_factor)
        new_height = int(height * self.scale_factor)

        # Resize the image
        upscaled_image = image.resize((new_width, new_height), Image.BICUBIC)

        # Save the upscaled image
        upscaled_folder = os.path.join(self.image_path, 'upscaled')
        os.makedirs(upscaled_folder, exist_ok=True)

        file_name = os.path.splitext(os.path.basename(image_file))[0]
        save_path = os.path.join(upscaled_folder, f'{file_name}_upscaled.png')
        upscaled_image.save(save_path)

        # print(f"Upscaled image saved: {save_path}")

    def upscale_images_in_directory(self):
        # Get a list of all image files in the directory
        image_files = [
            os.path.join(self.image_path, file_name)
            for file_name in os.listdir(self.image_path)
            if file_name.endswith(('.jpg', '.jpeg', '.png'))
        ]

        for image_file in image_files:
            self.upscale_image(image_file)


if __name__ == '__main__':
    directory_path = '../private_keys'
    scale_factor = 4  # Increase the dimensions by a factor of 4

    upscaler = ImageUpscaler(directory_path, scale_factor)
    upscaler.upscale_images_in_directory()
