1.1.0:
	- ecorp_diorama changed to ecorp-diorama. This image will be published in dockerhub, following the name conventions.
	- devops-build-image built separately and published where: https://hub.docker.com/r/lxeu/devops-build-image
	- remove building devops-build-image from default steps and leaving a copy of the original into a storage directory ./steps/. This makes builds faster and diorama image smaller

1.0.0:
	Released with basic functionalities:
		coredns nameserver, dc, controller, host controller, gitlab, core-gitlab-runner with automatic self provision, registering user accounts, runner, and run a step file makes the system ready to operate.
	Extra functions:
		- wrap container, if you dont wan't to run directly on the host
		- ecorp_diorama image: bake whole basic infrastructure into one runnable image, so you can tradeoff build time for image size and launch a whole ecorp instance inside a container (like in wrap container but this image has a whole installed base system)
		This makes module tsting easier in CI/CD envionment