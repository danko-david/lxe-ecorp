FROM debian:latest

# install basic utils
    RUN apt-get update
    RUN apt-get install -y nmap git nano sudo socat wget \
    rsync dnsutils tmux curl netcat-openbsd net-tools jq iputils-ping \
    ca-certificates \
    ansible sshpass \
    apache2 python3 python3-pip cron ssh \
    pandoc

    RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# install docker (source: https://docs.docker.com/engine/install/debian/#install-using-the-repository)
    RUN install -m 0755 -d /etc/apt/keyrings
    RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    RUN chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null

    RUN apt-get update
    RUN apt-get install -y docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

RUN echo "root:password" | chpasswd 

ENTRYPOINT ["/ecorp/units/controller/code/ecorp", "entrypoint"]
