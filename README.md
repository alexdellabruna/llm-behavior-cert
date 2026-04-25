# LLM Behavior Cert

This repo provides an experimental evaluation of LLM behavior through difficult prompts assessement.
The integrity is then evaluated calculating the JS/KL divergence.

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
axolotl train fine-tuning-axolotl/gpt-oss-20b-lora.yaml
```