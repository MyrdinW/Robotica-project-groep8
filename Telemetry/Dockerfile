# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN apt-get update
RUN apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python3-opencv
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./API.py" ]