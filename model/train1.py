import json
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset

# Load and preprocess data
def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return [{"text": f"Q: {item['question']} A: {item['answer']}"} for item in data]

# Load datasets
probability_data = load_json("CATOGERY_test.json")


# Combine datasets
full_data = probability_data 

# Convert to Hugging Face dataset format
dataset = Dataset.from_list(full_data)

# Load GPT-2 Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

# Tokenize dataset
def tokenize_function(example):
    return tokenizer(example["text"], padding="max_length", truncation=True, max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Load GPT-2 Model
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Training arguments with optimizations
training_args = TrainingArguments(
    output_dir="./math_model",
    evaluation_strategy="steps",
    save_steps=500,
    logging_steps=50,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    learning_rate=5e-5,
    warmup_steps=500,
    weight_decay=0.01,
    gradient_accumulation_steps=2,
    fp16=True,  # Enable mixed precision training
    save_total_limit=3,  # Keep only the latest 3 checkpoints
    logging_dir="./logs",
    report_to="none",  # Disable online logging services
)

# Data Collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Trainer Setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train Model
trainer.train()

# Save Model
trainer.save_model("math_model")
tokenizer.save_pretrained("math_model")