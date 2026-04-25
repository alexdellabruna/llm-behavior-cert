---
library_name: peft
license: apache-2.0
base_model: openai/gpt-oss-20b
tags:
- axolotl
- base_model:adapter:openai/gpt-oss-20b
- lora
- transformers
datasets:
- HuggingFaceH4/Multilingual-Thinking
pipeline_tag: text-generation
model-index:
- name: outputs/gpt-oss-out/
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

[<img src="https://raw.githubusercontent.com/axolotl-ai-cloud/axolotl/main/image/axolotl-badge-web.png" alt="Built with Axolotl" width="200" height="32"/>](https://github.com/axolotl-ai-cloud/axolotl)
<details><summary>See axolotl config</summary>

axolotl version: `0.16.1`
```yaml
base_model: openai/gpt-oss-20b
use_kernels: false
model_quantization_config: Mxfp4Config
model_quantization_config_kwargs:
  dequantize: true

plugins:
  - axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin

experimental_skip_move_to_device: true  # prevent OOM by NOT putting model to GPU before sharding

datasets:
  - path: HuggingFaceH4/Multilingual-Thinking
    type: chat_template
    field_thinking: thinking
    template_thinking_key: thinking

dataset_prepared_path: last_run_prepared
val_set_size: 0
output_dir: ./outputs/gpt-oss-out/

sequence_len: 4096
sample_packing: true

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

trackio_project_name:
trackio_run_name:
trackio_space_id:

gradient_accumulation_steps: 2
micro_batch_size: 1
num_epochs: 1

adapter: lora
lora_r: 8
lora_alpha: 16
lora_dropout: 0.0  # dropout not supported when using LoRA over expert parameters
lora_target_linear: true

optimizer: adamw_torch_8bit
lr_scheduler: constant_with_warmup
learning_rate: 2e-5

bf16: true
tf32: true

flash_attention: false
attn_implementation: eager  # this is not needed if using flash_attn >= 2.8.3

gradient_checkpointing: true
activation_offloading: true

logging_steps: 1
saves_per_epoch: 1

warmup_ratio: 0.03

special_tokens:
eot_tokens:
  - "<|end|>"

# choose the zero3 configuration that best fits your system capabilities
deepspeed: deepspeed_configs/zero3_bf16.json

```

</details><br>

# outputs/gpt-oss-out/

This model is a fine-tuned version of [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) on the HuggingFaceH4/Multilingual-Thinking dataset.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 1
- eval_batch_size: 1
- seed: 42
- distributed_type: multi-GPU
- num_devices: 4
- gradient_accumulation_steps: 2
- total_train_batch_size: 8
- total_eval_batch_size: 4
- optimizer: Use OptimizerNames.ADAMW_TORCH_8BIT with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: constant_with_warmup
- training_steps: 33

### Training results



### Framework versions

- PEFT 0.19.1
- Transformers 5.5.0
- Pytorch 2.10.0+cu128
- Datasets 4.5.0
- Tokenizers 0.22.2