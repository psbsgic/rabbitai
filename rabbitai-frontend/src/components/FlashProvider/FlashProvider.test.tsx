

import { render, screen } from 'spec/helpers/testing-library';
import React from 'react';
import { Provider } from 'react-redux';
import { store } from 'src/views/store';
import FlashProvider, { FlashMessage } from './index';

test('Rerendering correctly with default props', () => {
  const messages: FlashMessage[] = [];
  render(
    <Provider store={store}>
      <FlashProvider messages={messages}>
        <div data-test="my-component">My Component</div>
      </FlashProvider>
    </Provider>,
  );
  expect(screen.getByTestId('my-component')).toBeInTheDocument();
});

test('messages should only be inserted in the State when the component is mounted', () => {
  const messages: FlashMessage[] = [
    ['info', 'teste message 01'],
    ['info', 'teste message 02'],
  ];
  expect(store.getState().messageToasts).toEqual([]);
  const { rerender } = render(
    <Provider store={store}>
      <FlashProvider messages={messages}>
        <div data-teste="my-component">My Component</div>
      </FlashProvider>
    </Provider>,
  );
  const fistRender = store.getState().messageToasts;
  expect(fistRender).toHaveLength(2);
  expect(fistRender[1].text).toBe(messages[0][1]);
  expect(fistRender[0].text).toBe(messages[1][1]);

  rerender(
    <Provider store={store}>
      <FlashProvider messages={[...messages, ['info', 'teste message 03']]}>
        <div data-teste="my-component">My Component</div>
      </FlashProvider>
    </Provider>,
  );

  const secondRender = store.getState().messageToasts;
  expect(secondRender).toEqual(fistRender);
});
