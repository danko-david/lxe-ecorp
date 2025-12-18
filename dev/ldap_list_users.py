#!/usr/bin/python3

import os
from ldap3 import Server, Connection, SAFE_SYNC, ALL, SUBTREE, ANONYMOUS

# Configuration - It's recommended to use environment variables for sensitive data
# For a quick script, we'll use placeholders. Replace with actual values or environment variables.
LDAP_SERVER = os.getenv('LDAP_SERVER', 'localhost')
LDAP_PORT = int(os.getenv('LDAP_PORT', '389'))  # Use 636 for LDAPS
LDAP_SSL = bool(os.getenv('LDAP_SSL', "")) # use SSL
LDAP_BIND_DN = os.getenv('LDAP_BIND_DN', 'cn=admin,dc=example,dc=org') # Example: 'cn=admin,dc=yourdomain,dc=com'
LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD', 'adminpassword') # Replace with actual password
LDAP_SEARCH_BASE = os.getenv('LDAP_SEARCH_BASE', 'dc=example,dc=org') # Example: 'dc=yourdomain,dc=com'
LDAP_USER_FILTER = os.getenv('LDAP_USER_FILTER', '(objectClass=user)') # Common for OpenLDAP: (objectClass=person), for AD: (objectClass=user)
LDAP_ATTRIBUTES = ['sAMAccountName', 'displayName'] # Common attributes to fetch

def list_ldap_users():
    """
    Connects to an LDAP server, binds, and lists all user objects.
    """
    server = Server(LDAP_SERVER, port=LDAP_PORT, use_ssl=LDAP_SSL, get_info=ALL)
    conn = None
    try:
        # Establish connection
        conn = Connection(server,
                          user=LDAP_BIND_DN,
                          password=LDAP_BIND_PASSWORD,
                          auto_bind=True,
                          client_strategy=SAFE_SYNC,
                          read_only=True)

        if not conn.bound:
            print(f"Error: Could not bind to LDAP server as {LDAP_BIND_DN}")
            return

        print(f"Successfully connected and bound to LDAP server: {LDAP_SERVER}")
        print(f"Searching for users under base DN: {LDAP_SEARCH_BASE} with filter: {LDAP_USER_FILTER}")

        # Perform the search
        conn.search(search_base=LDAP_SEARCH_BASE,
                    search_filter=LDAP_USER_FILTER,
                    search_scope=SUBTREE,
                    attributes=LDAP_ATTRIBUTES)

        if conn.entries:
            print(f"\nFound {len(conn.entries)} user(s):")
            for entry in conn.entries:
                print("-" * 30)
                print(f"DN: {entry.entry_dn}")
                for attr in LDAP_ATTRIBUTES:
                    if attr in entry:
                        print(f"  {attr}: {entry[attr]}")
        else:
            print("No users found matching the criteria.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn and conn.bound:
            conn.unbind()
            print("Connection unbound.")

if __name__ == "__main__":
    print("Attempting to list LDAP users...")
    list_ldap_users()