import logging
import cv2
from collections import deque
import numpy as np
from sklearn.utils.linear_assignment_ import linear_assignment

#from utils.custom_utils import load_label_map
import src.helpers
from src.bbox_util import box_iou_ratio, draw_box_label
from src.tracker import ObjectTracker
from src.detector import ObjectDetector

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARN)

class DetectAndTrack:
    """
    Class that connects detection and tracking
    """
    def __init__(self, 
                 frame_count = 0,
                 max_age = 2,
                 min_hits = 1,
                 min_conf=0.3, front=True, left=False):
        # Initialize constants
        self.frame_count = frame_count                # frame counter
        self.max_age = max_age                    # no.of consecutive unmatched detection before  a track is deleted
        self.min_hits = min_hits                   # no. of consecutive matches needed to establish a track
        #self.min_conf = min_conf
        self.tracker_list = []
        self.left = left
        self.front = front
        #self.tracker_list: List[BaseTracker] = []
        #self.track_id_list = deque(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'])
        self.track_id_list = deque(list(map(str, range(100))))      # list for track ID

        # Set up 'Object Detector'
        self.detector = ObjectDetector(core_labels=True, min_conf=min_conf, info=True)
        #self.tracker = tracker

    # Method: Used to match detections to trackers
    @staticmethod
    def match_detections_to_trackers1(trackers, detections, min_iou=0.25):
    
        # Initialize 'iou_matrix'
        iou_matrix = np.zeros((len(trackers), len(detections)), dtype=np.float32)

        # Populate 'iou_matrix'
        for t, tracker in enumerate(trackers):
            for d, detection in enumerate(detections):
                #iou_matrix[t, d] = box_iou_ratio(tracker, detection)
                iou_matrix[t,d] = src.helpers.box_iou2(tracker,detection)

        # Produce matches by using the Hungarian algorithm to maximize the sum of IOU
        matched_index = linear_assignment(-iou_matrix)

        # Populate 'unmatched_trackers'
        unmatched_trackers = []
        for t in np.arange(len(trackers)):
            if t not in matched_index[:, 0]:
                unmatched_trackers.append(t)

        # Populate 'unmatched_detections'
        unmatched_detections = []
        for d in np.arange(len(detections)):
            if d not in matched_index[:, 1]:
                unmatched_detections.append(d)

        # Populate 'matches'
        matches = []
        for m in matched_index:
            # Create tracker if IOU is greater than 'min_iou'
            if iou_matrix[m[0], m[1]] > min_iou:
                matches.append(m.reshape(1, 2))
            else:
                unmatched_trackers.append(m[0])
                unmatched_detections.append(m[1])

        if matches:
            # Concatenate arrays on the same axis
            matches = np.concatenate(matches, axis=0)
        else:
            matches = np.empty((0, 2), dtype=int)

        # Return matches, unmatched detection and unmatched trackers
        return matches, np.array(unmatched_detections), np.array(unmatched_trackers)
    
    @staticmethod
    def match_detections_to_trackers(trackers, detections, min_iou=0.25):

    
        IOU_mat= np.zeros((len(trackers),len(detections)),dtype=np.float32)
        for t,trk in enumerate(trackers):
            #trk = convert_to_cv2bbox(trk) 
            for d,det in enumerate(detections):
                #   det = convert_to_cv2bbox(det)
                IOU_mat[t,d] = src.helpers.box_iou2(trk,det) 
        

        # Produces matches       
        # Solve the maximizing the sum of IOU assignment problem using the
        # Hungarian algorithm (also known as Munkres algorithm)

        matched_idx = linear_assignment(-IOU_mat)        

        unmatched_trackers, unmatched_detections = [], []
        for t,trk in enumerate(trackers):
            if(t not in matched_idx[:,0]):
                unmatched_trackers.append(t)

        for d, det in enumerate(detections):
            if(d not in matched_idx[:,1]):
                unmatched_detections.append(d)

        matches = []

        # For creating trackers we consider any detection with an 
        # overlap less than min_iou to signifiy the existence of 
        # an untracked object

        for m in matched_idx:
            if(IOU_mat[m[0],m[1]]<min_iou):
                unmatched_trackers.append(m[0])
                unmatched_detections.append(m[1])
            else:
                matches.append(m.reshape(1,2))

        if(len(matches)==0):
            matches = np.empty((0,2),dtype=int)
        else:
            matches = np.concatenate(matches,axis=0)

        return matches, np.array(unmatched_detections), np.array(unmatched_trackers)


    # Method: Used as a 'pipeline' function for detection and tracking
    def pipeline(self, image):
        dims = (image.shape[1], image.shape[0])
        #dims = image.shape[:2]
        self.frame_count += 1

        # Get bounding boxes for located vehicles
        det_boxes, det_class_name, det_score = self.detector.get_bounding_box_locations(image)

        # Get list of tracker bounding boxes
        trk_boxes = []
        #if self.tracker_list:
        if len(self.tracker_list) > 0:
            for tracker in self.tracker_list:
                trk_boxes.append(tracker.box)

        # Match detected vehicles to trackers
        matched, unmatched_dets, unmatched_trks = self.match_detections_to_trackers(trk_boxes, det_boxes, min_iou=0.3)

        # Deal with matched detections
        if matched.size > 0:
            for trk_idx, det_idx in matched:
                z = det_boxes[det_idx]
                z = np.expand_dims(z, axis=0).T
                temp_trk = self.tracker_list[trk_idx]
                temp_trk.kalman_filter(z)
                xx = temp_trk.x_state.T[0].tolist()
                xx = [xx[0], xx[2], xx[4], xx[6]]
                trk_boxes[trk_idx] = xx
                temp_trk.box = xx
                temp_trk.num_hits += 1

        # Deal with unmatched detections
        if len(unmatched_dets) > 0:
            for i in unmatched_dets:
                z = det_boxes[i]
                z = np.expand_dims(z, axis=0).T
                temp_trk = ObjectTracker()  # Create a new tracker
                x = np.array([[z[0], 0, z[1], 0, z[2], 0, z[3], 0]]).T
                temp_trk.x_state = x
                temp_trk.predict_only()
                xx = temp_trk.x_state
                xx = xx.T[0].tolist()
                xx = [xx[0], xx[2], xx[4], xx[6]]
                temp_trk.box = xx
                temp_trk.id = self.track_id_list.popleft()  # assign an ID for the tracker
                # assign label to tracked image
                temp_trk.label = det_class_name[i]
                temp_trk.score = det_score[i]
                self.tracker_list.append(temp_trk)
                trk_boxes.append(xx)

        # Deal with unmatched tracks
        if len(unmatched_trks) > 0:
            for i in unmatched_trks:
                temp_trk = self.tracker_list[i]
                temp_trk.num_unmatched += 1
                temp_trk.predict_only()
                xx = temp_trk.x_state
                xx = xx.T[0].tolist()
                xx = [xx[0], xx[2], xx[4], xx[6]]
                temp_trk.box = xx
                trk_boxes[i] = xx

        # Populate the list of trackers to be displayed on the image
        good_tracker_list = []
        #warning_count = 0
        #area_count = 0

        for tracker in self.tracker_list:
            if ((tracker.num_hits >= self.min_hits) and (tracker.num_unmatched <= self.max_age)):
                good_tracker_list.append(tracker)
                tracker_bb = tracker.box

                # Draw bounding box on the image
                #image = draw_box_label(image, tracker_bb)
                image = src.helpers.draw_box_label(id=tracker.id, img=image, bbox_cv2=tracker_bb,
                class_name=tracker.label, object_score=tracker.score) 

                #self.frame_count +=1
                """
                if self.front:
                    center = (int(np.average([tracker_bb[0], tracker_bb[2]])),
                              int(np.average([tracker_bb[1], tracker_bb[3]])))

                    if self.left:
                        if center[1] <= dims[1] // 2:
                            cv2.putText(image, 'WARNING', (20, 50), cv2.FONT_HERSHEY_DUPLEX, 2.0, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                            warning_count += 1
                    else:
                        if center[1] >= dims[1] // 2:
                            cv2.putText(image, 'WARNING', (dims[1]-300, 50), cv2.FONT_HERSHEY_DUPLEX, 2.0, (0, 0, 255), 2,
                                        cv2.LINE_AA)
                            warning_count += 1
                else:
                    h = tracker_bb[2] - tracker_bb[0]
                    w = tracker_bb[3] - tracker_bb[1]
                    bb_area = h * w
                    bb_area_percent = 100 * (bb_area/(dims[0]*dims[1]))

                    if bb_area_percent >= 2:
                        cv2.putText(image, 'WARNING', (int(dims[1]/2)-120, 50), cv2.FONT_HERSHEY_DUPLEX, 2.0,
                                    (0, 0, 255), 2, cv2.LINE_AA)
                        area_count += 1
                """

        # Find list of trackers to be deleted
        deleted_trackers = filter(lambda x: x.num_unmatched > self.max_age, self.tracker_list)

        for tracker in deleted_trackers:
            self.track_id_list.append(tracker.id)

        # Update list of active trackers
        self.tracker_list = [x for x in self.tracker_list if x.num_unmatched <= self.max_age]
        cv2.imshow("frame",image)
        """
        # True if vehicle was detected in a 'danger zone'
        if self.front:
            self.warning = True if warning_count > 0 else False
        else:
            self.warning = True if area_count > 0 else False
        """

        return image
