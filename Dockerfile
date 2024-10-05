FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get remove libstdc++-11-doc libstdc++6-11-dbg
RUN apt-get install -y libstdc++-12-doc libstdc++6-12-dbg
RUN apt-get install -y cmake g++
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME=World

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
