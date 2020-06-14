"""Take requested tank and images and run match with CukeCV."""

import cukecv
from operator import itemgetter

import logging
logger = logging.getLogger('main')


def make(query, subjects):
    """Run an image recognition search with given cuke instances."""
    results = []
    for subject in subjects:
        results.append((
            query.matches(cukecv.ReconstitutedCuke(subject.features)),
            subject,
        ))
    results.sort(key=itemgetter(0), reverse=True)
    return results
