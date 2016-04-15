import json
import urllib2

import numpy as np

API = 'http://ec2-52-11-11-89.us-west-2.compute.amazonaws.com/challenge16/api.py'

def get_blocked_videos(api=API):
    api_url = '{}?action=get_blocked'.format(api)
    req = urllib2.Request(api_url)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def interpolated_prec_rec(prec, rec):
    """Interpolated AP - THUMOS paradigm.
    """
    ap = 0
    recall_points = np.arange(0, 1.1, 0.1)
    n_points = float(recall_points.size)
    for recall_thr in recall_points:
        idx = rec >= recall_thr
        p = 0
        if idx.any():
            p = prec[idx].max()
        ap += p / n_points
    return ap

def segment_iou(target_segment, candidate_segments):
    """Compute the temporal intersection over union between a
    target segment and all the test segments.

    Parameters
    ----------
    target_segment : 1d array
        Temporal target segment containing [starting, ending] times.
    candidate_segments : 2d array
        Temporal candidate segments containing N x [starting, ending] times.

    Outputs
    -------
    tiou : 1d array
        Temporal intersection over union score of the N's candidate segments.
    """
    tt1 = np.maximum(target_segment[0], candidate_segments[:, 0])
    tt2 = np.minimum(target_segment[1], candidate_segments[:, 1])
    # Intersection including Non-negative overlap score.
    segments_intersection = (tt2 - tt1).clip(0)
    # Segment union.
    segments_union = (candidate_segments[:, 1] - candidate_segments[:, 0]) \
      + (target_segment[1] - target_segment[0]) - segments_intersection
    # Compute overlap as the ratio of the intersection
    # over union of two segments.
    tIoU = segments_intersection.astype(float) / segments_union
    return tIoU
