import os
import torch
import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer, TrainingArguments, Trainer
from datasets import Dataset
from peft import LoraConfig, get_peft_model

# ✅ Set device (Use GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ✅ Load base model & tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
base_model = T5ForConditionalGeneration.from_pretrained(model_name)

# ✅ Apply LoRA Configuration
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=["q", "v"],  # LoRA applied to query & value layers
    task_type="SEQ_2_SEQ_LM"
)

model = get_peft_model(base_model, lora_config)
model.to(device)

# ✅ Print LoRA model summary
print("\n🔍 LoRA Model Summary:")
model.print_trainable_parameters()

# ✅ Load dataset
df = pd.read_excel("algebra.xlsx")

# ✅ Convert DataFrame to Hugging Face Dataset
dataset = Dataset.from_pandas(df)

# ✅ Preprocessing function
def preprocess_function(examples):
    inputs = ["question: " + q for q in examples["question"]]
    targets = examples["answer"]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length").input_ids
    model_inputs["labels"] = labels
    return model_inputs

# ✅ Tokenize dataset
tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=dataset.column_names)

# ✅ Define training arguments
training_args = TrainingArguments(
    output_dir="./t5-lora-probability-model",
    per_device_train_batch_size=8,
    learning_rate=3e-4,
    num_train_epochs=3,
    save_strategy="epoch",
    evaluation_strategy="no",  # No evaluation dataset
    logging_dir="./logs",
    logging_steps=100,
)

# ✅ Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
)

# ✅ Train the model
print("\n🚀 Starting LoRA Fine-Tuning...")
trainer.train()

# ✅ Check if LoRA parameters are trained
print("\n🔍 Checking trained LoRA parameters...")
model.print_trainable_parameters()

# ✅ Save fine-tuned LoRA model
print("\n✅ Saving Fine-Tuned LoRA Model...")
model.save_pretrained("./t5-lora-probability-model", safe_serialization=False)
tokenizer.save_pretrained("./t5-lora-probability-model")

# ✅ Verify model save success
if os.path.exists("./t5-lora-probability-model/adapter_model.bin"):
    print("✅ LoRA Model Saved Successfully.")
else:
    print("❌ ERROR: adapter_model.bin not saved! Check training and paths.")
