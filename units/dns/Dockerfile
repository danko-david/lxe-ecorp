FROM  coredns/coredns

COPY Corefile /etc/coredns/Corefile

ENTRYPOINT ["/coredns", "-conf", "/etc/coredns/Corefile"]