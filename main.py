import sys
import os
import argparse
from classes.image_generator import ImageGenerator
from classes.image_encrypting import VisualCryptography
from classes.image_transparency import ImageTransparency
from classes.image_merger import ImageMerger
from classes.image_upscaler import ImageUpscaler

MAX_TEXT_LENGTH = 10

def process_text(text_input, image_size_option, image_size, scale_factor, private_key_path):
    # Generate the image
    img_gen = ImageGenerator(text_input, image_size=image_size)
    img_gen.create_image()

    # Prepare the image for encryption
    image_suffix = "_small" if image_size_option == "small" else "_large"
    message_image = f"messages/{text_input}{image_suffix}/message_{text_input}{image_suffix}.png"
    vc = VisualCryptography(message=text_input, message_image=message_image, private_key=private_key_path,
                            image_suffix=image_suffix)
    vc.run()

    # Apply image transparency to the key images
    image_transparency = ImageTransparency()
    image_transparency.process_directory(f"messages/{text_input}{image_suffix}",
                                         f"messages/{text_input}{image_suffix}/transparent")

    # Merge the key images
    merger = ImageMerger(f"messages/{text_input}{image_suffix}/transparent/private_key_{text_input}{image_suffix}.png",
                         f"messages/{text_input}{image_suffix}/transparent/public_key_{text_input}{image_suffix}.png",
                         f"messages/{text_input}{image_suffix}/transparent/decrypted_message_{text_input}{image_suffix}.png")
    merger.process()

    image_transparency.make_transparent_white(
        f"messages/{text_input}{image_suffix}/transparent/decrypted_message_{text_input}{image_suffix}.png",
        f"messages/{text_input}{image_suffix}/decrypted_message_{text_input}{image_suffix}.png")

    image_upscaler = ImageUpscaler(f"messages/{text_input}{image_suffix}", scale_factor=scale_factor)
    image_upscaler.upscale_images_in_directory()


def main():
    parser = argparse.ArgumentParser(description='Image encryption tool')
    parser.add_argument('-t', '--text', help='The text to encrypt', default=None)
    parser.add_argument('-ss', '--split', help='Split Sentence: Split the words in sentence', action='store_true')
    parser.add_argument('-s', '--size', help='Image size: small or large', default="small")
    parser.add_argument('-f', '--file', help='The private key file', default=None)

    args = parser.parse_args()

    if args.text:
        if args.split:
            text_inputs = args.text.split()
        else:
            text_inputs = [args.text]
    else:
        if args.split:
            text_input = input("Enter the text to encrypt (max 10 characters per word): ")
            text_inputs = text_input.split()
        else:
            text_input = input("Enter the text to encrypt (max 10 characters): ")
            text_inputs = [text_input]

    for text_input in text_inputs:
        if len(text_input) > MAX_TEXT_LENGTH:
            print(f"Error: Input text '{text_input}' should be up to 10 characters.")
            continue

        if args.size.lower() == "small":
            image_size_option = "small"
            image_size = (50, 50)
            scale_factor = 4
        elif args.size.lower() == "large":
            image_size_option = "large"
            image_size = (100, 100)
            scale_factor = 2
        else:
            print("Invalid image size option.")
            return

        private_key_filename = args.file
        if not private_key_filename:
            private_key_filename = f"default_{image_size[0]}.png"
        private_key_path = f"private_keys/{private_key_filename}"
        private_key_extension = os.path.splitext(private_key_filename)[1]
        if private_key_extension.lower() != ".png":
            print("Private key file should be in PNG format.")
            return

        process_text(text_input, image_size_option, image_size, scale_factor, private_key_path)


if __name__ == "__main__":
    main()
