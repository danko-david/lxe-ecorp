# Repo policy

Rules for anyone (human or AI tool) changing this repo. `README.md` describes what the project
is; this file says how to change it.

_First version, written from how the repository looks at 1.2.0. Pending review by David._

## 1. `./ecorp` is the only entry point

- Every command or workflow is a function in `./ecorp`. Do not add standalone scripts the user
  has to discover, a Makefile, or logic in `.gitlab-ci.yml`.
- Three more helper scripts in the same style run **inside** containers and are not called by
  the user: `units/controller/code/ecorp`, `units/host-controller/host-controller` and
  `units/dc/dc`. The root script reaches them with `dc exec` (`provision`, `follow_provision`).
- Functions that only make sense inside an image are named `inside_<where>__<what>`
  (`inside_diorama__build`) and carry no help line.
- CI entry points are named `ci_*`, carry a help line, and are the only thing a pipeline job
  calls.

## 2. Format of the helper scripts

- Tabs for indentation. Opening brace on its own line. `snake_case` function names, `__`
  between a namespace and a name. One blank line between functions.
- First statement of every user-facing function is `_rh_try_ret_help '<description>'`; mention
  arguments as `$1`, `$2`. Internal helpers omit it so they stay out of `help`.
- New functions go above the `RH built-in functions` banner. Do not modify the `RH helper
  functions`, `RH built-in functions` or `Application area` sections, they are the shared RH
  template. The one exception is the value of `ECORP_VERSION`.
- Reference repository files through `${ROOT}` (this project uses `ROOT`, not `HELPER_ROOT`).
  Inside containers the repository is always mounted or copied at `/ecorp`.
- Docker compose is called through `dc` (`docker compose -p ecorp`). The project name `ecorp`
  is load-bearing: container names (`ecorp-dc-1`, `ecorp-gitlab-1`,
  `ecorp-core-gitlab-runner-1`) and the network name (`ecorp_core`) are used literally in
  `units/controller/code/ansible/hosts.yml`, the roles and `.env.default`.

## 3. Units and services

- A self-built service is a directory in `units/<name>/` with its `Dockerfile` and, if it has
  logic, its own helper script whose `entrypoint` function the image starts.
- `docker-compose.yml` stays a plain list of services. Infrastructure services share the `x-def`
  anchor (restart policy, `core` network, the domain controller as DNS).
- Other containers join the infrastructure through labels (`dns_names`, `dns_mode`,
  `network_route`), not through changes in this repository. Keep it that way: this project is
  the minimal core, features belong in module projects (`project-server`, `build-images`, ...).

## 4. Configuration and state

- Configuration is environment variables in `.env`, spawned by `prepare` from `.env.default`.
  The default file is evaluated as a bash heredoc: escape `$` as `\$` unless it must be resolved
  at spawn time.
- A new variable goes into `.env.default` with a comment, into the table in `README.md`, and
  into the `environment:` list of the service that needs it. `ECORP_*` variables are published
  to every GitLab pipeline as instance variables: use that prefix only for values meant for
  them, and never for a secret.
- Files the user edits live in `settings/` as `<name>.yml.default`, are spawned by `prepare` and
  ignored by git.
- All runtime state is under `./data` (plus the `dc` volume). Do not read, quote, move or commit
  the contents of `data/`, `.env` or `settings/*.yml` unless the user names the file.
- Provisioning records what it has applied as plain files under `data/controller/`
  (`last_imports/`, `provision/`); deleting one makes that part run again.

## 5. Provisioning (Ansible)

- `units/controller/code/ansible/provision.yml` lists the roles in order; roles are grouped by
  what they act on: `dc/`, `gitlab/`, `step/`.
- **The filesystem is the registry for steps**: `step: <name>` in `settings/steps.yml` runs the
  role `roles/step/<name>`, with the keys of the step as its variables. A new step type is a new
  role directory plus a row in the step table of `README.md`. `step/main` is the dispatcher, not
  a step.
- Roles must be safe to run again: provisioning runs at every start of the controller.
- Ansible talks to the other containers with `docker exec` from the controller (`ad_exec`,
  `runner.target`) and to GitLab through its HTTP API.
- A ready-made step file goes to `steps/`; `settings/steps.yml.default` stays the smallest set
  that makes the system usable, because it decides the build time and size of the diorama image.

## 6. Version and release

- `ECORP_VERSION` in `./ecorp` equals the topmost heading of `CHANGELOG.md`
  (`tests/offline/version_matches_the_topmost_changelog_entry`).
- The version is also the tag of the published `ecorp-diorama` image: `ci_ensure_diorama`
  builds and publishes on `master` whenever the registry has no image for the current version.
  Raising the version therefore publishes; changing the stack without raising it does not,
  until the weekly build (`ci_weekly_diorama`) publishes it as `<version>-<year>w<week>`.
- Images are built from what git would commit (`build_source_image`), never from the whole
  working directory. Service images stay unpinned on purpose, the weekly build ships their
  fixes.
- Add a line to `CHANGELOG.md` for every change a user of the project would notice, in the same
  change. Format: version heading `X.Y.Z:`, tab-indented `- ` items, newest first.
- "commit changes" means: run `./ecorp run_tests`, bring `README.md`, the container files and
  `CHANGELOG.md` up to date, then commit on the current branch. "release" means the same plus an
  annotated tag named after the topmost changelog version. Neither pushes. There are two
  remotes: `origin` (internal GitLab) and `github` (public mirror).

## 7. Tests

- `./ecorp run_tests` runs every executable in `tests/offline/`. They need no docker, network
  or credentials, and must pass before a change is reported as done. CI runs them first.
- `./ecorp run_tests_install` runs `tests/install/` against a running, provisioned stack.
  `./ecorp ci_test_infra` installs the stack from zero in a container and runs them there; it
  needs docker and the internet, takes long and is not a gate.
- A test is a bash script named after the behaviour it shows, in plain words, one behaviour per
  file; it sources `tests/lib`, exits non-zero on failure and 77 when it has to be skipped.
  Adding a file adds the test.
- Offline tests work on a copy in a temporary directory (`make_sandbox`) and never touch
  `data/`, `.env` or `settings/*.yml`. What a command does with docker is tested against
  `tests/fake/docker` (`use_fake_docker`), which records its calls instead of doing anything.
- Any check written to verify a change is added there in the same change: offline if it can be,
  as an install test if it needs the running stack.
- A change to a unit, the compose file or a role is not verified by the offline tests: say so,
  and say whether the full install was run.

## 8. Change hygiene

- Do only what was asked. Known problems are listed in `TODO.md`; they are not fixed as a side
  effect. New findings are added there with the reason, not left as a comment in the code.
- Update `README.md` when a command, variable, step type, label or directory changes, and the
  page of the unit in `doc/` when its behaviour changes. `doc/*.md` is rendered by the web
  interface: link between pages with plain relative links (`dns.md`, from the README
  `doc/dns.md`), the interface rewrites them.
- Secrets are generated per installation into `data/` (`provision/root_token`, `ssh/id_rsa`),
  never written into the repository as a constant.
- Linux only, bash and standard tools. Do not add a dependency to the host side; what a
  container needs goes into its `Dockerfile`.
- Only scripts are executable, and they carry no extension unless something requires one
  (`index.cgi`).
- Commit only when asked.
