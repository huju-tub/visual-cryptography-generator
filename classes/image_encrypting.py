from PIL import Image
import os
import random

class VisualCryptography:
    def __init__(self, message, message_image, private_key=None):
        self.message = message
        self.message_image = message_image
        self.private_key = private_key

    def load_image(self, name):
        return Image.open(name)

    def prepare_message_image(self, image, size):
        if size != image.size:
            image = image.resize(size, Image.ANTIALIAS)
        return image.convert("1")

    def generate_private_key(self, size, secret_image=None):
        width, height = size
        private_key_image = Image.new(mode="1", size=(width * 2, height * 2))
        if secret_image:
            old_width, old_height = secret_image.size
        else:
            old_width, old_height = (-1, -1)

        for x in range(0, 2 * width, 2):
            for y in range(0, 2 * height, 2):
                if x < old_width and y < old_height:
                    color = secret_image.getpixel((x, y))
                else:
                    color = random.getrandbits(1)
                private_key_image.putpixel((x, y), color)
                private_key_image.putpixel((x + 1, y), 1 - color)
                private_key_image.putpixel((x, y + 1), 1 - color)
                private_key_image.putpixel((x + 1, y + 1), color)
        return private_key_image

    def generate_public_key(self, secret_image, prepared_image):
        width, height = prepared_image.size
        public_key_image = Image.new(mode="1", size=(width * 2, height * 2))
        for x in range(0, width * 2, 2):
            for y in range(0, height * 2, 2):
                secret = secret_image.getpixel((x, y))
                message = prepared_image.getpixel((x // 2, y // 2))
                if (message > 0 and secret > 0) or (message == 0 and secret == 0):
                    color = 0
                else:
                    color = 1
                public_key_image.putpixel((x, y), 1 - color)
                public_key_image.putpixel((x + 1, y), color)
                public_key_image.putpixel((x, y + 1), color)
                public_key_image.putpixel((x + 1, y + 1), 1 - color)
        return public_key_image

    def run(self):
        try:
            message_image = self.load_image(self.message_image)
        except IOError as e:
            print(f"Error: Failed to load message image '{self.message_image}': {str(e)}")
            return

        size = message_image.size

        width, height = size
        isWithPrivateKey = False

        if not self.private_key:
            self.private_key = f"messages/{self.message}/private_key_{self.message}.png"
            private_key_image = self.generate_private_key(size)
        elif not os.path.isfile(self.private_key):
            isWithPrivateKey = True
            private_key_image = self.generate_private_key(size)
        else:
            try:
                isWithPrivateKey = True
                private_key_image = self.load_image(self.private_key)
            except IOError as e:
                print(f"Error: Failed to load private key image '{self.private_key}': {str(e)}")
                return

            # if private_key_image.size != size:
            #     print(f"Error: Private key image '{self.private_key}' is not the same size as the message image")
            #     return

        prepared_image = self.prepare_message_image(message_image, size)
        public_key_image = self.generate_public_key(private_key_image, prepared_image)

        public_key_filename = f"messages/{self.message}/public_key_{self.message}.png"

        try:
            os.makedirs(os.path.dirname(self.private_key), exist_ok=True)
            private_key_image.save(f"messages/{self.message}/private_key_{self.message}.png")
            if isWithPrivateKey:
                private_key_image.save(self.private_key)
                print(f"Saved private key image as '{self.private_key}'")
            print(f"Saved private key image as 'messages/{self.message}/private_key_{self.message}.png'")
        except IOError as e:
            print(f"Error: Failed to save private key image '{self.private_key}': {str(e)}")

        try:
            os.makedirs(os.path.dirname(public_key_filename), exist_ok=True)
            public_key_image.save(public_key_filename)
            print(f"Saved public key image as '{public_key_filename}'")
        except IOError as e:
            print(f"Error: Failed to save public key image '{public_key_filename}': {str(e)}")





if __name__ == "__main__":
    VisualCryptography(message="TEST2", message_image="../messages/TEST2/message_TEST2.png").run()
