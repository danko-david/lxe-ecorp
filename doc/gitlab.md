# gitlab and the runner

GitLab CE (`gitlab/gitlab-ce`) at `http://gitlab.<ECORP_DNS_CORE_ZONE_NAME>`, container registry
at port `5005` of the same name. Its configuration, logs and data are in `data/gitlab/`.

## Logging in

- `root` with `GITLAB_ROOT_PASSWORD`.
- Every user of the domain (see [dc](dc.md)), on the *LDAP* tab of the login page.

## What provisioning sets up

- The URLs, in a marked block of `data/gitlab/config/gitlab.rb`; another marked block holds the
  LDAP connection. Outside these blocks the file is yours.
- An access token for `root` that provisioning itself uses (see [controller](controller.md)).
- Every `ECORP_*` variable of `.env` as an instance level CI/CD variable, so each pipeline knows
  where it runs: the DNS zone, the DNS server, the name of the infrastructure network, the
  storage root on the host and the SSH keys to authorize.
- Stored credentials for git in the controller, used by the steps that import repositories.

## Runners

One runner container, `core-gitlab-runner`, registered twice (list in
`units/controller/code/ansible/hosts.yml`):

| Runner | Picks up | Has |
| --- | --- | --- |
| Core infra runner | jobs tagged `core` | the docker socket of the host: its jobs can start containers next to the infrastructure. Meant for the projects that build infrastructure. |
| Core infra shared runner | untagged jobs | a docker volume for `/var/lib/docker`, no access to the host. |

Both use the domain controller as DNS server and only pull an image if it is not present.
