import sys
import os
from classes.image_generator import ImageGenerator
from classes.image_encrypting import VisualCryptography
from classes.image_transparency import ImageTransparency
from classes.image_merger import ImageMerger

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <text> <private_key>")
        return

    text_input = sys.argv[1]
    private_key_filename = sys.argv[2]
    private_key_path = f"private_keys/{private_key_filename}"
    private_key_extension = os.path.splitext(private_key_filename)[1]

    if private_key_extension.lower() != ".png":
        print("Private key file should be in PNG format.")
        return

    # Generate the image
    img_gen = ImageGenerator(text_input)
    img_gen.create_image()

    # Prepare the image for encryption
    message_image = f"messages/{text_input}/message_{text_input}.png"
    vc = VisualCryptography(message=text_input, message_image=message_image, private_key=private_key_path)
    vc.run()

    # Apply image transparency to the key images
    image_transparency = ImageTransparency()
    image_transparency.process_directory(f"messages/{text_input}", f"messages/{text_input}/transparent")

    # Merge the key images
    merger = ImageMerger(f"messages/{text_input}/transparent/private_key_{text_input}.png",
                         f"messages/{text_input}/transparent/public_key_{text_input}.png",
                         f"messages/{text_input}/transparent/decrypted_message.png")
    merger.process()

    image_transparency.make_transparent_white(f"messages/{text_input}/transparent/decrypted_message.png", f"messages/{text_input}/decrypted_message.png")


if __name__ == "__main__":
    main()
