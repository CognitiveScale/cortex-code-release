FROM c12e/cortex-python-lib:latest-develop
WORKDIR /app
COPY requirements.txt /app
COPY *.py /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python","/app/job.py"]
