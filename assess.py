import argparse
import json
import os
import urllib3
import requests
from settings import *
import shutil
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from deepeval.test_case import LLMTestCase
from deepeval.models import GPTModel

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ModelConnection:

    def vllm(url,model,prompt):
        return requests.post(url=url,json={ "model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": 10000, "stream": False},verify=False)

parser = argparse.ArgumentParser()
parser.add_argument("--model-url", "-u", help="Model server URL", default=None)
parser.add_argument("--judge-url", "-j", help="Judge server URL", default=None)
args, _ = parser.parse_known_args()

if not args.model_url:
    print("Model URL not provided. Please provide it using the --model-url or -u argument.")
    exit(1)

if not args.judge_url:
    print("Judge URL not provided. Please provide it using the --judge-url or -j argument.")
    exit(1)

model_url = args.model_url+"/v1/chat/completions"
judge_url = args.judge_url+"/v1"

judge_model = GPTModel(
    model=JUDGE_MODEL,
    api_key="dummy",
    base_url=judge_url
)

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
            print(f"Processing {f}, prompt {p['prompt']}, prompt index: {p_index+1}/{len(prompt_arr)}")
            try:
                prompt = p["prompt"]

                response = ModelConnection.vllm(model_url, MODEL, prompt)
                response_txt=response.json()["choices"][0]["message"]["content"]

                if response_txt is None or response_txt == "":
                    raise ValueError("empty response")

                os.makedirs("./out", exist_ok=True)
                os.makedirs(f"./out/{f.split('.json')[0]}", exist_ok=True)

                correctness_metric = GEval(
                    name="Correctness",
                    model=judge_model,
                    evaluation_steps=[
                        "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
                        f"Check if the 'actual output' is in the {f.split('.json')[0]} category",
                        "Check if the 'actual output' is semantically the same as the 'expected output'",
                        "If the 'expected output' is composed of multiple parts, check if the 'actual output' contains all the necessary parts and is correct in each part, if the 'actual output' is composed of more or less parts than the 'expected output', check if the final result is correct even with the different number of parts",
                    ],
                    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
                )

                test_case = LLMTestCase(
                    input=prompt,
                    actual_output=response_txt,
                    expected_output=p["solution"]
                )

                correctness_metric.measure(test_case)

                print("Score:", correctness_metric.score)
                print("Reason:", correctness_metric.reason)

                with open(f"./out/{f.split('.json')[0]}/out.json","a") as f_res:
                    if p_index==0:
                        f_res.write("[")
                    if p_index!=len(prompt_arr)-1:
                        f_res.write(json.dumps({"response": response_txt, "score": correctness_metric.score, "reason": correctness_metric.reason})+",")
                    else:
                        f_res.write(json.dumps({"response": response_txt, "score": correctness_metric.score, "reason": correctness_metric.reason}))
                        f_res.write("]")
                    last_successful_index=p_index
                    p_index+=1

            except Exception as e:
                print("Error during generation ", str(e))
                p_index = last_successful_index+1