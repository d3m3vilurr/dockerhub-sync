FROM library/python:2.7-slim

WORKDIR /opt

RUN set -x \
    && cd /etc/apt \
    && sed -i 's/deb.debian.org/ftp.kaist.ac.kr/g' sources.list \
    && sed -i 's/security.debian.org/ftp.kaist.ac.kr\/debian-security/g' sources.list \
    && builds='curl' \
    && apt-get update && apt-get install -y $builds --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && cd /opt \
    && curl -L https://github.com/d3m3vilurr/dockerhub-sync/raw/master/requirement.txt -o requirement.txt \
    && pip install -r requirement.txt

COPY sync.py /opt/sync.py

ENTRYPOINT ["python", "sync.py"]
