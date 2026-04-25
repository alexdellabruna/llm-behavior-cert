# LLM Behavior Cert

This repo provides an experimental evaluation of LLM behavior through difficult prompts assessement.
The integrity is then evaluated calculating the Jensen-Shannon divergence.

Evaluation steps:

```bash
python assess.py --model-url <model url> --judge-url <judge url>
```

to visualize:

```bash
python visualize.py
```

to fine-tune:

```bash
axolotl train fine-tuning-axolotl/gpt-oss-20b-lora.yaml --output-dir="./fine-tuning-axolotl"
```

to merge LoRa weights:

```bash
axolotl merge-lora fine-tuning-axolotl/gpt-oss-20b-lora.yaml --lora-model-dir="./fine-tuning-axolotl/gpt-oss-lora-adapter" --output-dir="./fine-tuning-axolotl/final"
```

> NOTE: the repo doesn't include the full merged model due to storage limits, the complete model can be downloaded from the following <a href="https://huggingface.co/alexdellabruna/gpt-oss-20b-sft-lora">Hugging Face Repo</a>