
import React from 'react';
import { shallow } from 'enzyme';
import Toast from 'src/messageToasts/components/Toast';
import ToastPresenter from 'src/messageToasts/components/ToastPresenter';

import mockMessageToasts from '../mockMessageToasts';

describe('ToastPresenter', () => {
  const props = {
    toasts: mockMessageToasts,
    removeToast() {},
  };

  function setup(overrideProps) {
    const wrapper = shallow(<ToastPresenter {...props} {...overrideProps} />);
    return wrapper;
  }

  it('should render a div with id toast-presenter', () => {
    const wrapper = setup();
    expect(wrapper.find('#toast-presenter')).toExist();
  });

  it('should render a Toast for each toast object', () => {
    const wrapper = setup();
    expect(wrapper.find(Toast)).toHaveLength(props.toasts.length);
  });

  it('should pass removeToast to the Toast component', () => {
    const removeToast = () => {};
    const wrapper = setup({ removeToast });
    expect(wrapper.find(Toast).first().prop('onCloseToast')).toBe(removeToast);
  });
});
