import memoizeOne from 'memoize-one';
import { UserWithPermissionsAndRoles } from 'src/types/bootstrapTypes';
import Dashboard from 'src/types/Dashboard';

type UserRoles = Record<string, [string, string][]>;

const findPermission = memoizeOne(
  (perm: string, view: string, roles?: UserRoles | null) =>
    !!roles &&
    Object.values(roles).some(permissions =>
      permissions.some(([perm_, view_]) => perm_ === perm && view_ === view),
    ),
);

export default findPermission;

// this should really be a config value,
// but is hardcoded in backend logic already, so...
const ADMIN_ROLE_NAME = 'admin';

const isUserAdmin = (user: UserWithPermissionsAndRoles) =>
  Object.keys(user.roles).some(role => role.toLowerCase() === ADMIN_ROLE_NAME);

const isUserDashboardOwner = (
  dashboard: Dashboard,
  user: UserWithPermissionsAndRoles,
) => dashboard.owners.some(owner => owner.username === user.username);

export const canUserEditDashboard = (
  dashboard: Dashboard,
  user?: UserWithPermissionsAndRoles | null,
) =>
  !!user?.roles &&
  (isUserAdmin(user) || isUserDashboardOwner(dashboard, user)) &&
  findPermission('can_write', 'Dashboard', user.roles);
