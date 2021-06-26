
import React from 'react';
import { t, styled } from '@rabbitai-ui/core';
import { Row, Col } from 'src/common/components';
import Tabs from 'src/components/Tabs';
import { UserWithPermissionsAndRoles } from 'src/types/bootstrapTypes';
import Favorites from './Favorites';
import UserInfo from './UserInfo';
import Security from './Security';
import RecentActivity from './RecentActivity';
import CreatedContent from './CreatedContent';

interface AppProps {
  user: UserWithPermissionsAndRoles;
}

const StyledTabPane = styled(Tabs.TabPane)`
  background-color: ${({ theme }) => theme.colors.grayscale.light5};
  padding: ${({ theme }) => theme.gridUnit * 4}px;
`;

export default function App({ user }: AppProps) {
  return (
    <div className="container app">
      <Row gutter={16}>
        <Col xs={24} md={6}>
          <UserInfo user={user} />
        </Col>
        <Col xs={24} md={18}>
          <Tabs centered>
            <StyledTabPane
              key="1"
              tab={
                <div>
                  <i className="fa fa-star" /> {t('Favorites')}
                </div>
              }
            >
              <Favorites user={user} />
            </StyledTabPane>
            <StyledTabPane
              key="2"
              tab={
                <div>
                  <i className="fa fa-paint-brush" /> {t('Created content')}
                </div>
              }
            >
              <CreatedContent user={user} />
            </StyledTabPane>
            <StyledTabPane
              key="3"
              tab={
                <div>
                  <i className="fa fa-list" /> {t('Recent activity')}
                </div>
              }
            >
              <RecentActivity user={user} />
            </StyledTabPane>
            <StyledTabPane
              key="4"
              tab={
                <div>
                  <i className="fa fa-lock" /> {t('Security & Access')}
                </div>
              }
            >
              <Security user={user} />
            </StyledTabPane>
          </Tabs>
        </Col>
      </Row>
    </div>
  );
}
