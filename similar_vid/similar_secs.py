import loaders
import matcher
import json


class Similar():

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
            
    
    def match(self, threshold = 1, format="seconds"):
        # Match the reference video against a list of other videos
        # the threshold is the number of seconds below which matches would not be considered
        # e.g. if threshold is 5, matched frames shorter than 5 seconds in length would not be counted.
        if not self.ref or not self.comp:
            print("Missing match parameters.")
        self._raw_matches = matcher.match_(self.ref, self.comp)
        self.matches = []
        for match_ in self._raw_matches:
            for matched, frames in match_.items():
                self.matches.append({"name" : matched, "matches" : matcher.consecutive_clusters(frames, threshold, format)})
    
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

        



file1 = r"videos\inside_job\01_trimmed.mkv"
file2 = r"videos\inside_job\03_trimmed.mkv"
file6 = r"videos\inside_job\rad.mp4"
file3 = r"videos\inside_job\03.mkv"
file4 = r"videos\inside_job\04.mkv"
file5 = r"videos\inside_job\05.mkv"

# file1 = "videos/inside_job/01.mkv"
# file2 = "videos/inside_job/02.mkv"
# file3 = "videos/inside_job/03.mkv"
# file4 = "videos/inside_job/04.mkv"
# file5 = "videos/inside_job/05.mkv"

if __name__ == "__main__":
    inside_job = Similar(ref=file1, comp_arr=[file2])
    # outside_job = Similar()
    # outside_job.ref = load(r"outs\ij_ref.json")
    # outside_job.comp.append(load(r"outs\ij_ref_02.json"))
    # print(type(outside_job.ref))
    # outside_job.match(threshold=10)
    # print(outside_job.matches)
    # print(inside_job.aliases)
    inside_job.match(threshold=17, format="frames")
    print(inside_job.matches)
    # print(inside_job.get_by_alias(r"ref - compare_0"))

    # jss = json.load(r"outs\ij_ref.json")
    # with open(r"outs\ij_ref.json") as file:
    #     jss = json.load(file)
    #     print(jss["location"])
    # save(inside_job.get_by_alias("compare_0"), r"outs\ij_ref_02.json")
    # print(inside_job.ref)
    # print(inside_job._raw_matches)
    # print(inside_job.matches)
    # print(type(inside_job))

    # print(inside_job.comp[0]["location"])