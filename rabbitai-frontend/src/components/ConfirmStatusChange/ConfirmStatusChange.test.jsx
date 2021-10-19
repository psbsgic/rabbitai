import React from 'react';
import { mount } from 'enzyme';
import Button from 'src/components/Button';
import { act } from 'react-dom/test-utils';
import { supersetTheme, ThemeProvider } from '@superset-ui/core';
import ConfirmStatusChange from 'src/components/ConfirmStatusChange';
import Modal from 'src/components/Modal';

describe('ConfirmStatusChange', () => {
  const mockedProps = {
    title: 'please confirm',
    description: 'are you sure?',
    onConfirm: jest.fn(),
  };
  const wrapper = mount(
    <ConfirmStatusChange {...mockedProps}>
      {confirm => (
        <>
          <Button id="btn1" onClick={confirm} />
        </>
      )}
    </ConfirmStatusChange>,
    {
      wrappingComponent: ThemeProvider,
      wrappingComponentProps: { theme: supersetTheme },
    },
  );

  it('opens a confirm modal', () => {
    act(() => {
      wrapper.find('#btn1').first().props().onClick('foo');
    });

    wrapper.update();

    expect(wrapper.find(Modal)).toExist();
  });

  it('calls the function on confirm', () => {
    act(() => {
      wrapper.find(Button).last().props().onClick();
    });

    expect(mockedProps.onConfirm).toHaveBeenCalledWith('foo');
  });
});
