FROM python:3.12-slim
RUN apt-get update && apt-get install -y texlive-latex-base
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "Pi_Solve.py", "--server.port=8501", "--server.address=0.0.0.0"]
