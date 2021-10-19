import React from 'react';
import Badge from 'src/components/Badge';
import { t } from '@superset-ui/core';

import Label from 'src/components/Label';
import { UserWithPermissionsAndRoles } from '../../types/bootstrapTypes';

interface SecurityProps {
  user: UserWithPermissionsAndRoles;
}

export default function Security({ user }: SecurityProps) {
  return (
    <div>
      <div className="roles">
        <h4>
          {t('Roles')} <Badge count={Object.keys(user.roles).length} showZero />
        </h4>
        {Object.keys(user.roles).map(role => (
          <Label key={role}>{role}</Label>
        ))}
        <hr />
      </div>
      <div className="databases">
        {user.permissions.database_access && (
          <div>
            <h4>
              {t('Databases')}{' '}
              <Badge count={user.permissions.database_access.length} showZero />
            </h4>
            {user.permissions.database_access.map(role => (
              <Label key={role}>{role}</Label>
            ))}
            <hr />
          </div>
        )}
      </div>
      <div className="datasources">
        {user.permissions.datasource_access && (
          <div>
            <h4>
              {t('Datasets')}{' '}
              <Badge
                count={user.permissions.datasource_access.length}
                showZero
              />
            </h4>
            {user.permissions.datasource_access.map(role => (
              <Label key={role}>{role}</Label>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
