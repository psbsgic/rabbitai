import Button, { OnClickHandler } from 'src/components/Button';
import React, { FC } from 'react';
import { styled, t } from '@superset-ui/core';

const RemovedContent = styled.div`
  display: flex;
  flex-direction: column;
  height: 400px; // arbitrary
  text-align: center;
  justify-content: center;
  align-items: center;
  color: ${({ theme }) => theme.colors.grayscale.base};
`;

type RemovedFilterProps = {
  onClick: OnClickHandler;
};

const RemovedFilter: FC<RemovedFilterProps> = ({ onClick }) => (
  <RemovedContent>
    <p>{t('You have removed this filter.')}</p>
    <div>
      <Button
        data-test="restore-filter-button"
        buttonStyle="primary"
        onClick={onClick}
      >
        {t('Restore Filter')}
      </Button>
    </div>
  </RemovedContent>
);

export default RemovedFilter;
