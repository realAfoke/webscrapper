#Use python official image
From python:3.12-slim

#set working directory
WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy project files
COPY . .

#Expose Django defualt port
EXPOSE 8000

#rUN Django server
CMD ["gunicorn","setting.wsgi:application","--bind","0.0.0.0:8000","--log-file","-"]
