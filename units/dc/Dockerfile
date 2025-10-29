FROM debian:trixie

RUN apt-get update

RUN apt-get install -y samba-ad-dc samba-client krb5-user # krb5-workstation

COPY dc /bin/dc

ENTRYPOINT ["/bin/dc", "entrypoint"]
