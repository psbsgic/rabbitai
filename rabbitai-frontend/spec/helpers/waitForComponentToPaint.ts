import { ReactWrapper } from 'enzyme';
import { act } from 'react-dom/test-utils';

// taken from: https://github.com/enzymejs/enzyme/issues/2073
// There is currently and issue with enzyme and react-16's hooks
// that results in a race condition between tests and react hook updates.
// This function ensures tests run after all react updates are done.
export default async function waitForComponentToPaint<P = {}>(
  wrapper: ReactWrapper<P>,
  amount = 0,
) {
  await act(async () => {
    await new Promise(resolve => setTimeout(resolve, amount));
    wrapper.update();
  });
}
