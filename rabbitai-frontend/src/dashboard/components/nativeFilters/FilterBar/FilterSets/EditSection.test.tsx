
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { mockStore } from 'spec/fixtures/mockStore';
import { Provider } from 'react-redux';
import EditSection, { EditSectionProps } from './EditSection';

const createProps = () => ({
  filterSetId: 'set-id',
  dataMaskSelected: {
    DefaultsID: {
      filterState: {
        value: 'value',
      },
    },
  },
  onCancel: jest.fn(),
  disabled: false,
});

const setup = (props: EditSectionProps) => (
  <Provider store={mockStore}>
    <EditSection {...props} />
  </Provider>
);

test('should render', () => {
  const mockedProps = createProps();
  const { container } = render(setup(mockedProps));
  expect(container).toBeInTheDocument();
});

test('should render the title', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('Editing filter set:')).toBeInTheDocument();
});

test('should render the set name', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('Set name')).toBeInTheDocument();
});

test('should render a textbox', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByRole('textbox')).toBeInTheDocument();
});

test('should change the set name', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  const textbox = screen.getByRole('textbox');
  userEvent.clear(textbox);
  userEvent.type(textbox, 'New name');
  expect(textbox).toHaveValue('New name');
});

test('should render the enter icon', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByRole('img', { name: 'enter' })).toBeInTheDocument();
});

test('should render the Cancel button', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('Cancel')).toBeInTheDocument();
});

test('should cancel', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  const cancelBtn = screen.getByText('Cancel');
  expect(mockedProps.onCancel).not.toHaveBeenCalled();
  userEvent.click(cancelBtn);
  expect(mockedProps.onCancel).toHaveBeenCalled();
});

test('should render the Save button', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  expect(screen.getByText('Save')).toBeInTheDocument();
});

test('should render the Save button as disabled', () => {
  const mockedProps = createProps();
  const saveDisabledProps = {
    ...mockedProps,
    disabled: true,
  };
  render(setup(saveDisabledProps));
  expect(screen.getByText('Save').parentElement).toBeDisabled();
});
