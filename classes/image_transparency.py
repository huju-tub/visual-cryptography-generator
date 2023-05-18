from PIL import Image
import os


class ImageTransparency:

    @staticmethod
    def make_background_transparent(img_path, output_path):
        img = Image.open(img_path)
        img = img.convert("RGBA")

        datas = img.getdata()

        new_data = []
        for item in datas:
            # change all white (also shades of whites)
            # pixels to transparent
            if item[0] in list(range(200, 256)):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(output_path, "PNG")

    @staticmethod
    def make_transparent_white(img_path, output_path):
        img = Image.open(img_path)
        img = img.convert("RGBA")

        datas = img.getdata()

        new_data = []
        for item in datas:
            # change all transparent pixels to white
            if item[3] == 0:
                new_data.append((255, 255, 255, 255))
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(output_path, "PNG")

    def process_directory(self, input_dir, output_dir):
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in os.listdir(input_dir):
            if filename.endswith(".png"):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                self.make_background_transparent(input_path, output_path)


if __name__ == "__main__":
    remover = ImageTransparency()
    remover.process_directory("images", "images_transparent")
