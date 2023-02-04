import os
from decord import VideoReader, cpu
from PIL import Image
import numpy as np
import imagehash
import cv2
from multiprocessing import Pool, get_context

def load(ref, comp_arr):
    # Checks reference video and comparision array of videos
    # Usage: load(r"reference.mp4", [r"comparision_1.mp4", r"comparision_2.mp4"])
    # Remember to pass as raw strings if on Windows
    tasks = []
    try:
        ref = os.path.normpath(ref)
        with open(ref, "r") as ref_vid:
            tasks.append(("ref", ref))

        for i, file in enumerate(comp_arr):
            file = os.path.normpath(file)
            with open(file, "r") as comp_vid:
                tasks.append((f"compare_{i}", file))
    except Exception as e:
        raise e
    
    # multiprocess hash
    try:
        with get_context("spawn").Pool() as pool:
            hashed_videos = pool.map(hasher, tasks)
            pool.close()
            pool.join()
    except Exception as e:
        print(e)
        exit()
    return hashed_videos
    

def hasher(task):
    # hashes a video into a perceptual hash

    name = task[0]
    video = task[1]
    print(f"Hashing {name} [{video}]")
    vid = VideoReader(video, ctx=cpu(0), width = 20, height= 20)
    length = len(vid)
    arr = []

    assert(length > 0)


    frames = 0
    while frames < length:
        frame = vid.next().asnumpy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = Image.fromarray(frame)
        frame = imagehash.phash(frame)
        arr.append(np.float64(int("0x"+str(frame), 16)))
        frames += 1
    
    print(f"Hashed {name}")

    return {"name": name, "hash" : arr, "location": video, "fps": vid.get_avg_fps()}

