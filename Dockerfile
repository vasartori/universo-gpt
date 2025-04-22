FROM nvidia/cuda:12.4.1-devel-ubuntu22.04 AS builder
ENV GGML_CUDA=1
ENV CMAKE_ARGS="-DGGML_CUDA=on"
COPY requirements.txt requirements.txt
RUN apt update && apt install -y build-essential git python3-pip ninja-build && pip install --user -r requirements.txt

FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04 AS app
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/bin
WORKDIR /app
RUN apt update && apt install -y libgomp1 python3
COPY templates templates
COPY static static
COPY app.py app.py
COPY --from=builder /root/.local /root/.local
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]