FROM debian:latest

# install basic utils
    RUN apt-get update
    RUN apt-get install -y nmap bwm-ng htop links2 screen apt-file strace git nano\
    mc hexedit lsof sudo socat nethogs iotop zip iftop sshfs wget tree\
    rsync mailutils dnsutils tmux curl netcat-openbsd net-tools jq iputils-ping\
    ca-certificates

# install operation tools
    RUN apt-get install -y ansible sshpass

# install services
    RUN apt-get install -y apache2 python3 python3-pip cron ssh
    RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# install docker (source: https://docs.docker.com/engine/install/debian/#install-using-the-repository)
    RUN install -m 0755 -d /etc/apt/keyrings
    RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    RUN chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    RUN apt-get update
    RUN apt-get install -y docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install graphical environment xrdp server
    RUN apt-get install -y xrdp xfce4 xfce4-goodies

# install developer environment
    RUN wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg \
    | gpg --dearmor > /usr/share/keyrings/vscodium-archive-keyring.gpg
    RUN echo 'Types: deb\nURIs: https://download.vscodium.com/debs\nSuites: vscodium\nComponents: main\nArchitectures: amd64 arm64\nSigned-by: /usr/share/keyrings/vscodium-archive-keyring.gpg' > /etc/apt/sources.list.d/vscodium.sources
    RUN apt-get update
    RUN apt-get install -y codium

RUN echo "root:password" | chpasswd 

ENTRYPOINT ["/ecorp/ecorp", "entrypoint"]
