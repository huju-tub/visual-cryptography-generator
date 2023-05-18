from classes.image_generator import ImageGenerator
from classes.image_encrypting import VisualCryptography
from classes.image_transparency import ImageTransparency
from classes.image_merger import ImageMerger


def main():
    # Change this line for different inputs
    text_input = "Test"

    private_key = None
    # Change this line for different private keys or comment it out to generate a new one
    private_key = "private_keys/hello_my_name_is_clara_brown.png"

    assert len(text_input) <= 8, "Input text should be up to 8 characters"

    # Generate the image
    img_gen = ImageGenerator(text_input)
    img_gen.create_image()

    # Prepare the image for encryption
    message_image = f"messages/{text_input}/message_{text_input}.png"
    vc = VisualCryptography(message=text_input, message_image=message_image, private_key=private_key)
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
