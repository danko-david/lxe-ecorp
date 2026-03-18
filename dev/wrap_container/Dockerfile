FROM debian:latest

RUN apt-get update

# Install base utils
	RUN apt-get install -y curl

# install docker (source: https://docs.docker.com/engine/install/debian/#install-using-the-repository)
    RUN install -m 0755 -d /etc/apt/keyrings
    RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    RUN chmod a+r /etc/apt/keyrings/docker.asc
    RUN echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null
    RUN apt-get update
    RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Create user with password
RUN useradd -m user && echo 'user:password' | chpasswd
RUN echo "root:password" | chpasswd

RUN systemctl enable docker containerd

RUN apt-get clean

RUN usermod -aG sudo user

STOPSIGNAL SIGRTMIN+5

CMD ["/usr/sbin/init"]
