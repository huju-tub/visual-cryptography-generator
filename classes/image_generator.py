from PIL import Image, ImageDraw, ImageFont
import os


class ImageGenerator:
    def __init__(self, text, font_path='fonts/arial/arial.ttf', image_size=(50, 50), font_size=10):
        self.text = text
        self.font_path = font_path
        self.image_size = image_size
        self.image_suffix = "_small" if image_size == (50, 50) else "_large"
        self.font_size = font_size

    def create_image(self):
        # Create a new image with black and white mode
        image = Image.new('1', self.image_size, 'white')
        draw = ImageDraw.Draw(image)

        # Load a truetype or opentype font file, and create a font object.
        font = ImageFont.truetype(self.font_path, self.font_size)

        # Calculate width and height of the text to center it
        text_width, text_height = draw.textbbox((0, 0), self.text, font=font)[2:4]
        text_x = (self.image_size[0] - text_width) // 2
        text_y = (self.image_size[1] - text_height) // 2

        # Add text to image
        draw.text((text_x, text_y), self.text, fill='black', font=font)

        # Ensure the "messages" directory exists
        if not os.path.exists('messages'):
            os.makedirs('messages')

        # Ensure the directory named after the input text exists
        folder_path = os.path.join('messages', self.text + self.image_suffix)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the image with the input text prefixed with "message_"
        image_path = os.path.join(folder_path, f'message_{self.text}{self.image_suffix}.png')
        image.save(image_path)


def main():
    text_input = input("Enter your text (1-10 characters): ")  # User-provided input
    assert 1 <= len(text_input) <= 10, "Input text should be 1 to 8 characters long"
    img_gen = ImageGenerator(text_input)
    img_gen.create_image()


if __name__ == "__main__":
    main()
