FROM python:3.8
WORKDIR /app
ADD src/. /app/.
ADD requirements.txt /app
RUN mkdir log
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]