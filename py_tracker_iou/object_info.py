class ObjectInfo(object):

    def __init__(self, bounding_box, confidence=0.0, class_id=-1,
                 track_id=0, detection_id=-1):
        self.bounding_box = bounding_box
        self.confidence = confidence
        self.class_id = class_id
        self.track_id = track_id

        # used to assign object to right detection
        self.detection_id = detection_id
