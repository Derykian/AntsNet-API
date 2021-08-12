# Set base image (host OS)
FROM python:3.8

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install -U pip

# ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
# COPY app.py .
# COPY detect.py .
# COPY best.pt .
# COPY models .
# COPY utils .
COPY . .

# RUN mkdir static
# RUN mkdir uploads
# RUN mkdir runs
RUN ln -s runs static/runs

# Specify the command to run on container start
# CMD [ "python", "./app.py" ]
ENTRYPOINT FLASK_APP=app.py flask run --host=0.0.0.0