from PIL import Image

class ImageMerger:

    def __init__(self, image1_path, image2_path, result_path):
        self.image1_path = image1_path
        self.image2_path = image2_path
        self.result_path = result_path

    def load_images(self):
        self.image1 = Image.open(self.image1_path)
        self.image2 = Image.open(self.image2_path)
        assert self.image1.size == self.image2.size, "Images must be the same size"

    def merge_images(self):
        self.result = Image.new('RGBA', self.image1.size)
        self.result.paste(self.image1, (0, 0))
        self.result.paste(self.image2, (0, 0), mask=self.image2)

    def save_result(self):
        self.result.save(self.result_path, 'PNG')

    def process(self):
        self.load_images()
        self.merge_images()
        self.save_result()


if __name__ == "__main__":
    pass
