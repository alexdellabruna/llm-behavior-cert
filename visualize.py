import os
import json
from matplotlib import pyplot as plt

for d in os.listdir("out/"):
    for f in os.listdir(os.path.join("out/", d)):
        if f.endswith(".json"):
            with open(os.path.join("out/", d, f), "r") as result_file:

                # add online generating visulization support
                res_file_raw=result_file.read()
                if res_file_raw.endswith(","):
                    res_file_raw=res_file_raw[:-1]+"]"

                result_arr = json.loads(res_file_raw)
                plt.plot(range(len(result_arr)), [r["score"] for r in result_arr], label=f.split(".json")[0])
                plt.savefig(os.path.join("out/", d, f.split(".json")[0]+".png"))
                plt.show()
                plt.close()