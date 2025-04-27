from fastapi import FastAPI
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import uvicorn,os

os.environ['HF_TOKEN'] = ""
app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")

model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-2b-it",
    device_map="auto",
    low_cpu_mem_usage=True,
    torch_dtype=torch.float16
)


def generate_response(input_text: str) -> str:
    try:
        inputs = tokenizer(input_text, return_tensors="pt").to("cpu")
        outputs = model.generate(inputs["input_ids"], max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response
    except Exception as e:
        print(f"오류 발생: {e}")
        return "응답 생성에 실패했습니다."

@app.post("/chat/")
async def chat(message: str):
    response = generate_response(message)
    return {"response": response}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)