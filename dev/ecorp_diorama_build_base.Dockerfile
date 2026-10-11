FROM ecorp-wrap-base:latest
COPY . /ecorp
CMD ["/ecorp/ecorp", "inside_diorama__launch"]
