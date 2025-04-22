import os
import time

from flask import Flask, request, jsonify
from llama_cpp import Llama

app = Flask(__name__)

MODEL_PATH = "./models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"

n_threads = int(os.getenv('N_THREADS', 4))
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_batch=512,
    n_threads=n_threads,
    n_gpu_layers=-1,
    verbose=True
)
@app.route("/chat", methods=["POST"])
def chat():
    start = time.time()
    user_input = request.json["message"]

    prompt = f"""
<|system|>Você é um assistente útil que responde sempre em português.<|end|>
<|user|>{user_input}<|end|>
<|assistant|>
    """.strip()

    output = llm(
        prompt,
        max_tokens=1000,
        temperature=0.7,
        top_p=0.9,
        stop=["<|user|>", "<|system|>", "<|end|>"]
    )

    reply = output['choices'][0]['text'].strip()
    end = time.time()
    print(f"Response time: {end - start:.2f} seconds")
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
