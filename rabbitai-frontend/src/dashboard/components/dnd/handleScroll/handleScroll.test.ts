
import handleScroll from '.';

jest.useFakeTimers();

const { scroll } = window;

afterAll(() => {
  window.scroll = scroll;
});

test('calling: "NOT_SCROLL_TOP" ,"SCROLL_TOP", "NOT_SCROLL_TOP"', () => {
  window.scroll = jest.fn();
  document.documentElement.scrollTop = 500;

  handleScroll('NOT_SCROLL_TOP');

  expect(clearInterval).not.toBeCalled();

  handleScroll('SCROLL_TOP');

  handleScroll('NOT_SCROLL_TOP');
  expect(clearInterval).toHaveBeenCalledWith(expect.any(Number));
});
