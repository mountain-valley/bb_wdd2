import cv2
import ffmpeg
import os

def convert_png_to_mp4(output_file, png_folder_path):
    # width = 1920
    # height = 1080
    fps = 30
    # get width, height from first image
    first_image = os.listdir(png_folder_path)[0]
    first_image_path = os.path.join(png_folder_path, first_image)
    img = cv2.imread(first_image_path)
    height, width, layers = img.shape
    
    # get frames count
    frames_count = len(os.listdir(png_folder_path))

    # create the video writer
    print(f'fps: {fps}, frames_count: {frames_count}, width: {width}, height: {height}')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # iterate over the PNG images in a folder
    for i in range(frames_count):
        img = cv2.imread(os.path.join(png_folder_path, f'{i}.png'))
        out.write(img)

    # png_files = sorted([f for f in os.listdir(png_folder_path) if f.endswith('.png')])
    # for png_file in png_files:
    #     # read the PNG image and convert it to BGR format
    #     png_path = os.path.join(png_folder_path, png_file)
    #     bgr_image = cv2.imread(png_path)
    # 
    #     # write the BGR image to the video
    #     out.write(bgr_image)

    # release the video writer
    out.release()

if __name__ == '__main__':
    convert_png_to_mp4('bee-video-sample.mov', 'bee-video-sample.mp4')
