FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y curl jq && \
    apt-get clean

USER jenkins
