import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from trl import SFTTrainer
from datasets import load_dataset

model_name = "mistralai/Mistral-7B-v0.1"
#model_name = "openai-community/gpt2"
data_files = {"train":"output.json"}
dataset = load_dataset('json', data_files=data_files)
print(dataset["train"][0])

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.add_eos_token = True
tokenizer.add_bos_token, tokenizer.add_eos_token
#tokenizer.padding_side = 'right'

model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32,device_map="cuda")
model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
model.config.pretraining_tp = 1
model.gradient_checkpointing_enable()

training_arguments = TrainingArguments(
    output_dir= "./checkpoints",
    num_train_epochs= 4,
    per_device_train_batch_size= 16,
    gradient_accumulation_steps= 4,
    optim = "adamw_torch",
    save_steps= 5000,
    logging_steps= 30,
    learning_rate= 2e-4,
    weight_decay= 0.001,
    fp16= True, 
    bf16= False,
    max_grad_norm= 0.3,
    max_steps= -1,
    warmup_ratio= 0.3,
    group_by_length= True,
    lr_scheduler_type= "constant"
)
# Setting sft parameters
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    max_seq_length= 1024,
    dataset_text_field="text",
    tokenizer=tokenizer,
    args=training_arguments
)

trainer.train()
tokenizer.save_pretrained("./drug-gpt")
model.save_pretrained('./drug-gpt')
model.config.use_cache = True
model.eval()