import numpy as np
import os
import sys
import tensorflow as tf
import cv2

from collections import defaultdict
from io import StringIO
from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


def getObject(image):
    '''Args:
        image (raw image): current image of cozmo camera
    Returns:
        array with [score, prozentual positon x1, prozentual positon y1, prozentual positon x2, prozentual positon y2]'''

    raw_rgb = np.array(image)
    edge = cv2.Canny(raw_rgb, 100, 200)
    cv2.imwrite("act_pic.jpg", edge)

    edge_image = cv2.imread('act_pic.jpg')

    NUM_CLASSES = 1

    PATH_TO_LABELS = os.path.join('./object_detection/object-detection.pbtxt')

    # ## Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile("./object_detection/frozen_gpu_graph_9963/frozen_inference_graph.pb", 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # ## Loading label map
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Size, in inches, of the output images.
    IMAGE_SIZE = (12, 8)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # while True:
            image_np = edge_image
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

            # item(1) = Y1
            # itme(0) = X1
            # item(3) = Y2
            # item(2) = X2
            ret = [scores.item(0), boxes.item(1), boxes.item(0),
                   boxes.item(3), boxes.item(2)]
            print(ret)
            return ret

            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)

            cv2.imshow('object detection', cv2.resize(image_np, (800, 600)))

            cv2.waitKey(0)
