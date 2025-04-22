FROM python:3-slim AS build
COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

FROM python:3-slim
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/bin
WORKDIR /app
COPY --from=build /root/.local /root/.local
COPY frontend.py frontend.py
CMD ["streamlit", "run", "frontend.py"]