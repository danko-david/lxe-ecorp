# Wrap container and diorama image

Two ways to keep the stack off your host. Both use the same base image (`ecorp-wrap-base`,
`dev/ecorp_wrap_base.Dockerfile`): Debian with systemd and a docker daemon of its own.

## Wrap container

`./ecorp run_in_container` starts that image (`dev/wrap_container/docker-compose.yml`), clones
the committed state of this repository into it and runs `./ecorp up` inside. The docker data of
the inner daemon is kept in `dev/wrap_container/data/`. At the end it prints the route that makes
the inner network reachable from the host.

## Diorama image

`ecorp-diorama` is the stack already installed and provisioned, baked into one image: larger to
download, but running in the time GitLab needs to boot. It is published as `lxeu/ecorp-diorama`.

`./ecorp build_diorama_image` builds it: the project is copied into the base image, the stack is
installed in a container of it, and the result is committed together with the docker data of the
inner daemon. Only files git would commit are copied, so your `.env`, `settings/*.yml` and `data`
never get into an image.

To run it:

```yaml
services:
  ecorp:
    image: lxeu/ecorp-diorama:latest
    restart: unless-stopped
    cap_add:
      - ALL
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
      - systempaths=unconfined
    tmpfs:
      - /tmp
      - /run
    volumes:
      # Required for systemd
      - /sys/fs/cgroup:/sys/fs/cgroup
      # Required for docker (Overlay can't be mounted on overlay)
      - docker:/var/lib/docker
      - containerd:/var/lib/containerd
      - storage:/ecorp/data/storage

volumes:
  docker:
  containerd:
  storage:
```

## Published tags

| Tag | Built | Content |
| --- | --- | --- |
| `<version>` | once, when the version of `./ecorp` is raised on `master` | That version of this project on the service images of that day. |
| `<version>-w<week>` | by the weekly schedule | The same version of this project, rebuilt on the newest Debian, GitLab, runner and CoreDNS images, so their fixes are shipped. `<week>` is the ISO week of the year. |
| `latest` | with both | The newest of the above. |

The service images are deliberately not pinned: the weekly build is what keeps the diorama
current.
