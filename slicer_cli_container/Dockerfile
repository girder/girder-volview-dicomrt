FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y python3-vtk7
RUN pip3 install itk
RUN pip3 install girder_client ctk_cli numpy==1.23.1 rt_utils

COPY . $PWD
ENTRYPOINT ["python3", "./cli_list.py"]
ENV PYTHONUNBUFFERED=TRUE
