def assign_role_group(group_name, new_users, members=[]):
    for user in new_users:
        if user not in members:
            members.append(user)
    
    return {
        "group": group_name,
        "members": members,
        "count": len(members)
    }

admin_group = assign_role_group("Administrators", ["alice", "bob"])
editor_group = assign_role_group("Editors", ["charlie"])
viewer_group = assign_role_group("Viewers", ["dave", "alice"])

print(admin_group)
print(editor_group)
print(viewer_group)
