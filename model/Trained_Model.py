# import torch
# from transformers import GPT2Tokenizer, GPT2LMHeadModel

# # List of model paths
# model_paths = [
#     "algebra_model",
#     "algebra_model",
#     # Add more models as needed
# ]

# # Load models and tokenizers
# models = []
# tokenizers = []

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# for path in model_paths:
#     tokenizer = GPT2Tokenizer.from_pretrained(path)
#     model = GPT2LMHeadModel.from_pretrained(path).to(device)
#     model.eval()
    
#     tokenizers.append(tokenizer)
#     models.append(model)

# # Use the first tokenizer as the main tokenizer (assumes same tokenization style)
# tokenizer = tokenizers[0]

# # Function to select the best model based on confidence
# def generate_best_answer(problem):
#     input_text = f"Q: {problem} A:"
#     inputs = tokenizer(input_text, return_tensors="pt").to(device)

#     best_output = None
#     best_confidence = float("-inf")

#     with torch.no_grad():
#         for model in models:
#             outputs = model(**inputs)
#             logits = outputs.logits  # Get model output logits

#             # Compute confidence score (sum of max logits per token)
#             confidence = logits.max(dim=-1).values.sum().item()

#             # Select the model with the highest confidence score
#             if confidence > best_confidence:
#                 best_confidence = confidence
#                 best_output = model.generate(
#                     **inputs,
#                     max_length=100,
#                     num_return_sequences=1,
#                     pad_token_id=tokenizer.eos_token_id
#                 )

#     # Decode the selected model's output
#     prediction = tokenizer.decode(best_output[0], skip_special_tokens=True)
#     return prediction

# # List of math problems to test
# problems_to_test = [
# "If 2 to the power of 8 equals 4 to the power of x, what is the value of x?"
# ]

# # Process each problem
# for problem in problems_to_test:
#     prediction = generate_best_answer(problem)
#     print(f"Problem: {problem}")
#     print(f"Prediction: {prediction}")
#     print("-" * 50)



import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# تحميل النموذج والتوكنيزر بعد التدريب
model_path = "algebra_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# ضبط الجهاز
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# اختبار بعض المسائل الرياضية
problems_to_test = [
"The two endpoints of a segment are at (1,4) and (1,10). What is the sum of the coordinates of the midpoint of the segment?"
]

for problem in problems_to_test:
    # تحويل السؤال إلى مدخلات النموذج
    input_text = f"Q: {problem} A:"
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    # توليد الإجابة
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=100,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )

    # طباعة النتائج
    prediction = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"Problem: {problem}")
    print(f"Prediction: {prediction}")
    print("-" * 50)
