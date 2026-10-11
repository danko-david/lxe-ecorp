1.2.0:
	Housekeeping: tests, documentation and policy. The stack itself behaves as in 1.1.0.
	- run_tests: new command, runs the offline tests in tests/offline (helper script, spawning of config files, consistency of compose file, playbook and step files). Needs no docker or network.
	- CI runs the offline tests in every pipeline before anything else.
	- ci_ensure_diorama is listed in help.
	- purge: the help text says what it really does (.env and settings/*.yml are kept).
	- README describes the services, commands, every variable of .env, the step types, the container labels and the CI variables.
	- AGENTS.md: rules for changing this repository.
	- TODO.md lists the known problems found while reviewing the repository.
	- Files that are not scripts are no longer marked executable.

1.1.0:
	- ecorp_diorama changed to ecorp-diorama. This image will be published in dockerhub, following the name conventions.
	- devops-build-image built separately and published where: https://hub.docker.com/r/lxeu/devops-build-image
	- remove building devops-build-image from default steps and leaving a copy of the original into a storage directory ./steps/. This makes builds faster and diorama image smaller

1.0.0:
	Released with basic functionalities: coredns nameserver, dc, controller, host controller, gitlab, core-gitlab-runner with automatic self provision, registering user accounts, runner, and run a step file makes the system ready to operate.
	- wrap container, if you don't want to run directly on the host
	- ecorp_diorama image: bake whole basic infrastructure into one runnable image, so you can tradeoff build time for image size and launch a whole ecorp instance inside a container (like in wrap container but this image has a whole installed base system). This makes module testing easier in CI/CD environment
