FROM debian:latest

# Install base utils
RUN apt-get update \
    && apt-get install --no-install-recommends -y systemd systemd-sysv curl ca-certificates net-tools iptables\
    && apt clean && rm -rf /var/lib/apt/lists/*

# install docker (source: https://docs.docker.com/engine/install/debian/#install-using-the-repository)
    RUN install -m 0755 -d /etc/apt/keyrings
    RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    RUN chmod a+r /etc/apt/keyrings/docker.asc
    RUN echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null
    RUN apt-get update \
        && apt-get install --no-install-recommends -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin \
        && apt clean && rm -rf /var/lib/apt/lists/*

# Enable
RUN systemctl enable docker containerd

STOPSIGNAL SIGRTMIN+5

CMD ["/usr/sbin/init"]
