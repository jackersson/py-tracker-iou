import logging
import traceback

import numpy as np

from .utils import intersection_over_union
from .tracked_object import TrackedObject
from .last_pos_predictor import LastPosPredictor
from .object_info import ObjectInfo


class IouObjectTracker(object):

    def __init__(self, iou_threshold=0.5, max_frames_count_no_detections=15):
        """
            Create iou object tracker

            :param iou_threshold: bounding boxes IOU threshold when objects considered the same
            :type iou_threshold: float [0, 1.0]

            :param max_frames_count_no_detections: indicates number of frames to keep object alive if no detections exists for this object
            :type max_frames_count_no_detections: int
        """

        self._iou_treshold = iou_threshold
        self._max_frames_count_no_detections = max_frames_count_no_detections

        self._counter = 0
        self._tracks = {}
        self._previous_frame_id = -1

    def _up_to_date(self, tracked_object, frame_id):
        """
            Check that tracked_object was updated in frame with frame_id.

            :param tracked_object:
            :type tracked_object: TrackedObject

            :param frame_id: incremental frame offset [0, maxint)
            :type frame_id: int

            :rtype: bool
        """
        # TODO think about better fix
        return frame_id == tracked_object.last_frame_update()

    def process(self, frame, frame_id, detections=[]):
        """
            Assigns track_id to each detection.
            Returns objects that are alive as tracks, and objects that disappeared in current frame

            :param frame:
            :type frame: np.ndarray [h, w, c] (RGB colorspace)

            :param frame_id: incremental frame offset [0, maxint)
            :type frame_id: int

            :param detections:
            :type detections: list of ObjectInfo

            :rtype: list of ObjectInfo (objects that are active in current frame)
            :rtype: list of int (ids of tracks to be removed)
        """

        actives = []
        if self._previous_frame_id < frame_id:
            actives = self._update(frame, frame_id, detections)
            self._previous_frame_id = frame_id
        else:
            raise ValueError("Failed. Previous frame id ({}) > Next({})".format(self._previous_frame_id,
                                                                                frame_id))

        objects_to_remove = []
        for key, tracked_object in self._tracks.items():

            # check if we already updated track in detections
            # so there is no need to update this track twice
            if self._up_to_date(tracked_object, frame_id):
                continue

            ret, position = tracked_object.new_position(frame_id)
            if ret:
                object_info = ObjectInfo(bounding_box=position,
                                         confidence=tracked_object.confidence(),
                                         class_name=tracked_object.class_name(),
                                         track_id=tracked_object.track_id())
                actives.append(object_info)
            else:
                # assume that tracked object isn't valid for current frame
                objects_to_remove.append(key)

        for idx in objects_to_remove:
            tracked_object = self._tracks.pop(idx, None)

        return actives, objects_to_remove

    def _update(self, frame, frame_id, detections):
        """
            Updates tracks with detections for current frame (frame_id)
            Set "track_id" field in object info

            :param frame:
            :type frame: np.ndarray [h, w, c] (RGB colorspace)

            :param frame_id: incremental frame offset [0, maxint)
            :type frame_id: int

            :param detections:
            :type detections: list of ObjectInfo

            :rtype: list of ObjectInfo
        """
        if not detections:
            return []

        # n = len(detections)

        ious = np.zeros(len(detections))
        used = set()  # prevent from using same detections in tracker update
        actives = []
        for track_id in self._tracks:

            tracked_box = self._tracks[track_id].bounding_box()
            assert tracked_box is not None

            for i, object_info in enumerate(detections):
                if i in used:
                    continue

                assert isinstance(object_info, ObjectInfo), "Invalid detection object type %s" % (
                    type(object_info))

                detected_box = object_info.bounding_box
                assert detected_box is not None

                ious[i] = intersection_over_union(detected_box, tracked_box)

            # Find best match for detected-tracked object
            sorted_indices = np.argsort(ious)[::-1]
            best_index = sorted_indices[0]
            if ious[best_index] > self._iou_treshold:
                object_info = detections[best_index]

                assert track_id == self._tracks[track_id].track_id()
                object_info.track_id = track_id

                self._tracks[track_id].update_from_detection(frame_id,
                                                             object_info.bounding_box,
                                                             class_name=object_info.class_name,
                                                             confidence=object_info.confidence)
                used.add(best_index)  # prevent from duplicating same object
                actives.append(object_info)
            ious.fill(0)  # reset calculated IOUS

        # create new tracked objects from detections
        # for those whose haven't been in tracked objects yet
        for i, object_info in enumerate(detections):
            if i in used:
                continue
            new_id = self._next_id()
            assert new_id not in self._tracks
            object_info.track_id = new_id

            self._tracks[new_id] = self._create_tracked_object(track_id=new_id)
            self._tracks[new_id].update_from_detection(frame_id,
                                                       bounding_box=object_info.bounding_box,
                                                       class_name=object_info.class_name,
                                                       confidence=object_info.confidence)
            actives.append(object_info)
        return actives

    # TODO this could be overriden by other implementations
    def _next_id(self):
        """
            Returns unique track id

            :rtype: int
        """
        self._counter += 1
        return self._counter

    def _create_tracked_object(self, track_id):
        """
            Creates track_id in

            :rtype: TrackedObject
        """
        predictor = LastPosPredictor(
            max_frames_count_no_detections=self._max_frames_count_no_detections)
        return TrackedObject(predictor, track_id)

    def __del__(self):
        self._tracks.clear()
