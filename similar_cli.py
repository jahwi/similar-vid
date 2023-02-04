from similar_vid.similar_secs import Similar, load
import argparse
import os

# CLI interface for similar_vid
if __name__=="__main__":
    parser = argparse.ArgumentParser("Similar-Vid CLI")
    parser.add_argument("ref", type=str, default="", help='Reference video or video hash.')
    parser.add_argument('comp', type=str, default="", help="List of video files or video hash files to compare against.")
    parser.add_argument('--threshold', type=int, default=1, help='Time in seconds below which matches will not be considered.')
    parser.add_argument('--format', type=str, default="seconds", help='Format of matches, either frames or seconds.')

    args = parser.parse_args()

    # print(args.comp.split())
    # exit()
    video_task = None

    # check that videos are supplied
    if not args.ref or not args.comp:
        print("Invalid input.")
        exit()
    
    # check if files exist
    ref = args.ref
    comp_list = args.comp.split()
    files = [ref]
    files.extend(comp_list)
    for file in files:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"Cannot find file {file}.")

    # check correct format
    if not args.format in ["seconds", "frames"]:
        raise TypeError(f"Invalid format: `{args.frame}`")
    
    # if inputs are hashfiles
    if os.path.splitext(ref)[1] == ".json":
        video_task = Similar()
        video_task.ref = load(args.ref)

        for hashed in comp_list:
            if not os.path.splitext(hashed)[1] == ".json":
                raise TypeError("Hashfiles must have a json extension.")
            
            # if list, extend list, if dictionary, append.
            loaded = load(hashed)
            typ = str(type(loaded))
            if typ == "<class 'list'>":
                video_task.comp.extend(loaded)
            elif typ == "<class 'dict'>":
                video_task.comp.append(loaded)
    else:
        # If inputs are videos
        video_task = Similar(ref=ref, comp_arr=comp_list)

    # match
    video_task.match(threshold=args.threshold, format=args.format)
    for match in video_task.matches:
        print(match)

