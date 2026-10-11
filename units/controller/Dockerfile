FROM debian:latest

# install basic utils
    RUN apt-get update && apt-get install --no-install-recommends -y tini git nano sudo wget \
    rsync dnsutils curl netcat-openbsd net-tools jq iputils-ping \
    ca-certificates \
    ansible sshpass \
    apache2 python3 python3-pip cron ssh \
    pandoc \
    && apt clean && rm -rf /var/lib/apt/lists/*

    # ssh: key logins only. Accepted keys: /root/.ssh/authorized_keys and the
    # ones the entrypoint collects (ECORP_SSH_EXTRA_AUTH and the controller's own)
    RUN printf '%s\n' \
    'PermitRootLogin prohibit-password' \
    'PasswordAuthentication no' \
    'AuthorizedKeysFile .ssh/authorized_keys /etc/ssh/ecorp_authorized_keys' \
    > /etc/ssh/sshd_config.d/ecorp.conf

# install docker (source: https://docs.docker.com/engine/install/debian/#install-using-the-repository)
    RUN install -m 0755 -d /etc/apt/keyrings
    RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    RUN chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null

    RUN apt-get update && apt-get install --no-install-recommends -y docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN pip install --break-system-packages python-gitlab

ENTRYPOINT ["/usr/bin/tini", "/ecorp/units/controller/code/ecorp", "--", "entrypoint"]
