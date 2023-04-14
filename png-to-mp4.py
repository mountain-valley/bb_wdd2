import json
import shutil

import cv2
import ffmpeg
import os
import dateutil.parser as parser
from datetime import datetime

def get_all_videos(apng_folder_path, output_folder_path='waggle_apngs'):
    """
    recursively get all directories with apng files in them under the apng_folder_path and put them in a new folder
    Args:
        apng_folder_path:
        output_folder_path:

    Returns:

    """
    # recursively get all directories with apng files in them under the apng_folder_path and put them in a new folder
    for root, dirs, files in os.walk(apng_folder_path):
        if len(files) != 0:
            # get .apng file only (not all files in folder are .apng files)
            first_image = os.listdir(root)[0]
            # move .apng file to new folder
            os.rename(os.path.join(root, first_image), os.path.join(output_folder_path, first_image))
            return
        for dir in dirs:
            get_all_videos(os.path.join(root, dir))

def get_all_dir(png_folder_path, output_folder_path='waggle_videos'):
    """
    recursively get all directories with png files in them under the png_folder_path and convert the png files to mp4
    """
    for root, dirs, files in os.walk(png_folder_path):
        if len(dirs) == 0:
            convert_png_to_mp4(root, output_folder_path)
            return
        for dir in dirs:
            get_all_dir(os.path.join(root, dir))

def convert_png_to_mp4(png_folder_path, output_folder_path='waggle_videos'):
    # if the output_folder_path does not exist, create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # width = 1920
    # height = 1080
    fps = 30
    # get width, height from first image
    first_image = os.listdir(png_folder_path)[0]
    first_image_path = os.path.join(png_folder_path, first_image)
    img = cv2.imread(first_image_path)
    height, width, layers = img.shape

    # # get frames count
    # frames_count = len(os.listdir(png_folder_path))

    # create the video writer and write to a new mp4 file with the same name as the png folder to a specific output folder
    # print(f'folder: {png_folder_path}, fps: {fps}, frames_count: {frames_count}, width: {width}, height: {height}')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(os.path.join(output_folder_path, png_folder_path[16:].replace('/', '-') + '.mp4'), fourcc, fps, (width, height))

    # iterate over the PNG images in a folder
    png_files = sorted([f for f in os.listdir(png_folder_path) if f.endswith('.png')])
    for png_file in png_files:
        img = cv2.imread(os.path.join(png_folder_path, png_file))
        out.write(img)

    # release the video writer
    out.release()

def convert_json_to_csv(wdd_output_folder_path, json_folder_path="waggle_jsons", output_folder_path='waggle_csvs', start_timestamp=0, fps=30.0):
    """
    combine the information in the json files in the json_folder_path into a single csv file
    """
    # if the output_folder_path does not exist, create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # if the "waggle_jsons" folder does not exist, create it
    if not os.path.exists(json_folder_path):
        os.makedirs(json_folder_path)
    get_all_json(wdd_output_folder_path, json_folder_path)

    # get all json files in the json_folder_path
    json_files = sorted([f for f in os.listdir(json_folder_path) if f.endswith('.json')])

    # create a new csv file in the output_folder_path
    csv_file = open(os.path.join(output_folder_path, 'wdd_output' + '.csv'), 'w')
    # write the header of the csv file
    csv_file.write('startFrame,endFrame,endFrame2,angle,duration,duration2,startPointX,startPointY,endPointX,endPointY,\n')

    # iterate over the json files in the json_folder_path
    for json_file in json_files:
        # read the json file
        json_data = open(os.path.join(json_folder_path, json_file))
        # get the data from the json file
        data = json.load(json_data)
        # write the data to the csv file
        timestamp_begin = data["timestamp_begin"]  # ISO format, e.g. 2020-07-01T00:00:00.000Z
        duration = data["waggle_duration"]
        start_frame = (parser.parse(timestamp_begin) - parser.parse(start_timestamp)).total_seconds() * fps
        # deal with duration being None / null
        if duration is None:
            duration = 0
        end_frame = start_frame + duration * fps
        end_frame2 = (parser.parse(data["camera_timestamps"][-1]) - parser.parse(start_timestamp)).total_seconds() * fps
        duration2 = (parser.parse(data["camera_timestamps"][-1]) - parser.parse(data["camera_timestamps"][0])).total_seconds()
        duration3 = (parser.parse(data["frame_timestamps"][-1]) - parser.parse(data["frame_timestamps"][0])).total_seconds()
        duration4 = (parser.parse(data["frame_timestamps"][-1]) - parser.parse(timestamp_begin)).total_seconds()
        print(f'start_frame: {start_frame}, end_frame: {end_frame}, end_frame2: {end_frame2}, duration: {duration}, duration2: {duration2}, duration3: {duration3}, duration4: {duration4}')

        csv_file.write(f'{start_frame},{end_frame},{end_frame2},{data["waggle_angle"]},{data["waggle_duration"]},{duration2},{data["x_coordinates"][0]},{data["y_coordinates"][0]},{data["x_coordinates"][-1]},{data["y_coordinates"][-1]}\n')

def get_all_json(json_folder_path, output_folder_path='waggle_jsons'):
    # recursively get all directories with apng files in them under the apng_folder_path and put them in a new folder
    for root, dirs, files in os.walk(json_folder_path):
        if len(files) != 0:
            # get .json file only (not all files in folder are .json files)
            json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]
            # copy .json file to new folder
            for json_file in json_files:
                shutil.copy(os.path.join(root, json_file), os.path.join(output_folder_path, json_folder_path[17:].replace('/', '-') + '.json'))
                # os.rename(os.path.join(root, json_file), os.path.join(output_folder_path, json_file))
            return
        for dir in dirs:
            get_all_json(os.path.join(root, dir))

if __name__ == '__main__':
    # get_all_dir('output/cam0', 'waggle_videos')
    # get_all_videos('output/cam0', 'waggle_apngs')
    convert_json_to_csv('output/cam0', output_folder_path='waggle_csvs', start_timestamp="2022-08-07T14:35:42+00:00")
