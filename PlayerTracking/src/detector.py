import logging
import os
import numpy as np
import tensorflow as tf

from utils.custom_utils import load_label_map

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARN)

class ObjectDetector:
    # Method: Constructor
    def __init__(self, core_labels=True, min_conf=0.3, info=False):
        """
        :param core_labels: If True, use the Offense/Defense label model
        :param min_conf: Minimum acceptable confidence level
        :param info: If True, display all visualisations
        """
        self.bounding_boxes = []
        self.min_conf = min_conf
        self.info = info
        self.core_labels = core_labels
        
        self.object_class = []
        self.object_scores = []
        #self.classes_to_detect = list(range(1, 15))
        self.classes_to_detect = []

        # Change to current working directory
        os.chdir(os.getcwd())

        if self.core_labels:
            PATH_TO_MODEL = '../models/frozen_inference_graph.pb'
            PATH_TO_LABEL_MAP = '../models/core_labelmap.pbtxt'
            NUM_CLASSES = 11
        else:
            PATH_TO_MODEL = 'models/frozen_model.pb'
            PATH_TO_LABEL_MAP = 'models/Off_Def_labelmap.pbtxt'
            NUM_CLASSES = 7

        # Tensorflow Setup
        self.detection_graph = tf.Graph()       # Define TensorFlow graph
        config = tf.ConfigProto()               
        config.gpu_options.allow_growth = True  # configuration for possible GPU use

        # load frozen tensorflow detection model and initialize the tensorflow graph
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
               serialized_graph = fid.read()
               od_graph_def.ParseFromString(serialized_graph)
               tf.import_graph_def(od_graph_def, name='')
            
            # Setup session and image tensor
            self.session = tf.Session(graph=self.detection_graph, config=config)
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected
            self.boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')   

            # Each score represents the classification confidence for each of the objects
            self.scores =self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_detections =self.detection_graph.get_tensor_by_name('num_detections:0')

        # Load label map and convert into categories
        # Assign an index to each category
        self.category_index = load_label_map(PATH_TO_LABEL_MAP, NUM_CLASSES)

    # Helper function to convert image into numpy array    
    @staticmethod
    def load_image_into_numpy_array(image):
         (im_width, im_height) = image.size

         return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)       
    
    # Helper function to convert normalized box coordinates to pixels
    @staticmethod
    def box_normal_to_pixel(box, dims):
        """
        :param box: Box with normalized coordinates
        :param dims: Image dimensions
        :return: Box with pixel coordinates
        """
        height, width = dims[0], dims[1]
        box_pixel = [int(box[0]*height), int(box[1]*width), int(box[2]*height), int(box[3]*width)]

        return np.array(box_pixel)    
    
    #def get_detections(self, image, debug=False) -> List[UnitObject]:
    # Method: Used to detect the locations of the objects in the image
    def get_bounding_box_locations(self, image):
        """
        :param image: Image
        :return: Bounding box locations surrounding detected objects
        """   
        with self.detection_graph.as_default():
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_expanded = np.expand_dims(image, axis=0)

            # Actual detection
            (boxes, scores, classes, num_detections) = self.session.run(
                [self.boxes, self.scores, self.classes, self.num_detections],
                feed_dict={self.image_tensor: image_expanded})

            # Remove 1D entries from the shape of the array
            boxes = np.squeeze(boxes)
            classes = np.squeeze(classes)
            #classes = np.squeeze(classes).astype(int).tolist()
            scores = np.squeeze(scores)

            
            # Convert to a list
            classes_list = classes.tolist()

            # Find cars detected in the image
            if self.core_labels:
                index_vector = [i for i, id in enumerate(classes_list) if (scores[i] > self.min_conf)]
            else:
                index_vector = [i for i, id in enumerate(classes_list) if ((id == 3) and (scores[i] > self.min_conf))]

            if len(index_vector) > 0:
                temp_boxes = []
                tmp_classes = []
                tmp_scores = []

                for index in index_vector:
                    # Get image dimensions
                    dims = image.shape[0:2]

                    # Convert normalized coordinates to pixel coordinates
                    box = self.box_normal_to_pixel(boxes[index], dims)

                    # Calculate height, width and ratio to filter out boxes that not the right shape or size
                    box_h = box[2] - box[0]
                    box_w = box[3] - box[1]
                    #ratio = box_h / box_w
                    ratio = box_h/(box_w + 0.01)

                    # Filter out boxes that are not the right shape or size
                    if ratio < 0.8 and box_h > 20 and box_w > 20:
                        temp_boxes.append(box)
                        tmp_classes.append(self.category_index[classes_list[index]]['name'])
                        tmp_scores.append(scores[index]*100.0)

                        if self.info:
                            print("[INFO]: Object {} Detected at {} with {:.2f}% confidence".format(self.category_index[classes_list[index]]['name'], box, scores[index]*100.0))

                self.bounding_boxes = temp_boxes
                self.object_class = tmp_classes
                self.object_scores = tmp_scores
            
            else: print('no detection!')
        
        return self.bounding_boxes, self.object_class, self.object_scores