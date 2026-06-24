FROM debian:latest

RUN apt-get update && apt-get install --no-install-recommends -y tini samba-ad-dc samba-client krb5-user samba-ad-provision \
	&& apt clean && rm -rf /var/lib/apt/lists/*

COPY dc /bin/dc

ENTRYPOINT ["/usr/bin/tini", "/bin/dc", "--", "entrypoint"]
