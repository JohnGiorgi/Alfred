FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "alfred.app"]
EXPOSE 5000
