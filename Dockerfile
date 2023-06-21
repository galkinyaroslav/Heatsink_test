FROM ubuntu:latest
LABEL authors="emmel"

ENTRYPOINT ["top", "-b"]