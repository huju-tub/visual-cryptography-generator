import sys
import os
import argparse
from classes.image_generator import ImageGenerator
from classes.image_encrypting import ImageEncrypting
from classes.image_transparency import ImageTransparency
from classes.image_merger import ImageMerger
from classes.image_upscaler import ImageUpscaler
from classes.video_from_images import VideoFromImages
import shutil

MAX_TEXT_LENGTH = 10


def process_text(idx, text_input, image_suffix, image_size, scale_factor, private_key_path, video_scale_factor=10):
    # Generate the image
    img_gen = ImageGenerator(text_input, image_size=image_size)
    img_gen.create_image()

    # Prepare the image for encryption
    message_image = f"messages/{text_input}{image_suffix}/message_{text_input}{image_suffix}.png"
    encrypting = ImageEncrypting(message=text_input, message_image=message_image, private_key=private_key_path,
                                 image_suffix=image_suffix)
    encrypting.run()

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


def video_creator(idx, image_type, image_suffix, text_input, video_scale_factor=10):
    # PUBLIC KEY
    # After processing text, copy the file to video_images directory
    directory_name = f"video_images/{image_type}"
    os.makedirs(directory_name, exist_ok=True)
    src = f"messages/{text_input}{image_suffix}/{image_type}_{text_input}{image_suffix}.png"
    dest = f"{directory_name}/{idx}_{image_type}_{text_input}{image_suffix}.png"
    shutil.copy2(src, dest)
    # Upscale the images in video_images directory
    video_image_upscaler = ImageUpscaler(directory_name, scale_factor=video_scale_factor)
    video_image_upscaler.upscale_images_in_directory()


def main():
    parser = argparse.ArgumentParser(description='Image encryption tool')
    parser.add_argument('-t', '--text', help='The text to encrypt', default=None)
    parser.add_argument('-ss', '--split', help='Split Sentence: Split the words in sentence', action='store_true')
    parser.add_argument('-s', '--size', help='Image size: small or large', default="small")
    parser.add_argument('-f', '--file', help='The private key file', default=None)
    parser.add_argument('-v', '--video', help='Video: Create a video from sentence', action='store_true')

    args = parser.parse_args()

    if args.video and not args.split:
        print("Error: Video option can only be used with split option.")
        return
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

    for idx, text_input in enumerate(text_inputs):
        if len(text_input) > MAX_TEXT_LENGTH:
            print(f"Error: Input text '{text_input}' should be up to 10 characters.")
            continue

        if args.size.lower() == "small":
            image_suffix = "_small"
            image_size = (50, 50)
            scale_factor = 4
        elif args.size.lower() == "large":
            image_suffix = "_large"
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

        process_text(idx, text_input, image_suffix, image_size, scale_factor, private_key_path)
        if args.video:
            video_creator(idx, "message", image_suffix, text_input)
            video_creator(idx, "public_key", image_suffix, text_input)

    if args.video:
        # Make a video from the images in video_images directory
        video_maker = VideoFromImages("video_images/message/upscaled", "videos/original.avi", 2)
        video_maker.make_video()
        video_maker = VideoFromImages("video_images/public_key/upscaled", "videos/encrypted.avi", 2)
        video_maker.make_video()

        # Delete contents of video_images directory
        shutil.rmtree('video_images')


if __name__ == "__main__":
    main()
