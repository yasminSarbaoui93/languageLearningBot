FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
#copy everything from the current directory (my local one) to the container current directory (/app)
COPY . . 
CMD ["python", "src/app.py"]