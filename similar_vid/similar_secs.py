from . import loaders
from . import matcher
import json


class Similar():

    ref: dict
    """The reference video field. Contains the hashed reference video."""
    comp: list
    """The Comparision array field. Contains an array of hashed comparision videos."""
    matches: dict
    """Contains the dictionary of matches, if any."""
    aliases: list
    """Contains a list of aliases."""



    def __init__(self, *args, **kwargs):
        """
        Description: Instantiates a `Similar` class object.

        Usage: `Similar(ref=video, comp_arr=[video2, video3])`
        where the videos are paths to video files.

        An empty instance can be created by passing no aguments to the constructor as in `Similar()`
        This is most useful for loading saved hashfiles into fields.

        Returns: a Similar class instance.
        """
        ref = kwargs.get("ref", "")
        comp_arr = kwargs.get("comp_arr", "")

        # check if files exist, can be read, and are videos
        self.ref = None
        self.comp = []
        self.matches = {}
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
        """
        Description: Matches a reference video against a list of other videos.

        Usage: `instance.match(threshold, format)`

        The threshold argument is the number of seconds below which matches would not be considered.
        e.g. if threshold is 5, matched frames shorter than 5 seconds in length would not be counted.

        The format argument specifies the format of the returned match list, its options are 'seconds' or 'frames'.

        Returns: a dictionary of dictionaries.

        Consider the following:
        {
        'compare_0': {'ref': [[3.167, 21.542]]}, 
        'ref': {'compare_0': [[0.458, 23.125]]}
        }
        The above means that seconds 3.167-21.452 of compare 0 match seconds 0.458-23.125 in ref.
        """

        if not self.ref or not self.comp:
            raise TypeError("Missing match parameters.")
        self._raw_matches = matcher.match_(self.ref, self.comp)
        self.matches = {}
        
        for m in self._raw_matches:
            ref = m[0]
            searched = m[1]
            searched_matches = m[2]
            ref_matches = m[3]

            searched_matches = matcher.consecutive_clusters(searched_matches, threshold, format)
            ref_matches = matcher.consecutive_clusters(ref_matches, threshold, format)

            if self.matches.get(searched, None) is not None:
                self.matches[searched].update({ref: searched_matches})
            else:
                self.matches.update({searched: {ref: searched_matches}})

            if self.matches.get(ref, None) is not None:
                self.matches[ref].update({searched: ref_matches})
            else:
                self.matches.update({ref: {searched: ref_matches}})


    def get_by_alias(self, obj):
        """
        Description: Selects an object by its alias. See the `instance.aliases` field to check alaises, if any.

        Usage: `instance.get_by_alias(alias_name)`

        Example: `batman.get_by_alias(ref)`
        The above woiuld select the ref field.
        """

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
    """
    Description: Saves a field to a JSON file.

    Usage: `save(object_or_field, destination)`

    Example: `save(inside_job.matches, "outs//matches.json")`
    """

    try:
        with open(target, "w") as file:
            file.writelines(json.dumps(source_obj))
    except Exception as e:
        raise e

def load(json_file):
    """
    Description: Reads a JSON file into a field.

    Usage: `instance_field = load(path_to_ref_video_hash.json)`

    Example: `inside_job.ref = load("hashes//inside_job_ref.json")`
    """

    with open(json_file, "r") as file:
        obj = json.load(file)
        return obj