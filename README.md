# LLM Behavior Cert

This repo provides an experimental evaluation of LLM behavior through difficult prompts assessement.
The integrity is then evaluated calculating the Jensen-Shannon divergence.

The model used in the experiments is `gpt-oss-20b`, on that is applied a soft fine tuning with QLoRA, then the integrity is calculated. For a full overview of the process see the methodology section.

The experiments were conducted on an architecture composed of a K3S cluster with 4 GPUs (1 A40 and 3 L40S):
- model server: vLLM (both for `gpt-oss-20b` and `gpt-oss-20b-qlora`)
- judge model server: Ollama (running `deepseek-r1:70b`)

All settings are configurable in `settings.py`.

Evaluation steps:

```bash
python assess.py --model-url <model url> --judge-url <judge url>
```

to visualize:

```bash
python visualize.py
```

to fine-tune we used Unsloth Studio, the used configuration can be found in the `fine-tuning-unsloth/gpt_oss_20b_qlora.conf`

to calculate distance:

```bash
python analyze.py --comp-out-dir <saved outputs to compare>
```

> NOTE: the repo doesn't include the full merged model due to storage limits, the complete model can be downloaded from <a href="https://huggingface.co/alexdellabruna/gpt-oss-20b-qlora">Hugging Face Repo</a>, the QLoRA adapter can be downloaded from <a href="https://huggingface.co/alexdellabruna/gpt-oss-20b-qlora-adapter">Hugging Face Repo</a>

Methodology:

<img src="scheme.png">

Results:

Math Prompt Integrity:

Final result: integral (JS Divergence: 0.02263192461839762)

<img src="analyze_out/math.png">

Logics Prompt Integrity:

Final result: not integral (JS Divergence: 0.10179068552486605)

<img src="analyze_out/logics.png">