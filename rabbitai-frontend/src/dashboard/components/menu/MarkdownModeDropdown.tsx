import React from 'react';
import { t } from '@superset-ui/core';

import PopoverDropdown, {
  OnChangeHandler,
} from 'src/components/PopoverDropdown';

interface MarkdownModeDropdownProps {
  id: string;
  value: string;
  onChange: OnChangeHandler;
}

const dropdownOptions = [
  {
    value: 'edit',
    label: t('Edit'),
  },
  {
    value: 'preview',
    label: t('Preview'),
  },
];

export default class MarkdownModeDropdown extends React.PureComponent<MarkdownModeDropdownProps> {
  render() {
    const { id, value, onChange } = this.props;

    return (
      <PopoverDropdown
        id={id}
        options={dropdownOptions}
        value={value}
        onChange={onChange}
      />
    );
  }
}
