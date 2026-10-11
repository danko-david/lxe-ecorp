# TODOS

Keep this project minimal and outsource components to module projects that can be deployed separatly.
- runner config, volumes, dns, [runners.docker] pull_policy = "if-not-present"

### To test
Test from zero:
- open web vscode editor

### Releases
- Tags `1.0.0` and `1.1.0` do not exist in git although both were released (`lxeu/ecorp-diorama:1.1.0` was published on 2026-06-29). By the changelog and the publish time they belong on `122ce1c` (1.0.0) and `93942de` (1.1.0).

### Known problems
Found in the review for 1.2.0. Not fixed there because each changes behaviour and can only be verified with a full install (`./ecorp ci_test_infra`).

CI and image build (`./ecorp`):
- `ci_test_infra` and `build_diorama_image` cannot fail: their `cleanup` trap ends with `exit 0`, which replaces the exit status of whatever failed before. The install test job is green even if `./ecorp up` breaks.
- `ci_ensure_diorama` pushes `${REPO}ecorp-diorama:<version>`, but `build_diorama_image` only tags `ecorp-diorama:<version>` without the prefix; `REPO` is also used by the `docker pull` check before the function sets it. As written the push only works if something outside the script covers for it. To check against how 1.1.0 really got published.
- `run_in_container` starts the wrap container as compose project `ecorp`, the same project name the stack itself uses on a host.
- A local diorama build copies the whole working directory into the image (`COPY . /ecorp`): `.git`, `.env` and `settings/*.yml` included, only `data` and `tmp` are in `.dockerignore`. Customised passwords would end up in the image.
- All base images are unpinned (`debian:latest`, `gitlab/gitlab-ce:latest`, `gitlab/gitlab-runner:latest`, `coredns/coredns`), so the same ecorp version does not give the same diorama image twice.
- `purge` leaves the firewall rules and routes that host-controller added on the host.

Controller (`units/controller`):
- `gen_ssh_master_key` has its condition inverted: it generates the key only if it already exists, so never on a fresh install. Nothing in this repository uses the key either.
- `HOME_WWW_USER` / `HOME_WWW_PASSWORD` (basic auth for the web interface) can never be set: they are not in `.env.default`, not passed to the container, and the entrypoint does not read `.env`. The web interface is always open, and it can start provisioning and run docker.
- `follow_provision` and `_raw_follow_log` store `$?` instead of `$!` as the pid of the background `tail`. `follow_provision` leaves a `tail -f` behind in the controller on every call; the web one ends up calling `kill 0`.
- `index.cgi`: the `file` parameter of the log pages is used unchecked in a path and in the HTML; `/?page=dbg` is an unlinked page that prints the whole environment including every password; the `doc=` parameter renders files from `/ecorp/doc/`, which does not exist; `manage_ent ajax` has no `_ajax_*` function to call; `<html lang="hu">` on an English page.
- `script.js`: `ajax`, `ajaxResultSetTo` and `loopRun` are unused, every click is written to the console. `style.css`: `.info-block` is unused.
- `Dockerfile`: `cron` is installed and started with no crontab; `ssh` runs with `PermitRootLogin yes` and root password `password` on a container that holds the docker socket; `sshpass`, `wget`, `rsync` are not used by anything here. controller and host-controller only need the docker CLI but also install `containerd.io`, buildx and the compose plugin.
- `chk_prov` is true when provisioning is *not* running, and exists twice (helper and `index.cgi`).

Ansible:
- The GitLab root access token is the literal string `SUPER_SECRET_ROOT_TOKEN`, repeated in 17 places over 7 files. It is a fixed, public admin token on every install; at least it should be one variable.
- `gitlab_url` in `hosts.yml` is defined and never used: every task spells `http://gitlab.{{ ECORP_DNS_CORE_ZONE_NAME }}` out.
- `gitlab/dc_connect` sets `group_base`, `admin_group`, `sync_ssh_keys` and `ldap_sync_worker_cron`, which to my knowledge only GitLab EE acts on while the image is CE; `group_base` points to `OU=groups`, which nothing creates. `active_directory` is `false` against an AD.
- `dc/import_roles_users`: user and group existence is a substring match on the whole listing (`mcp` would match `mcpx`); `all_roles` is not unique because `| unique` binds to `user.roles` only, so groups are checked once per user that has them.
- `step/create_project_server`: `fail: No registration token available` is not a valid form of the module (needs `msg:`).
- `step/create_project_server` and `step/run_job` are not used by any shipped step file, `step/wait_pipelines` only by `steps/lxe-base-repos.yml`: they are never exercised by the install test.
- State files are in two places: `data/controller/last_imports/ad-users.yml` but `data/controller/last_steps.yml`.

Configuration:
- `DC_REALM=ecorp` and `DC_DOMAIN=ecorp.intra` look swapped compared to what Samba calls them (realm is the DNS-style name, domain/workgroup the short one). With `ECORP_DNS_CORE_ZONE_NAME=e-corp.intra.net` there are three different names for one thing: the DC's hostname is `dc.ecorp.intra`, GitLab reaches it as `dc.e-corp.intra.net`.
- `ECORP_CORE_NETWORK_BRIDGE` looks like a setting but is not one: the network is always `ecorp_core`, the variable only has to repeat it.
- `ECORP_SSH_EXTRA_AUTH` is described as "added to every managed ssh capable machine", nothing in this repository does that.
- `.gitignore` has `*.gitignore.*` and `gitignore.*`, which match nothing in the repository.
- `dev/diorama/docker-compose.yml` is not used by any command, `dev/ci_test/Dockerfile` duplicates `dev/ecorp_diorama_build_base.Dockerfile` without its `CMD`, and the helper images still use underscores (`ecorp_wrap_base`, `tmp_ecorp_diorama_build_base`) after 1.1.0 moved the published one to hyphens.
