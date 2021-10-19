import React from 'react';
import { mount } from 'enzyme';
import { ThemeProvider, supersetTheme } from '@superset-ui/core';

import SearchInput from 'src/components/SearchInput';

describe('SearchInput', () => {
  const defaultProps = {
    onSubmit: jest.fn(),
    onClear: jest.fn(),
    onChange: jest.fn(),
    value: '',
  };

  const factory = overrideProps => {
    const props = { ...defaultProps, ...(overrideProps || {}) };
    return mount(
      <ThemeProvider theme={supersetTheme}>
        <SearchInput {...props} />
      </ThemeProvider>,
    );
  };

  let wrapper;

  beforeAll(() => {
    wrapper = factory();
  });

  afterEach(() => {
    defaultProps.onSubmit.mockClear();
    defaultProps.onClear.mockClear();
    defaultProps.onChange.mockClear();
  });

  it('renders', () => {
    expect(React.isValidElement(<SearchInput {...defaultProps} />)).toBe(true);
  });

  const typeSearchInput = value => {
    wrapper
      .find('[data-test="search-input"]')
      .first()
      .props()
      .onChange({ currentTarget: { value } });
  };

  it('submits on enter', () => {
    typeSearchInput('foo');

    wrapper
      .find('[data-test="search-input"]')
      .first()
      .props()
      .onKeyDown({ key: 'Enter' });

    expect(defaultProps.onChange).toHaveBeenCalled();
    expect(defaultProps.onSubmit).toHaveBeenCalled();
  });

  it('submits on search icon click', () => {
    typeSearchInput('bar');

    wrapper.find('[data-test="search-submit"]').first().props().onClick();

    expect(defaultProps.onSubmit).toHaveBeenCalled();
  });

  it('clears on clear icon click', () => {
    const wrapper2 = factory({ value: 'fizz' });
    wrapper2.find('[data-test="search-clear"]').first().props().onClick();

    expect(defaultProps.onClear).toHaveBeenCalled();
  });
});
