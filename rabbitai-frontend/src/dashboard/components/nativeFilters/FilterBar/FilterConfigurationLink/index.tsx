import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setFilterConfiguration } from 'src/dashboard/actions/nativeFilters';
import Button from 'src/components/Button';
import { styled } from '@superset-ui/core';
import { FilterConfiguration } from 'src/dashboard/components/nativeFilters/types';
import { FiltersConfigModal } from 'src/dashboard/components/nativeFilters/FiltersConfigModal/FiltersConfigModal';
import { getFilterBarTestId } from '..';

export interface FCBProps {
  createNewOnOpen?: boolean;
}

const HeaderButton = styled(Button)`
  padding: 0;
`;

export const FilterConfigurationLink: React.FC<FCBProps> = ({
  createNewOnOpen,
  children,
}) => {
  const dispatch = useDispatch();
  const [isOpen, setOpen] = useState(false);

  function close() {
    setOpen(false);
  }

  async function submit(filterConfig: FilterConfiguration) {
    dispatch(await setFilterConfiguration(filterConfig));
    close();
  }

  return (
    <>
      {/* eslint-disable-next-line jsx-a11y/no-static-element-interactions */}
      <HeaderButton
        {...getFilterBarTestId('create-filter')}
        buttonStyle="link"
        buttonSize="xsmall"
        onClick={() => setOpen(true)}
      >
        {children}
      </HeaderButton>
      <FiltersConfigModal
        isOpen={isOpen}
        onSave={submit}
        onCancel={close}
        createNewOnOpen={createNewOnOpen}
      />
    </>
  );
};

export default FilterConfigurationLink;
