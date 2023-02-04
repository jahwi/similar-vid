import numpy as np
import datetime
from multiprocessing import Pool

def consecutive_clusters(numbers, threshold=1, format="seconds"):
    # Takes in a list of matching frames and returns boundaries around matching frames
    # eliminates stranded matching frames


    def span(arr):
        # returns the "length" of a list of frames
        return abs(arr[0] - arr[-1])
    
    # error check args
    if not numbers:
        return
    allowed_formats = ["seconds", "frames"]
    if not format in allowed_formats:
        print(f"Ignoring format '{format}' and formatting in seconds")
        format="seconds"
    

    numbers = list(set(numbers))
    numbers = sorted(numbers)
    clusters = []

    current_cluster = [numbers[0]]

    for i in range(1, len(numbers)):
        if numbers[i] <= current_cluster[-1] + 23:
            current_cluster.append(numbers[i])
        else:
            if span(current_cluster) / 24 >= threshold:
                clusters.append(current_cluster)
            current_cluster = [numbers[i]]

    if span(current_cluster) / 24 >= threshold:
        clusters.append(current_cluster)
    
    div = 1
    if format == "seconds":
        div = 24
    clusters = [[round(cluster[0]/div, 3), round(cluster[-1]/div, 3)] for cluster in clusters]

    return clusters


def matcher(dicts):
    # finds similarities between arrays of frames

    matches = []
    dict1, dict2 = dicts[0], dicts[1]
    arr1, arr2 = np.asarray(dict1["hash"]), np.asarray(dict2["hash"])


    print(f"Matching {dict1['name']} & {dict2['name']}")
    begin = datetime.datetime.now()
    for i, ref_hash in enumerate(arr1):
        comp_array = abs(arr2 - ref_hash)
        closest_frame = comp_array.argmin()

        closest_frame_hash = arr2[closest_frame]
        diff = comp_array[closest_frame] / 64
        diff = abs(diff * 100)

        if diff <= 9000000000 and diff >= 0:
            matches.append(int(closest_frame))
        else:
            continue

    return {f"{dict1['name']} - {dict2['name']}" : matches}


def match_(refdict, comp_array_of_dicts):
    # match two dictionaries containing hashes

    tasks = [(refdict, comp_vid) for comp_vid in comp_array_of_dicts]
    with Pool() as pool:
        matches = pool.map(matcher, tasks)
    
    return matches

    
    



