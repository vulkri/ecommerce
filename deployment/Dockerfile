FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV IN_A_DOCKER_CONTAINER Yes
ARG UID
ARG GID


RUN --mount=type=cache,target=/var/cache/apt \
	apt-get update && \
    apt-get install --no-install-recommends -y build-essential libpq-dev 

RUN apt install -y sudo && \
    addgroup --gid $GID nonroot && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot && \
    rm -rf /var/lib/apt/lists/* \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

WORKDIR /home/nonroot/app

COPY backend/requirements.txt ./requirements.txt
COPY deployment/scripts /home/nonroot/deployment/scripts

RUN chown -R nonroot:nonroot /home/nonroot/app
RUN chown -R nonroot:nonroot /home/nonroot/deployment/scripts
USER nonroot

RUN --mount=type=cache,target=/home/nonroot/.cache/pip \
    pip install pip --upgrade \
    && pip install -r requirements.txt

COPY backend/ ./

RUN chmod -R +x /home/nonroot/deployment/scripts/*
