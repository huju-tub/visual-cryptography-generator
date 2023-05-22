import sys
import os
from classes.image_generator import ImageGenerator
from classes.image_encrypting import VisualCryptography
from classes.image_transparency import ImageTransparency
from classes.image_merger import ImageMerger
from classes.image_upscaler import ImageUpscaler

MAX_TEXT_LENGTH = 10


def main():
    if len(sys.argv) < 2:
        text_input = input("Enter the text to encrypt (max 10 characters): ")
        if len(text_input) > MAX_TEXT_LENGTH:
            print("Error: Input text should be up to 10 characters.")
            return
        private_key_filename = input("Enter the private key filename (default.png if not specified): ")
        if not private_key_filename:
            private_key_filename = "default.png"
    elif len(sys.argv) == 2:
        text_input = sys.argv[1]
        if len(text_input) > MAX_TEXT_LENGTH:
            print("Error: Input text should be up to 10 characters.")
            return
        private_key_filename = "default.png"
    else:
        text_input = sys.argv[1]
        if len(text_input) > MAX_TEXT_LENGTH:
            print("Error: Input text should be up to 10 characters.")
            return
        private_key_filename = sys.argv[2]

    private_key_path = f"private_keys/{private_key_filename}"
    private_key_extension = os.path.splitext(private_key_filename)[1]

    if private_key_extension.lower() != ".png":
        print("Private key file should be in PNG format.")
        return

    image_size_option = input("Select image size (small/large): ")
    if image_size_option.lower() == "small":
        image_size = (50, 50)
        scale_factor = 4
        image_suffix = "_small"
    elif image_size_option.lower() == "large":
        image_size = (100, 100)
        scale_factor = 2
        image_suffix = "_large"
    else:
        print("Invalid image size option.")
        return

    # Generate the image
    img_gen = ImageGenerator(text_input, image_size=image_size)
    img_gen.create_image()

    # Prepare the image for encryption
    message_image = f"messages/{text_input}{image_suffix}/message_{text_input}{image_suffix}.png"
    vc = VisualCryptography(message=text_input, message_image=message_image, private_key=private_key_path, image_suffix=image_suffix)
    vc.run()

    # Apply image transparency to the key images
    image_transparency = ImageTransparency()
    image_transparency.process_directory(f"messages/{text_input}{image_suffix}", f"messages/{text_input}{image_suffix}/transparent")

    # Merge the key images
    merger = ImageMerger(f"messages/{text_input}{image_suffix}/transparent/private_key_{text_input}{image_suffix}.png",
                         f"messages/{text_input}{image_suffix}/transparent/public_key_{text_input}{image_suffix}.png",
                         f"messages/{text_input}{image_suffix}/transparent/decrypted_message{image_suffix}.png")
    merger.process()

    image_transparency.make_transparent_white(f"messages/{text_input}{image_suffix}/transparent/decrypted_message{image_suffix}.png",
                                              f"messages/{text_input}{image_suffix}/decrypted_message{image_suffix}.png")

    image_upscaler = ImageUpscaler(f"messages/{text_input}{image_suffix}", scale_factor=scale_factor)
    image_upscaler.upscale_images_in_directory()


if __name__ == "__main__":
    main()
