import os
import json
import scipy.spatial.distance as spd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--comp-out-dir", "-c", help="Compare output directory", default=None)
args, _ = parser.parse_known_args()

if not args.comp_out_dir:
    print("Compare output directory not provided. Please provide it using the --comp-out-dir or -c argument.")
    exit(1)

comp_out_dir = args.comp_out_dir

for d in os.listdir("out/"):
    with open(os.path.join("out/", d, "out.json"), "r") as result_file:
        res_file_raw=result_file.read()

        result_arr = json.loads(res_file_raw)
        result_arr = [r["score"] for r in result_arr]

        with open(os.path.join(comp_out_dir, d, "out.json"), "r") as compare_file:
            compare_file_raw=compare_file.read()
            
            compare_result_arr = json.loads(compare_file_raw)
            compare_result_arr = [r["score"] for r in compare_result_arr]

            js_distance=spd.jensenshannon(result_arr, compare_result_arr)

            print(js_distance)