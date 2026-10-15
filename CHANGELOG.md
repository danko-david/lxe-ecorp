1.2.1:
	- Open work moved from TODO.md to tickets on a Backlog.md board in backlog/ (backlog board, backlog browser), one ticket per former item.

1.2.0:
	Fixes from a review of the whole repository, tests, documentation and policy. Existing installations: see the items marked "Upgrade".
	- The access token of the GitLab root user is generated once per installation (data/controller/provision/root_token) instead of being the same fixed string everywhere. Upgrade: the next provisioning replaces the old token by itself.
	- The controller generates its SSH key at first start (it never did). Pipelines get its public key, followed by the keys of ECORP_SSH_EXTRA_AUTH, in the ECORP_SSH_EXTRA_AUTH variable, so machines built by module projects accept both.
	- SSH into the controller: keys only, root has no password any more. Accepted are the controller's own key, the keys of ECORP_SSH_EXTRA_AUTH and data/controller/root/.ssh/authorized_keys. Upgrade: logging in with root/password stops working.
	- HOME_WWW_USER and HOME_WWW_PASSWORD in .env protect the management web interface with a password (they had no effect before).
	- Web interface: log pages only show provisioning logs, the hidden debug page that printed the environment is gone, unit documentation from the new doc/ directory is linked from the main page.
	- host-controller marks its firewall rules and removes them, together with the routes it added, when it is stopped; purge leaves the host as it was. Upgrade: the unmarked rules of earlier versions stay until reboot.
	- ./ecorp provision and ./ecorp up exit with the status of the provisioning; follow_provision no longer leaves a process behind in the controller.
	- CI: ci_test_infra and build_diorama_image fail when the install fails (they always succeeded), and ci_test_infra also runs the install tests.
	- CI: ci_ensure_diorama names the image with the REPO prefix before pushing and looks for the existing version under it. Set REPO (lxeu/) and DOCKER_REGISTRY_USERNAME/PASSWORD; DOCKER_REGISTRY is only needed for a registry other than Docker Hub.
	- ci_weekly_diorama: new command for a weekly schedule, rebuilds the current version on the newest base images and publishes it as <version>-<year>w<week> (1.2.0-26w42) and latest.
	- Images are built from what git would commit: .env, settings/*.yml, data and .git no longer get into a locally built diorama image.
	- Users and roles: existence is checked by exact name (a user named like the beginning of another one was skipped), each role is created once.
	- The domain of the domain controller is named after ECORP_DNS_CORE_ZONE_NAME: ad.<zone> (ad.e-corp.intra.net), short name from the first label of the zone (E-CORP). DC_REALM and DC_DOMAIN are gone from .env.default. Upgrade: keep both in the .env of an existing installation, they still win, a created domain cannot be renamed.
	- GitLab LDAP configuration without the group, admin group and SSH key synchronisation settings, which GitLab CE ignores.
	- GitLab treats the domain controller as an Active Directory (active_directory true), so accounts disabled in the domain are noticed, and binds with the full name of the Administrator.
	- create_project_server step: a missing runner token is reported with its message instead of a module error.
	- The record of executed steps moved to data/controller/last_imports/steps.yml. Upgrade: moved automatically.
	- run_tests: new command, runs the offline tests in tests/offline. Needs no docker or network. CI runs it in every pipeline before anything else.
	- run_tests_install: new command, tests a running, provisioned stack.
	- Helper images are named ecorp-wrap-base and ecorp-diorama-build-base. dev/diorama/docker-compose.yml is now an example in doc/diorama.md.
	- README describes the services, commands, every variable of .env, the step types, the container labels and the CI variables. AGENTS.md: rules for changing this repository.
	- Git tags 1.0.0 and 1.1.0 added for the earlier releases.

1.1.0:
	- ecorp_diorama changed to ecorp-diorama. This image will be published in dockerhub, following the name conventions.
	- devops-build-image built separately and published where: https://hub.docker.com/r/lxeu/devops-build-image
	- remove building devops-build-image from default steps and leaving a copy of the original into a storage directory ./steps/. This makes builds faster and diorama image smaller

1.0.0:
	Released with basic functionalities: coredns nameserver, dc, controller, host controller, gitlab, core-gitlab-runner with automatic self provision, registering user accounts, runner, and run a step file makes the system ready to operate.
	- wrap container, if you don't want to run directly on the host
	- ecorp_diorama image: bake whole basic infrastructure into one runnable image, so you can tradeoff build time for image size and launch a whole ecorp instance inside a container (like in wrap container but this image has a whole installed base system). This makes module testing easier in CI/CD environment
