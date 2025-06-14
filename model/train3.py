import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset

# Load and preprocess data
def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return [{"text": f"Solve: {item['question']} Answer: {item['answer']}"} for item in data]

# Load datasets
probability_data = load_json("probability.json")
geometry_data = load_json("geometry.json")
algebra_data = load_json("algebra.json")

# Combine datasets
full_data = probability_data + geometry_data + algebra_data

# Convert to Hugging Face dataset format
dataset = Dataset.from_list(full_data)

# Load T5 Tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")
tokenizer.pad_token = tokenizer.eos_token

# Tokenize dataset
def tokenize_function(example):
    return tokenizer(example["text"], padding="max_length", truncation=True, max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Load T5 Model with LoRA Config
model = T5ForConditionalGeneration.from_pretrained("t5-small")
lora_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,  # T5 is a seq2seq model
    r=8,  # Low-rank matrix size
    lora_alpha=32,  # Scaling factor
    lora_dropout=0.05
)
model = get_peft_model(model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir="./math_model",
    evaluation_strategy="steps",
    save_steps=500,
    logging_steps=50,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    learning_rate=5e-4,  # Increased LR for LoRA
    warmup_steps=500,
    weight_decay=0.01,
    gradient_accumulation_steps=2,
    fp16=True,
    save_total_limit=3,
    logging_dir="./logs",
    report_to="none",
)

# Trainer Setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
    tokenizer=tokenizer,
)

# Train Model
trainer.train()

# Save Model
trainer.save_model("./math_model")
tokenizer.save_pretrained("./math_model")