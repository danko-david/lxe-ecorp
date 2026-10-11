# dc

`units/dc` is a Samba Active Directory domain controller. On the first start it provisions the
domain from `DC_REALM`, `DC_DOMAIN` and `DC_ADMIN_PASS`; the domain lives in the docker volume
`dc` (a volume and not a directory under `data/`, because Samba needs file ACLs that a bind mount
does not give).

It has the static address `NET_DC` and is the DNS server of every container of the
infrastructure. Names it does not know go to its forwarder, the [dns](dns.md) unit.

## Users and roles

`settings/ad-users.yml` is imported by provisioning when the file changed:

```yaml
ad_users:
  - user: tcolby
    password: password
    given_name: Terry
    surname: Colby
    title: Chief Technology Officer
    roles:
      - cto
      - admin
```

- Every role becomes a group, every user is created (or gets its password set again), enabled
  and added to the groups of its roles. `email` defaults to `<user>@<ECORP_DNS_CORE_ZONE_NAME>`.
- Nothing is removed: a user or role deleted from the file stays in the domain.
- Password complexity and password expiry are switched off in the domain, this is a lab.

Users can log in to GitLab with their domain user name and password. GitLab CE does not
synchronise groups from LDAP, so the roles are not visible there.

To look into the domain: `docker exec ecorp-dc-1 samba-tool user list`, or the *AD Users* page
of the management web interface.
