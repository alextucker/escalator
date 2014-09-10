from guardian.shortcuts import assign_perm


def assign_admin_perms(organization, user):
    assign_perm('edit_organization', user, organization)
    assign_perm('view_organization', user, organization)
    assign_perm('create_organization_group', user, organization)
    assign_perm('invite_organization_user', user, organization)
    organization.user_set.add(user)
