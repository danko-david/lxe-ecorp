# dc

`units/dc` is a Samba Active Directory domain controller. On the first start it provisions the
domain with the administrator password `DC_ADMIN_PASS`; the domain lives in the docker volume
`dc` (a volume and not a directory under `data/`, because Samba needs file ACLs that a bind mount
does not give).

It has the static address `NET_DC` and is the DNS server of every container of the
infrastructure. Names it does not know go to its forwarder, the [dns](dns.md) unit.

## Name of the domain

Everything is named after `ECORP_DNS_CORE_ZONE_NAME`, with the default `e-corp.intra.net`:

| What | Value | With the default |
| --- | --- | --- |
| Domain (Kerberos realm, DNS domain of the directory) | `ad.<zone>` | `ad.e-corp.intra.net` |
| LDAP base | the same as `DC=` parts | `DC=ad,DC=e-corp,DC=intra,DC=net` |
| Short (NetBIOS) name | first label of the zone in capitals, at most 15 characters | `E-CORP` |
| The server itself | `dc.<zone>` like every other container | `dc.e-corp.intra.net` |

The domain is a subdomain of the zone and not the zone itself, because Samba answers every DNS
request for its own domain by itself and would not forward the names of the containers to the
[dns](dns.md) unit.

An installation made before 1.2.0 has `DC_REALM` and `DC_DOMAIN` in its `.env`. They still win
over the derived names, and have to stay there: a domain cannot be renamed after it was created.

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
