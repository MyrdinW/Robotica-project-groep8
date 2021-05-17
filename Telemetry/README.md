# REQUIREMENTS
1. install portaudio
2. on ubuntu: apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python3-opencv
3. pip install -r requirements.txt to install python deps

# DOCKER
1. dockerfile does all this
2. simply build the image:
3. docker build -t telemetrie .
4. and run
5. docker run -p 3000:3000 telemetrie