import { renderHook } from '@testing-library/react-hooks';
import { useComponentDidUpdate } from './useComponentDidUpdate';

test('the effect should not be executed on the first render', () => {
  const effect = jest.fn();
  const hook = renderHook(props => useComponentDidUpdate(props.effect), {
    initialProps: { effect },
  });
  expect(effect).toBeCalledTimes(0);
  const changedEffect = jest.fn();
  hook.rerender({ effect: changedEffect });
  expect(changedEffect).toBeCalledTimes(1);
});
