import cv2
import os


class VideoFromImages:
    def __init__(self, image_folder, video_name, fps):
        self.image_folder = os.path.join(os.getcwd(), image_folder)
        self.video_name = video_name
        self.fps = fps

    def make_video(self):
        images = [img for img in os.listdir(self.image_folder) if img.endswith(".png")]
        images.sort()  # so that the images are in order

        frame = cv2.imread(os.path.join(self.image_folder, images[0]))
        height, width, layers = frame.shape

        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.video_name), exist_ok=True)

        video = cv2.VideoWriter(self.video_name, cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(self.image_folder, image)))

        cv2.destroyAllWindows()
        video.release()
        print(f"Video saved to {self.video_name}")


def main():
    video_maker = VideoFromImages('../video_images/upscaled', '../videos/output_video.avi', 1)
    video_maker.make_video()


if __name__ == "__main__":
    main()
