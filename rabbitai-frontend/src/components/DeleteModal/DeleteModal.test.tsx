
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import DeleteModal from '.';

test('Must display title and content', () => {
  const props = {
    title: <div data-test="test-title">Title</div>,
    description: <div data-test="test-description">Description</div>,
    onConfirm: jest.fn(),
    onHide: jest.fn(),
    open: true,
  };
  render(<DeleteModal {...props} />);
  expect(screen.getByTestId('test-title')).toBeInTheDocument();
  expect(screen.getByTestId('test-title')).toBeVisible();
  expect(screen.getByTestId('test-description')).toBeInTheDocument();
  expect(screen.getByTestId('test-description')).toBeVisible();
});

test('Calling "onHide"', () => {
  const props = {
    title: <div data-test="test-title">Title</div>,
    description: <div data-test="test-description">Description</div>,
    onConfirm: jest.fn(),
    onHide: jest.fn(),
    open: true,
  };
  render(<DeleteModal {...props} />);
  expect(props.onHide).toBeCalledTimes(0);
  expect(props.onConfirm).toBeCalledTimes(0);
  expect(screen.getByText('×')).toBeVisible();
  userEvent.click(screen.getByText('×'));
  expect(props.onHide).toBeCalledTimes(1);
  expect(props.onConfirm).toBeCalledTimes(0);
});

test('Calling "onConfirm" only after typing "delete" in the input', () => {
  const props = {
    title: <div data-test="test-title">Title</div>,
    description: <div data-test="test-description">Description</div>,
    onConfirm: jest.fn(),
    onHide: jest.fn(),
    open: true,
  };
  render(<DeleteModal {...props} />);
  expect(props.onHide).toBeCalledTimes(0);
  expect(props.onConfirm).toBeCalledTimes(0);
  expect(screen.getByTestId('delete-modal-input')).toBeVisible();
  expect(props.onConfirm).toBeCalledTimes(0);

  // do not execute "onConfirm" if you have not typed "delete"
  userEvent.click(screen.getByText('delete'));
  expect(props.onConfirm).toBeCalledTimes(0);

  // execute "onConfirm" if you have typed "delete"
  userEvent.type(screen.getByTestId('delete-modal-input'), 'delete');
  userEvent.click(screen.getByText('delete'));
  expect(props.onConfirm).toBeCalledTimes(1);
});
