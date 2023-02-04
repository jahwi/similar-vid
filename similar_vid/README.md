# Similar Vid

Similar-vid is a library for finding similar frames between videos. It is written as a thin wrapper aroung the Decord and OpenCV libraries.
It was inspired by Netflix's "Skip Intro" feature which allows users to skip intro portions of a tv show.

# Table of Contents
+ Dependencies
+ Installation
+ Usage

## Dependencies
Similar-vid depends on the following:
+ pillow
+ numpy
+ decord
+ imagehash
+ opencv-python

Fortunately, there's a Pipfile that contains virtual environment configurations as will be explained below.

## Installation
The most atraightforward way to use the library is via pipenv:
1. Clone the repository
2. cd to the repository and install the dependencies using pipenv
3. activate the directory

```
git clone https://github.com/jahwi/similar-vid.git
cd similar-vid
(optionally install pipenv) pip install pipenv
pipenv install
pipenv shell
```

Alternatively, you can install the dependencies above manually using pip.
```
pip install pillow numpy decord opencv-python imagehash
```

## Usage

### 1. Loading and Matching
The main way to use the library is via the `Similar` class. It compares frames between a reference video and an array of at least one other video.

```python
# import the class
from similar_vid.similar_secs import Similar

if __name__=="__main__":
    # The library uses multiprocessing, so protect the entry point
    
    # load videos
    video_task = Similar(ref=path_to_reference_video, comp_arr=[path_to_other_video_1, path_to_other_video_2, path_to_other_video_3])

    # match videos in comp_arr against reference video
    video_task.match()

    # print matches
    print(video_task.matches)
```

### 2. Saving hashes and match data for future use
The library also provides a `save` function, which is a wrapper around the `json.dumps` method of the `json` library. It allows saving fields of the `Similar` class to a json file for future use. These can then be reloaded as will be discussed in `3. Loading saved hashes into fields`.

```python
# import the class
from similar_vid.similar_secs import Similar, save

if __name__=="__main__":

    # load videos
    video_task = Similar(ref=path_to_reference_video, comp_arr=[path_to_other_video_1, path_to_other_video_2, path_to_other_video_3])

    # save the video's fields for future use
    save(video_task.ref, path_to_output_file.json) # field holds the reference video hash
    save(video_task.comp, path_to_another_output_file.json) # field holds the hashes of the comparision array
```

### 3. Loading saved hashes into fields
After saving fields using the `save` function, the `load` function allows loading saved hashes into fields.

```python
# import the class
from similar_vid.similar_secs import Similar, load

if __name__=="__main__":

    # load videos via hashes
    video_task = Similar() # first, declare an empty instance
    video_task.ref = load(path_to_ref_video_hash.json) # then edit the fields directly
    video_task.comp = load(path_to_comp_videos_hash.json)

    # It can then be matched, as usual
    video_task.match()
    print(video_task.matches)

    # You can also add individual hashfiles to the comp_array
    video_task.comp.append(load(path_to_a_hashed_video.json))
```

### 4. Using Aliases
The library assigns aliases to videos. The reference video has an alias named `ref`, while the videos to be compared against are named `compare_n`, where `n` is the zero-indexed position of the video in the array. The library provides a method `get_by_alias` which allows selecting class objects by their aliases.

```python
# import the class
from similar_vid.similar_secs import Similar

if __name__=="__main__":

    # load videos
    video_task = Similar(ref=path_to_reference_video, comp_arr=[path_to_other_video_1, path_to_other_video_2, path_to_other_video_3])

    reference_by_alias = video_task.get_by_alias("ref") # selects the reference video object, if it exists.

    # The above is equivalent to:
    reference_directly = video_task.ref
```