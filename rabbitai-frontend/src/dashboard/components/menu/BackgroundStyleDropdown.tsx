import React from 'react';
import cx from 'classnames';

import backgroundStyleOptions from 'src/dashboard/util/backgroundStyleOptions';
import PopoverDropdown, {
  OptionProps,
  OnChangeHandler,
} from 'src/components/PopoverDropdown';

interface BackgroundStyleDropdownProps {
  id: string;
  value: string;
  onChange: OnChangeHandler;
}

function renderButton(option: OptionProps) {
  return (
    <div className={cx('background-style-option', option.className)}>
      {`${option.label} background`}
    </div>
  );
}

function renderOption(option: OptionProps) {
  return (
    <div className={cx('background-style-option', option.className)}>
      {option.label}
    </div>
  );
}

export default class BackgroundStyleDropdown extends React.PureComponent<BackgroundStyleDropdownProps> {
  render() {
    const { id, value, onChange } = this.props;
    return (
      <PopoverDropdown
        id={id}
        options={backgroundStyleOptions}
        value={value}
        onChange={onChange}
        renderButton={renderButton}
        renderOption={renderOption}
      />
    );
  }
}
