import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import PopoverDropdown, {
  PopoverDropdownProps,
  OptionProps,
} from 'src/components/PopoverDropdown';

const defaultProps: PopoverDropdownProps = {
  id: 'popover-dropdown',
  options: [
    { label: 'Option 1', value: '1' },
    { label: 'Option 2', value: '2' },
  ],
  value: '1',
  renderButton: (option: OptionProps) => <span>{option.label}</span>,
  renderOption: (option: OptionProps) => <div>{option.label}</div>,
  onChange: jest.fn(),
};

test('renders with default props', () => {
  render(<PopoverDropdown {...defaultProps} />);
  expect(screen.getByRole('button')).toBeInTheDocument();
  expect(screen.getByRole('button')).toHaveTextContent('Option 1');
});

test('renders the menu on click', () => {
  render(<PopoverDropdown {...defaultProps} />);
  userEvent.click(screen.getByRole('button'));
  expect(screen.getByRole('menu')).toBeInTheDocument();
});

test('renders with custom button', () => {
  render(
    <PopoverDropdown
      {...defaultProps}
      renderButton={({ label, value }: OptionProps) => (
        <button type="button" key={value}>
          {`Custom ${label}`}
        </button>
      )}
    />,
  );
  expect(screen.getByText('Custom Option 1')).toBeInTheDocument();
});

test('renders with custom option', () => {
  render(
    <PopoverDropdown
      {...defaultProps}
      renderOption={({ label, value }: OptionProps) => (
        <button type="button" key={value}>
          {`Custom ${label}`}
        </button>
      )}
    />,
  );
  userEvent.click(screen.getByRole('button'));
  expect(screen.getByText('Custom Option 1')).toBeInTheDocument();
});

test('triggers onChange', () => {
  render(<PopoverDropdown {...defaultProps} />);
  userEvent.click(screen.getByRole('button'));
  expect(screen.getByText('Option 2')).toBeInTheDocument();
  userEvent.click(screen.getByText('Option 2'));
  expect(defaultProps.onChange).toHaveBeenCalled();
});
