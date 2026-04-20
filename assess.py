import argparse
import json
import os
import urllib3
import requests
from settings import *
import shutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ModelConnection:

    def ollama(url,model,prompt):
        return requests.post(url=url,json={ "model": model, "prompt": prompt, "stream": False},verify=False)

parser = argparse.ArgumentParser()
parser.add_argument("--ollama-url", "-u", help="OLLAMA server URL", default=None)
args, _ = parser.parse_known_args()

if not args.ollama_url:
    print("OLLAMA URL not provided. Please provide it using the --ollama-url or -u argument.")
    exit(1)

ollama_url = args.ollama_url

shutil.rmtree('./out/', ignore_errors=True)
prompt_folder_path = "./prompts"

prompt_files = [f for f in os.listdir(prompt_folder_path) if os.path.isfile(os.path.join(prompt_folder_path, f))]

for f in prompt_files:
    with open(os.path.join(prompt_folder_path, f), "r") as prompt_file:
        prompt_arr = json.load(prompt_file)
        last_successful_index=0
        p_index = 0
        while p_index < len(prompt_arr):
            p = prompt_arr[p_index]
            try:
                prompt = p["prompt"]

                response = ModelConnection.ollama(ollama_url, MODEL, prompt)
                response_txt=response.json()["response"]

                if response_txt is None or response_txt == "":
                    raise ValueError("empty response")

                os.makedirs("./out", exist_ok=True)
                os.makedirs(f"./out/{f.split('.json')[0]}", exist_ok=True)

                check_prompt="Are these two sentences semantically the same?\nSentence 1:\n"+response_txt+"\nSentence 2:\n"+p["solution"]+"\nAnswer only with yes or no."

                check_response = ModelConnection.ollama(ollama_url, MODEL, check_prompt)
                check_response_txt = check_response.json()["response"]

                if check_response_txt.lower().strip().startswith("yes"):
                    check_response_txt="yes"
                elif check_response_txt.lower().strip().startswith("no"):
                    check_response_txt="no"
                else:
                    raise ValueError("unexpected check response: "+check_response_txt)

                with open(f"./out/{f.split('.json')[0]}/out.json","a") as f_res:
                    if p_index==0:
                        f_res.write("[")
                    if p_index!=len(prompt_arr)-1:
                        f_res.write(json.dumps({"response": response_txt, "check": check_response_txt})+",")
                    else:
                        f_res.write(json.dumps({"response": response_txt, "check": check_response_txt}))
                        f_res.write("]")
                    last_successful_index=p_index
                    p_index+=1

            except Exception as e:
                print("Error during generation ", str(e))
                p_index = last_successful_index