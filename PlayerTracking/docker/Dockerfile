FROM tensorflow/tensorflow:1.12.0-py3

LABEL Name=tensorflow-objectdetection-training Version=0.0.1

WORKDIR /app
COPY requirements.txt /app

RUN python3 -m pip install -r requirements.txt
RUN apt-get update && apt-get -q -y install git-core wget
RUN cd /usr/local/lib/python3.5/dist-packages/tensorflow/ && mkdir models && cd models && git init && git remote add models https://github.com/tensorflow/models.git && git fetch models && git checkout models/master && git checkout 0558408 -- research/object_detection && git checkout 0558408 -- research/slim
RUN git clone https://github.com/cocodataset/cocoapi.git && cd cocoapi/PythonAPI && make && cp -r pycocotools /usr/local/lib/python3.5/dist-packages/tensorflow/models/research/
RUN cd /usr/local/lib/python3.5/dist-packages/tensorflow/models/research && wget -O protobuf.zip https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip && unzip protobuf.zip && ./bin/protoc object_detection/protos/*.proto --python_out=.

ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.5/dist-packages/tensorflow/models/research:/usr/local/lib/python3.5/dist-packages/tensorflow/models/research/slim"
ENV TFRESEARCH "/usr/local/lib/python3.5/dist-packages/tensorflow/models/research"

CMD ["/bin/bash"]