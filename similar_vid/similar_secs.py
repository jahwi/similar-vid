from . import loaders
from . import matcher
import json


class Similar():
    # Use:
    # Similar(ref=video, comp_arr=[video2, video3])

    def __init__(self, *args, **kwargs):
        ref = kwargs.get("ref", "")
        comp_arr = kwargs.get("comp_arr", "")

        # check if files exist, can be read, and are videos
        self.ref = None
        self.comp = []
        self.matches = None
        self.aliases = []

        if not ref or not comp_arr:
            return

        check_videos = loaders.load(ref, comp_arr)
        # populate fields
        for hashed_video in check_videos:
            if hashed_video["name"] == "ref":
                self.ref = hashed_video
            else:
                self.comp.append(hashed_video)
            self.aliases.append(hashed_video["name"])

    
    def match(self, threshold = 1, format="seconds"):
        # Match the reference video against a list of other videos
        # the threshold is the number of seconds below which matches would not be considered
        # e.g. if threshold is 5, matched frames shorter than 5 seconds in length would not be counted.
        if not self.ref or not self.comp:
            raise TypeError("Missing match parameters.")
        self._raw_matches = matcher.match_(self.ref, self.comp)
        self.matches = []
        for match_ in self._raw_matches:
            for matched, frames in match_.items():
                match = {"name" : matched, "matches" : matcher.consecutive_clusters(frames, threshold, format)}
                self.matches.append(match)
                self.aliases.append(match["name"])
    
    def get_by_alias(self, obj):

        # search ref field
        if obj == "ref":
            return self.ref
        
        # search comp array
        for video in self.comp:
            if video["name"] == obj:
                return video

        # search match list
        for match_ in self.matches:
            if match_["name"] == obj:
                return match_

        # No match
        return None


def save(source_obj, target):
    # Save a field to a file

    try:
        with open(target, "w") as file:
            file.writelines(json.dumps(source_obj))
    except Exception as e:
        raise e

def load(json_file):
    # reads a json file to a field

    with open(json_file, "r") as file:
        obj = json.load(file)
        return obj