import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { mockStore } from 'spec/fixtures/mockStore';
import { Provider } from 'react-redux';
import userEvent from '@testing-library/user-event';
import FilterSetUnit, { FilterSetUnitProps } from './FilterSetUnit';

const createProps = () => ({
  editMode: true,
  setFilterSetName: jest.fn(),
  onDelete: jest.fn(),
  onEdit: jest.fn(),
  onRebuild: jest.fn(),
});

function openDropdown() {
  const dropdownIcon = screen.getByRole('img', { name: 'ellipsis' });
  userEvent.click(dropdownIcon);
}

const setup = (props: FilterSetUnitProps) => (
  <Provider store={mockStore}>
    <FilterSetUnit {...props} />
  </Provider>
);

test('should render', () => {
  const mockedProps = createProps();
  const { container } = render(setup(mockedProps));
  expect(container).toBeInTheDocument();
});

test('should render the edit button', () => {
  const mockedProps = createProps();
  const editModeOffProps = {
    ...mockedProps,
    editMode: false,
  };
  render(setup(editModeOffProps));
  expect(screen.getByRole('button', { name: 'Edit' })).toBeInTheDocument();
});

test('should render the menu', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  openDropdown();
  expect(screen.getByRole('menu')).toBeInTheDocument();
  expect(screen.getAllByRole('menuitem')).toHaveLength(3);
  expect(screen.getByText('Edit')).toBeInTheDocument();
  expect(screen.getByText('Rebuild')).toBeInTheDocument();
  expect(screen.getByText('Delete')).toBeInTheDocument();
});

test('should edit', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  openDropdown();
  const editBtn = screen.getByText('Edit');
  expect(mockedProps.onEdit).not.toHaveBeenCalled();
  userEvent.click(editBtn);
  expect(mockedProps.onEdit).toHaveBeenCalled();
});

test('should delete', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  openDropdown();
  const deleteBtn = screen.getByText('Delete');
  expect(mockedProps.onDelete).not.toHaveBeenCalled();
  userEvent.click(deleteBtn);
  expect(mockedProps.onDelete).toHaveBeenCalled();
});

test('should rebuild', () => {
  const mockedProps = createProps();
  render(setup(mockedProps));
  openDropdown();
  const rebuildBtn = screen.getByText('Rebuild');
  expect(mockedProps.onRebuild).not.toHaveBeenCalled();
  userEvent.click(rebuildBtn);
  expect(mockedProps.onRebuild).toHaveBeenCalled();
});
