from keycloak import KeycloakAdmin
import pandas as pd
import os

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL", "http://localhost:8080/auth/")
USERNAME = os.environ.get("KEYCLOAK_ADMIN_USER", "admin")
PASSWORD = os.environ.get("KEYCLOAK_ADMIN_PASSWORD", "Pa55w0rd")
REALM_NAME = os.environ.get("KEYCLOAK_REALM", "enki")

print(REALM_NAME)
print(KEYCLOAK_URL)
keycloak_admin = KeycloakAdmin(server_url=KEYCLOAK_URL,
                               username=USERNAME,
                               password=PASSWORD,
                               verify=True)
keycloak_admin.realm_name = REALM_NAME


def create_role(admin, name, description):
    return admin.create_realm_role({'name': name, 'description': description, 'clientRole': True}, skip_exists=True)


def create_roles(admin):
    roles = pd.read_csv("./roles.csv")
    for r, row in roles.where(pd.notnull(roles), None).iterrows():
        create_role(admin, row['name'], row['description'])


def create_group(admin, name, parent):
    if parent:
        found_group = keycloak_admin.get_group_by_path(f"/{parent}")
        group = admin.create_group({"name": name}, parent=found_group["id"], skip_exists=True, )

    else:
        group = admin.create_group({"name": name}, skip_exists=True, )
    return group


def assign_role_to_group(admin, group_id, roles, realm_roles):
    roles_ids = [realm_role["id"] for realm_role in realm_roles if realm_role["name"] in roles]
    return admin.assign_group_realm_roles(group_id=group_id, roles=[{"id": role_id} for role_id in roles_ids])


def create_groups(admin, realm_roles):
    groups = pd.read_csv("./groups.csv")
    for r, row in groups.where(pd.notnull(groups), None).iterrows():
        _ = create_group(admin, row["name"], row.parent)
        # found_group = admin.get_group_by_path(f"/{row['name']}")
        # roles = row["roles"].split("/")
        # assign_role_to_group(admin, found_group["id"], roles=roles, realm_roles=realm_roles)


def create_user(admin, email, password, code_commune):
    password = password or os.environ.get("DEFAULT_PASSWORD", "defaultpassword")
    new_user = admin.create_user({
                    "username": email,
                    "email": email,
                    "enabled": True,
    })
    response = admin.set_user_password(user_id=new_user, password=password, temporary=False)
    return new_user


def assign_user_group(admin, user_id, group_id):
    return admin.group_user_add(user_id, group_id)


def create_users(admin):
    users = pd.read_csv("./users_seed.csv")
    for r, row in users.where(pd.notnull(users), None).iterrows():
        user = create_user(admin, row['email'], row['password'], row['code_insee'])
        found_group = admin.get_group_by_path(f"/{row['group']}")
        assign_user_group(admin, user, found_group["id"])


create_roles(keycloak_admin)
realm_roles = keycloak_admin.get_realm_roles()
create_groups(keycloak_admin, realm_roles=realm_roles)
create_users(keycloak_admin)
