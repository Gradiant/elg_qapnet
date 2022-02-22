FROM ubuntu:18.04

RUN apt-get update -y \
	&& apt-get install -y python3-pip python3-dev \
	&& apt-get install -y wget \
	&& apt-get install -y unzip \
	&& apt-get install -y git \
    && apt-get install -y git-lfs \
	&& rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install torch transformers flask_json flask flask-cors

ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8"


EXPOSE 8866

RUN mkdir -p qaptnet
WORKDIR /qaptnet/
RUN mkdir files

RUN git clone https://github.com/nunorc/qaptnet.git
WORKDIR /qaptnet/qaptnet
RUN sed -i "s/pytorch_transformers/transformers/g" qaptnet.py && \
    sed -i "s/self.model(torch.tensor(self.tokenizer.encode(string)).unsqueeze(0))/self.model(torch.tensor(self.tokenizer.encode(string)).unsqueeze(0), return_dict=False)/g" qaptnet.py && \
    sed -i "s/source = 'model-pretrained'/source = 'qaptnet\/model-pretrained'/g" qaptnet.py

RUN git lfs install
RUN git lfs pull

WORKDIR /qaptnet/
COPY ./serve.py /qaptnet/serve.py
CMD ["python3", "serve.py"]

