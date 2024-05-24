#!/usr/bin/env python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def setup():
    model_name = "./drug-gpt"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="cuda", trust_remote_code=True)
    model.eval()
    return model, tokenizer

def generate(model, tokenizer, prompt, length):
    input_ids = torch.tensor([tokenizer.encode(prompt, add_special_tokens=False)], dtype=torch.long).to("cuda")
    outputs = model.generate(
        input_ids,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        max_length=length + len(input_ids[0]),
        temperature=0.9,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        repetition_penalty=1.1
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return generated_text

if __name__ == "__main__":
    model, tokenizer = setup()
    sent = generate(model, tokenizer, "Look at this, a ", 50)
    print(sent)