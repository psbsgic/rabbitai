import React from 'react';
import Gravatar from 'react-gravatar';
import moment from 'moment';
import { t, styled } from '@superset-ui/core';
import { UserWithPermissionsAndRoles } from '../../types/bootstrapTypes';

interface UserInfoProps {
  user: UserWithPermissionsAndRoles;
}

const StyledContainer = styled.div`
  .panel {
    padding: ${({ theme }) => theme.gridUnit * 6}px;
  }
`;

export default function UserInfo({ user }: UserInfoProps) {
  return (
    <StyledContainer>
      <a href="https://en.gravatar.com/">
        <Gravatar
          email={user.email}
          width="100%"
          height=""
          size={220}
          alt={t('Profile picture provided by Gravatar')}
          className="img-rounded"
          style={{ borderRadius: 15 }}
        />
      </a>
      <hr />
      <div className="panel">
        <div className="header">
          <h3>
            <strong>
              {user.firstName} {user.lastName}
            </strong>
          </h3>
          <h4 className="username">
            <i className="fa fa-user-o" /> {user.username}
          </h4>
        </div>
        <hr />
        <p>
          <i className="fa fa-clock-o" /> {t('joined')}{' '}
          {moment(user.createdOn, 'YYYYMMDD').fromNow()}
        </p>
        <p className="email">
          <i className="fa fa-envelope-o" /> {user.email}
        </p>
        <p className="roles">
          <i className="fa fa-lock" /> {Object.keys(user.roles).join(', ')}
        </p>
        <p>
          <i className="fa fa-key" />
          &nbsp;
          <span className="text-muted">{t('id:')}</span>&nbsp;
          <span className="user-id">{user.userId}</span>
        </p>
      </div>
    </StyledContainer>
  );
}
