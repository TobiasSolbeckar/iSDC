import cv2 # computer vision library
import helpers # helper functions

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # for loading in images

"""
1. Loading and visualizing the data. 
The first step in any classification task is to be familiar with your data; you'll need to load in the images of traffic lights and visualize them!

2. Pre-processing. 
The input images and output labels need to be standardized. 
This way, you can analyze all the input images using the same classification pipeline, and you know what output to expect when you eventually classify a new image.

3. Feature extraction. 
Next, you'll extract some features from each image that will help distinguish and eventually classify these images.

4. Classification and visualizing error. 
Finally, you'll write one function that uses your features to classify any traffic light image. 
This function will take in an image and output a label. You'll also be given code to determine the accuracy of your classification model.

5. Evaluate your model. 
To pass this project, your classifier must be >90% accurate and never classify any red lights as green;  it's likely that you'll need to improve the accuracy of your classifier by changing existing features or adding new features. 
I'd also encourage you to try to get as close to 100% accuracy as possible!
"""

def standardize_input(image):
## This function should take in an RGB image and return a new, standardized version    
    standard_im = np.copy(image)
    standard_im = cv2.resize(standard_im,(32,32))
    
    return standard_im

def one_hot_encode(label):
## Given a label - "red", "green", or "yellow" - return a one-hot encoded label
    if label == 'red':
    	one_hot_encoded = [1,0,0]
    elif label == 'yellow':
    	one_hot_encoded = [0,1,0]
    elif label == 'green':
    	one_hot_encoded = [0,0,1]
    else:
    	raise ValueError('Incorrect label! Label must be "red", "yellow" or "green", but got "' + str(label) + '"')
    return one_hot_encoded

def standardize(image_list):
    
    # Empty image data array
    standard_list = []

    # Iterate through all the image-label pairs
    for item in image_list:
        image = item[0]
        label = item[1]

        # Standardize the image
        standardized_im = standardize_input(image)

        # One-hot encode the label
        one_hot_label = one_hot_encode(label)    

        # Append the image, and it's one hot encoded label to the full, processed list of image data 
        standard_list.append((standardized_im, one_hot_label))
        
    return standard_list

def create_indicator_values(data,threshold):
# Sum up all values in a row that are higher than a certain threshold, in a given data grid.
    row_sums = []
    for i in range(len(data)):
        row = []
        for j in range(len(data[i])):
            cell = data[i][j]
            value = 0
            if cell > threshold:
                # If pixel contains high amount of Hue add the number 1 'mask'
                value = 1
            row.append(value)
        row_sums.append(np.sum(row))
    return row_sums

def translate_detector(array,weighted=True):
    output = [0,0,0]
    out_val = 1
    # Division-by-0 protection
    if (np.sum(array) != 0):
        certainty = np.max(array)/np.sum(array)
    else:
        return [output, array, 0]
    # If the indicator is certain, boost the output value
    if (weighted == True) and (certainty > 0.7):
        out_val = 2
    for i in range(len(array)):
        if array[i] == np.max(array):
            output[i] = out_val
    return [output, array, certainty]

