# host-controller

`units/host-controller` runs in the network namespace of the docker host with the right to
administer its network. It makes the containers reachable by address from each other and from
outside, which docker prevents by default.

## Firewall

At start it inserts two rules, both carrying the comment `ecorp-host-controller`:

- `filter` table, `FORWARD` chain: accept, so traffic is forwarded between docker networks,
- `raw` table, `PREROUTING` chain: accept, so containers can be addressed directly from outside.

This switches off the network isolation docker sets up **for every container on the host**, which
is why the stack belongs in a machine or container of its own.

## Routes

A container with the label `network_route=<CIDR>` has a network behind it. The host gets a route
to that network through the container, added when the container starts and removed when it
stops.

## Stopping

When the container is stopped (`./ecorp purge`, `docker compose down`, `docker stop`) it removes
the firewall rules with its comment and the routes it added. Rules added by a version before
1.2.0 carry no comment and stay until the host restarts or they are deleted by hand
(`iptables -D FORWARD -j ACCEPT`, `iptables -t raw -D PREROUTING -j ACCEPT`).
