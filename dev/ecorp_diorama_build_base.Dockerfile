FROM ecorp_wrap_base:latest
COPY . /ecorp
CMD ["/ecorp/ecorp", "inside_diorama__launch"]
