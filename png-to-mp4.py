import cv2
import ffmpeg
import os

def convert_mkv_to_mp4(output_file, png_folder_path):
    # # Read the .mkv file
    # cap = cv2.VideoCapture(input_file)
    #
    # # Get the frames properties
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # if fps == 0:
    #     print("Error reading video file. Skipping this video")
    #     return
    # frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # `width`
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # `height`

    frames_count = 9000
    width = 1920
    height = 1080
    fps = 30

    # create the video writer
    print(f'fps: {fps}, frames_count: {frames_count}, width: {width}, height: {height}')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # # Read frames from the input file and write to the output file
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the color format from BGR to RGB
    #     out.write(frame)
    #
    # # Close the input and output files
    # cap.release()
    # out.release()


    # iterate over the PNG images in a folder
    png_files = sorted([f for f in os.listdir(png_folder_path) if f.endswith('.png')])
    for png_file in png_files:
        # read the PNG image and convert it to BGR format
        png_path = os.path.join(png_folder_path, png_file)
        bgr_image = cv2.imread(png_path)

        # write the BGR image to the video
        out.write(bgr_image)

    # release the video writer
    out.release()

if __name__ == '__main__':
    convert_mkv_to_mp4('bee-video-sample.mov', 'bee-video-sample.mp4')