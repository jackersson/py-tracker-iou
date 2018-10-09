class TrackedObject(object):

    UNDEFINED_CLASS_ID = -1

    def __init__(self, predictor, track_id):
        super(TrackedObject, self).__init__()

        self._predictor = predictor

        self._track_id = track_id
        self._class_id = self.UNDEFINED_CLASS_ID
        self._confidence = 0.0

    def update_from_detection(self, frame_id, bounding_box,
                              class_id=UNDEFINED_CLASS_ID,
                              confidence=0.0):
        """
            Update predictor with new position from detection
        """

        self._confidence = self._confidence
        self._class_id = class_id if class_id >= 0 else self._class_id

        ret = self._predictor.update(frame_id, bounding_box)
        if not ret:
            return False

        self._last_frame_update = frame_id
        return True

    def new_position(self, frame_id):
        """
            Predicts new object position for next frame
        """
        position = self._predictor.predict(frame_id)
        return self._predictor.valid(), position

    def track_id(self):
        return self._track_id

    def class_id(self):
        return self._class_id

    def confidence(self):
        return self._confidence

    def bounding_box(self):
        return self._predictor.bounding_box()

    def last_frame_update(self):
        return self._predictor._last_frame_update
