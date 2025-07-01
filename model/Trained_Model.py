


import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# تحميل النموذج والتوكنيزر بعد التدريب
model_path = "CATOGERY_model"
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
