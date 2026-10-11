# TODOS

### To test
Test from zero:
- open web vscode editor
- a user disabled in the domain should be blocked in GitLab since `active_directory` is `true`: not covered by `tests/install`, which only signs in an enabled domain user.
- the web interface with `HOME_WWW_USER` set: not covered by `tests/install`.
- an installation made before 1.2.0 (with `DC_REALM` and `DC_DOMAIN` in `.env`) after upgrading: GitLab now binds as `CN=Administrator,CN=Users,DC=ecorp`.
- `ci_ensure_diorama` and `ci_weekly_diorama` against the real registry: only tested with the fake docker.

### To set up
- A weekly pipeline schedule on `master` in GitLab for `ci_weekly_diorama`.
