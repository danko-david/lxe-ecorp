FROM debian:latest

RUN apt-get update && apt-get install --no-install-recommends -y samba-ad-dc samba-client krb5-user \
	&& apt clean && rm -rf /var/lib/apt/lists/*

COPY dc /bin/dc

ENTRYPOINT ["/bin/dc", "entrypoint"]
