# Simple predictor (for returning last position)
class LastPosPredictor(object):
    """
        Predictor returns same position of object
        Updates from detector
    """

    def __init__(self, max_frames_count_no_detections=1):
        self._bounding_box = None
        self._last_frame_update = 0
        self._last_frame_predict = 0
        self._max_frames_count_no_detections = max_frames_count_no_detections

    def bounding_box(self):
        return self._bounding_box

    def update(self, frame_id, bounding_box):
        if self._last_frame_predict > 0 and (self._last_frame_predict - frame_id) > self._max_frames_count_no_detections:
            return False

        self._bounding_box = bounding_box

        self._last_frame_update = frame_id

        return True

    def predict(self, frame_id):
        self._last_frame_predict = frame_id

        if not self.valid():
            return None

        return self._bounding_box

    def valid(self):
        return abs(self._last_frame_predict - self._last_frame_update) < self._max_frames_count_no_detections