def create_feature(rgb_image,white_th):
	# DEFINE MAPPING PARAMETERS
	#white_th = 180 			# Default: 190. Threshold for detecting white background in images. 
	row_th   = 10			# Default: 6. 	Threshold used for finding first/last row of data in image. this is the number of cells in a row that need to be in the image.
	h_thres  = 165 			# Default: 150. Hue-threshold for including pictures
	s_thres  = 70			# Default: 70.  Sat-threshold for including pictures
	v_thres  = 210 			# Default: 170. V-threshold for including pictures
	
	# Mask out the white background
	mask = cv2.inRange(rgb_image,np.array([white_th,white_th,white_th]),np.array([255,255,255]))
	masked_im = np.copy(rgb_image)
	masked_im[mask != 0] = [0,0,0]

	# Find the first row of data which actually says something.
	first_row = 0
	for i in range(len(mask)):
		tmp = np.sum(mask[i])
		if tmp < (32-row_th)*255:
			first_row = i
			break
	last_row = 32
	for i in range(len(mask)):
		tmp = np.sum(mask[31-i])
		if tmp < (32-row_th)*255:
			last_row = 31-i
			break

	hsv_image = cv2.cvtColor(masked_im, cv2.COLOR_RGB2HSV)
	h = hsv_image[:,:,0]
	s = hsv_image[:,:,1]
	v = hsv_image[:,:,2]
	# Create edges to use for extra-masking
	delta = np.floor((last_row-first_row)/3)
	delta = int(delta)
	#print('Image number: ' + str(image_num))
	#print('First row: ' + str(first_row))
	#print('Delta:     ' + str(delta))	
	r1 = first_row
	r2 = r1 + delta
	y1 = r2 + 1
	y2 = y1 + delta
	g1 = y2 + 1
	g2 = g1 + delta

	# Hue-detector
	row_sums = create_indicator_values(h,h_thres)
	# Translate raw data to detector
	#[hue_det, hue_det_raw,hue_c] = translate_detector([np.sum(row_sums[r1:r2]),np.sum(row_sums[y1:y2]),np.sum(row_sums[g1:g2])])
	hue_det = [np.sum(row_sums[r1:r2]),np.sum(row_sums[y1:y2]),np.sum(row_sums[g1:g2])]
	"""
	print('Hue-det-raw:  ' + str(hue_det_raw))
	print('Hue-detector: ' + str(hue_det))
	"""

	# Sat-detector
	row_sums = create_indicator_values(s,s_thres)
	# Translate raw data to detector
	#[sat_det, sat_det_raw,sat_c] = translate_detector([np.sum(row_sums[r1:r2]),np.sum(row_sums[y1:y2]),np.sum(row_sums[g1:g2])])
	sat_det = [np.sum(row_sums[r1:r2]),np.sum(row_sums[y1:y2]),np.sum(row_sums[g1:g2])]
	"""
	print('Sat-det-raw:  ' + str(sat_det_raw))
	print('Sat-detector: ' + str(sat_det))
	"""
		# V-detector
	row_sums = create_indicator_values(v,v_thres)
	# Translate raw data to detector
	#[v_det, v_det_raw,v_c] = translate_detector([np.sum(row_sums[r1:r2]),np.sum(row_sums[y1:y2]),np.sum(row_sums[g1:g2])])
	v_det = [np.sum(row_sums[r1:r2]),np.sum(row_sums[y1:y2]),np.sum(row_sums[g1:g2])]
	"""
	print('V-det-raw:    ' + str(v_det_raw))
	print('V-detector:   ' + str(v_det))
	"""
	#feature = [[hue_det,hue_det_raw,hue_c],[sat_det,sat_det_raw,sat_c],[v_det,v_det_raw,v_c]]
	#feature = [hue_det, sat_det, v_det,hue_det_raw,sat_det_raw,v_det_raw]
	feature = [hue_det, sat_det, v_det]
	return feature

def estimate_label(rgb_image):
	white_th = 190
	mask = cv2.inRange(rgb_image,np.array([white_th,white_th,white_th]),np.array([255,255,255]))
	masked_im = np.copy(rgb_image)
	masked_im[mask != 0] = [0,0,0]
	#plt.imshow(mask)
	#plt.show()
	#plt.imshow(masked_im)
	#plt.show()
    # Create features
	feature_list = create_feature(rgb_image,white_th)
	total_det = []
	total_raw = []
	manually_updated = 0
	use_det = [0,0,1]
	for i in range(3):
		value = 0
		if use_det[0] == 1:
			value += feature_list[0][i]
		if use_det[1] == 1:
			value += feature_list[1][i]
		if use_det[2] == 1:		
			value += feature_list[2][i]
		total_det.append(value)

	#print('H-det: ' + str(feature_list[0]))
	#print('S-det: ' + str(feature_list[1]))
	#print('V-det: ' + str(feature_list[2]))
	#print('Total: ' + str(total_det))
		#total_raw.append(feature_list[0][1][i] + feature_list[1][1][i] + feature_list[2][1][i])
	""""
	# Special handling for the case when estimator thinks it's a green light
	if total_det[2] == np.max(total_det):
		# Double check with red/green detector
		if np.sum(masked_im[:,:,1]) < np.sum(masked_im[:,:,0]):
			# Red/green disagrees --> set estimate to red
			total_det = [1,0,0]
			manually_updated = 1
			print('R/G: changing maually')
		if (feature_list[1][0][0] == 1) or (feature_list[2][0][0] == 1):
			# This means that either s or v detector is set to 'red' --> set estimate to red
			print('S/V: changing maually')
			print('S: ' + str(feature_list[1][0][0]))
			print('V: ' + str(feature_list[2][0][0]))
			total_det = [1,0,0]
			manually_updated = 1
	"""

	traffic_light_classifier = translate_detector(total_det,weighted=False)
	# If the classifier was manually updated, the certainty should be set to 0
	if manually_updated == 1:
		traffic_light_classifier[2] = 0
	#return [traffic_light_classifier, traffic_light_classifier_raw]
	return [traffic_light_classifier, feature_list]
##################################################################################################################################
##################################################################################################################################

# Setup global variables
global debug
debug = False
global output_log
output_log = str('')

# Image data directories
IMAGE_DIR_TRAINING = "traffic_light_images/training/"
IMAGE_DIR_TEST = "traffic_light_images/test/"

# Using the load_dataset function in helpers.py
# Load training data
IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TRAINING)

# Standardize all training images
STANDARDIZED_LIST = standardize(IMAGE_LIST)

image_num = 0
for image_num in range(9):
	test_im = STANDARDIZED_LIST[image_num][0]
	test_label = STANDARDIZED_LIST[image_num][1]
	# Compose final feature/detector
	classifier_label = estimate_label(test_im)
	print('True label:      ' + str(test_label))
	print('Predicted label: ' + str(classifier_label[0][0]))