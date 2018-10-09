def intersection_over_union(boxA, boxB, ltrb=False):
    if ltrb:
        return _intersection_over_union(boxA, boxB)
    else:
        xA, yA, wA, hA = boxA
        xB, yB, wB, hB = boxB
        return _intersection_over_union([xA, yA, xA + wA, yA + hA],
                                        [xB, yB, xB + wB, yB + hB])


def _intersection_over_union(boxA, boxB):
    """
        Calculates intersection over union for two bounding boxes:
        Args:
            boxA: ints xmin, ymin, xmax, ymax
            boxB: ints xmin, ymin, xmax, ymax

        Returns:
            IOU : float [0..1]

    """


    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    if (xB < xA) or (yB < yA):
        return 0

    # compute the area of intersection rectangle
    interArea = (xB - xA) * (yB - yA)

    # compute the area of both the prediction and ground-truth rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou
