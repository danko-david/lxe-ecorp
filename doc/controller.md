# controller

`units/controller` is the unit that turns the started containers into a working system. It has
the project mounted at `/ecorp` and the docker socket of the host, and does three things.

## Provisioning

`units/controller/code/ecorp controller_ansible_provision` runs the playbook
`units/controller/code/ansible/provision.yml`. It runs at every start of the container, with
`./ecorp provision` and from the *Actions* page of the web interface; only one run at a time.

| Role | What it does |
| --- | --- |
| `gitlab/configure` | Sets the URL of GitLab, makes sure the root access token works, publishes every `ECORP_*` variable as an instance CI/CD variable. |
| `dc/import_roles_users` | Imports `settings/ad-users.yml` into the domain controller, if the file changed. |
| `gitlab/dc_connect` | Connects GitLab to the domain controller through LDAP. |
| `gitlab/runner_register` | Registers the runners listed in `hosts.yml` that are not registered yet. |
| `step/main` | Executes the steps of `settings/steps.yml`, if the file changed. |

Every run writes a log into `data/controller/provision/logs/<date>_<time>` and its exit status
into the file of the same name ending in `.exit`.

What was applied is recorded in plain files; delete one to have that part done again:

| File under `data/controller/` | Meaning |
| --- | --- |
| `last_imports/ad-users.yml` | The user list that was imported last. |
| `last_imports/steps.yml` | The step file that was executed successfully last. |
| `last_imports/git_import/` | Mirrors of the git repositories imported by steps. |
| `provision/root_token` | Access token of the GitLab `root` user, generated once per installation. If GitLab stops accepting it (expired, deleted), provisioning sets it again. |
| `ssh/id_rsa`, `ssh/id_rsa.pub` | SSH key of the controller, generated at first start. |

## SSH key of the installation

The controller generates one SSH key. Its public half, followed by the keys in
`ECORP_SSH_EXTRA_AUTH` of `.env`, is the list of keys that may log in to machines managed by
this system:

- GitLab pipelines get the whole list in the variable `ECORP_SSH_EXTRA_AUTH`, one key per line.
  Module projects that create machines (for example project-server) authorize these keys.
- The controller accepts the same list for its own `root`, and uses its key by default, so
  `ssh root@<machine>` works from the controller to every machine built this way.

The controller only allows key logins. Keys in `data/controller/root/.ssh/authorized_keys` are
accepted too.

## DNS zone of the containers

`service_docker_dns_zones` listens to docker events and regenerates the configuration of the
[dns](dns.md) unit whenever a container starts or stops.

## Management web interface

`http://controller.<ECORP_DNS_CORE_ZONE_NAME>`, a bash CGI script (`code/www/index.cgi`):
this documentation, the variables of `.env`, the containers on the infrastructure network, the
users of the domain, and starting and following provisioning.

It is open by default. Set `HOME_WWW_USER` and `HOME_WWW_PASSWORD` in `.env` and recreate the
container (`./ecorp up`) to protect it with basic authentication. Anyone who can use it can start
provisioning, so treat it as an administrator interface.
