import os
import cv2
import numpy as np
import ffmpeg
from wdd.decoding import WaggleDecoder
import pandas as pd

# get png images from a folder into an array of images
def get_png_images(png_folder_path):
    png_files = sorted([f for f in os.listdir(png_folder_path) if f.endswith('.png')])
    images = []
    for png_file in png_files:
        img = cv2.imread(os.path.join(png_folder_path, png_file), cv2.IMREAD_GRAYSCALE)  #TODO: There could be an error in the type of image it is interpreting. See argument "mode" in cv2.imread()
        images.append(img)
    return images

# get ground truth angles from csv
def get_ground_truth_angles(csv_file_path):
    with open(csv_file_path, 'r') as f:
        lines = f.readlines()
        angles = []
        flipped_angles = []
        for i, line in enumerate(lines):
            if i == 0:
                continue
            try:
                angle = float(line.split(',')[1])
                angles.append(angle)
                f_angle = float(line.split(',')[3])
                flipped_angles.append(f_angle)
            except:
                continue
    return angles, flipped_angles

# get the angles from their results (from the ForList.csv file, which are from them running their original wdd code)
def get_angles_from_results(results_file_path):
    angles = []
    for directory in os.listdir('GTRuns'):
        # for each directory, loop through the subdirectories
        for subdirectory in os.listdir(os.path.join('GTRuns', directory)):
            # for each subdirectory, get the 'ForList.csv' file and get the third column value, first row
            for file in os.listdir(os.path.join('GTRuns', directory, subdirectory)):
                if file == 'ForList.csv':
                    with open(os.path.join('GTRuns', directory, subdirectory, file), 'r') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if i == 0:
                                angle = float(line.split(',')[2])
                                angles.append(angle)
                                continue
    return angles

def getAngleDif(x, y):
    angle = np.arctan2(np.sin(x - y), np.cos(x - y))
    return angle

"""
Search over different bee lengths to find the best one
"""
# ground_truth_angles, gt_flipped_angles = get_ground_truth_angles('GTAverage_w_degrees.csv')
# berlin_angles = get_angles_from_results('GTRuns')
# angle_error = []
# berlin_error = []
# flipped_angle_error = []
# length_error = []
# length_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
#
# for b_length in length_values:
#     angles = []
#     waggle_lengths = []
#     for directory in os.listdir('GTRuns'):
#         # for each directory, loop through the subdirectories
#         for subdirectory in os.listdir(os.path.join('GTRuns', directory)):
#             # for each subdirectory, get the images
#             images = get_png_images(os.path.join('GTRuns', directory, subdirectory))
#             images = np.array(images)
#             # try different bee lengths
#
#             try:
#                 decoder = WaggleDecoder(60, bee_length=b_length)
#                 corrected_angle, waggle_length = decoder.calculate_fourier_angle_from_waggle_run_images(images)
#                 angles.append(corrected_angle)
#                 waggle_lengths.append(waggle_length)
#             except:
#                 # print('error')
#                 angles.append(0)
#                 waggle_lengths.append(0)
#
#     angle_error.append(np.mean(getAngleDif(np.array(angles), np.array(ground_truth_angles))))
#     berlin_error.append(np.mean(getAngleDif(np.array(berlin_angles), np.array(ground_truth_angles))))
#     # flip all the angles by adding pi and compare to the ground truth flipped angles
#     flipped_angles = [angle + np.pi for angle in angles]
#     flipped_angle_error.append(np.mean(getAngleDif(np.array(flipped_angles), np.array(gt_flipped_angles))))
#     length_error.append(np.mean(getAngleDif(np.array(waggle_lengths), np.array(ground_truth_angles))))
#
# # add them all to a pandas dataframe and save it to a csv file
# df = pd.DataFrame({'bee lengths': length_values, 'angle_error': angle_error, 'berlin_error': berlin_error, 'flipped_angle_error': flipped_angle_error, 'length_error': length_error})
# df.to_csv('berlin_data_om.csv', index=False)

# 12 seems to be the right bee length given the above code

"""
check bee lengths of 12
"""
ground_truth_angles, gt_flipped_angles = get_ground_truth_angles('GTAverage_w_degrees.csv')
berlin_angles = get_angles_from_results('GTRuns')
angle_error = []
berlin_error = []
flipped_angle_error = []
length_error = []
b_length = 12
directories = []

angles = []
waggle_lengths = []
for directory in os.listdir('GTRuns'):
    # for each directory, loop through the subdirectories
    for subdirectory in os.listdir(os.path.join('GTRuns', directory)):
        # for each subdirectory, get the images
        images = get_png_images(os.path.join('GTRuns', directory, subdirectory))
        images = np.array(images)
        # try different bee lengths

        try:
            decoder = WaggleDecoder(60, bee_length=b_length)
            corrected_angle, waggle_length = decoder.calculate_fourier_angle_from_waggle_run_images(images)
            angles.append(corrected_angle)
            waggle_lengths.append(waggle_length)
        except:
            # print('error')
            angles.append(0)
            waggle_lengths.append(0)

        directories.append(os.path.join('GTRuns', directory, subdirectory))

# angle_error.append(np.mean(getAngleDif(np.array(angles), np.array(ground_truth_angles))))
# berlin_error.append(np.mean(getAngleDif(np.array(berlin_angles), np.array(ground_truth_angles))))
# flip all the angles by adding pi and compare to the ground truth flipped angles
flipped_angles = [angle + np.pi for angle in angles]
# flipped_angle_error.append(np.mean(getAngleDif(np.array(flipped_angles), np.array(gt_flipped_angles))))
# length_error.append(np.mean(getAngleDif(np.array(waggle_lengths), np.array(ground_truth_angles))))
difs = getAngleDif(np.array(angles), np.array(ground_truth_angles))
flipped_difs = getAngleDif(np.array(flipped_angles), np.array(ground_truth_angles))


# add them all to a pandas dataframe and save it to a csv file
df = pd.DataFrame({'ground_truth':ground_truth_angles, 'om_angles': angles, 'errors': difs, 'flipped_om_angles': flipped_angles, 'flipped_angle_error': flipped_difs})
df.to_csv('berlin_data_om_12.csv', index=False)

"""
try out varying the fps and bee_length and test against the ground truth angle from the ground truth for Berlin's new code
"""
# length_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# images = get_png_images('4')
#
# images = np.array(images)
#
# fps_values = [i for i in range(1, 61)]
# for length in length_values:
#     for fps_v in fps_values:
#         try:
#             decoder = WaggleDecoder(fps=fps_v, bee_length=length)
#             corrected_angle, waggle_length = decoder.calculate_fourier_angle_from_waggle_run_images(images)
#             # print(corrected_angle, waggle_length)
#             if abs(corrected_angle - 3.029633477419171) < 0.001:
#                 print(length, fps_v, corrected_angle, waggle_length)
#         except:
#             pass

# output:
# 14 34 3.029490181761041 67
# 14 36 3.0297985923274715 60
# 17 21 3.0290071489970476 67
# 17 22 3.0290071489970476 67
# 17 32 3.0290681364322447 65