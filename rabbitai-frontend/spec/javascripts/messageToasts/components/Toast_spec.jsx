import React from 'react';
import { mount } from 'enzyme';
import { ThemeProvider, supersetTheme } from '@superset-ui/core';
import Toast from 'src/messageToasts/components/Toast';
import { act } from 'react-dom/test-utils';
import mockMessageToasts from '../mockMessageToasts';

const props = {
  toast: mockMessageToasts[0],
  onCloseToast() {},
};

const setup = overrideProps =>
  mount(<Toast {...props} {...overrideProps} />, {
    wrappingComponent: ThemeProvider,
    wrappingComponentProps: { theme: supersetTheme },
  });

describe('Toast', () => {
  it('should render', () => {
    const wrapper = setup();
    expect(wrapper.find('[data-test="toast-container"]')).toExist();
  });

  it('should render toastText within the div', () => {
    const wrapper = setup();
    const container = wrapper.find('[data-test="toast-container"]');
    expect(container.hostNodes().childAt(1).text()).toBe(props.toast.text);
  });

  it('should call onCloseToast upon toast dismissal', async () =>
    act(
      () =>
        new Promise(done => {
          const onCloseToast = id => {
            expect(id).toBe(props.toast.id);
            done();
          };

          const wrapper = setup({ onCloseToast });
          wrapper.find('[data-test="close-button"]').props().onClick();
        }),
    ));
});
