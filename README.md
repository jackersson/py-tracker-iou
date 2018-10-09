# Python implementation of IOU tracker

Installation:

    pip3 install git+https://github.com/dataiCV/pytracker_iou.git

Simple usage

    from py_tracker_iou import IouObjectTracker
    tracker = IouObjectTracker(iou_threshold=0.6, max_frames_count_no_detections=15)
    actives, non_actives = tracker.process(None, offset, objects)





