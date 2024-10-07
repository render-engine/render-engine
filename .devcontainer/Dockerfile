ARG IMAGE="thekevjames/nox:2019.11.9"
FROM --platform=amd64 ${IMAGE}
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends build-essential libssl-dev gdb cmake
