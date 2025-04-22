# ./app.py
import os
import time

from flask import Flask, Response, request, jsonify
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
    user_input = request.json["message"]

    prompt = f"""
    <|system|>Você é Sofia, uma assistente virtual que responde sempre em português com clareza, empatia e foco técnico.<|end|>
    <|user|>{user_input}<|end|>
    <|assistant|>
    """.strip()

    def generate():
        start = time.time()
        try:
            for chunk in llm.create_completion(
                prompt=prompt,
                max_tokens=1000,
                stream=True,
                temperature=0.8,
                top_p=0.9,
                stop=["<|user|>", "<|system|>", "<|end|>"]
            ):
                token = chunk["choices"][0]["text"]
                yield token
        finally:
            end = time.time()
            print(f"⏱️ Tempo de resposta: {end - start:.2f} segundos")

    return Response(generate(), content_type="text/plain; charset=utf-8")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
