# Use the official Python 3.10 image
FROM python:3.10-buster

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gcc \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    git 

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs

RUN git config --global user.email "alain.seys@vanmarcke.be"
RUN git config --global user.name "Alain Seys"

# Install PIP requirements


# Optional: If you need to install Python packages here, uncomment the following lines
 COPY requirements.txt .
 RUN pip install -r requirements.txt

 RUN git config --global http.sslverify false
