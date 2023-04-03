FROM c12e/cortex-python-lib:latest-develop
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["python3", "predict/main.py"]
