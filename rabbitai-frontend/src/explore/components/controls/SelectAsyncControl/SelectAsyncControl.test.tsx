
import userEvent from '@testing-library/user-event';
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import SelectAsyncControl from '.';

jest.mock('src/components/AsyncSelect', () => ({
  __esModule: true,
  default: (props: any) => (
    <div
      data-test="select-test"
      data-data-endpoint={props.dataEndpoint}
      data-value={JSON.stringify(props.value)}
      data-placeholder={props.placeholder}
      data-multi={props.multi ? 'true' : 'false'}
    >
      <button
        type="button"
        onClick={() => props.onChange(props.multi ? [] : {})}
      >
        onChange
      </button>
      <button type="button" onClick={() => props.mutator()}>
        mutator
      </button>

      <div data-test="valueRenderer">
        {props.valueRenderer({ label: 'valueRenderer' })}
      </div>
    </div>
  ),
}));

const createProps = () => ({
  value: [],
  dataEndpoint: 'api/v1/dataset/related/owners',
  multi: true,
  onAsyncErrorMessage: 'Error while fetching data',
  placeholder: 'Select ...',
  onChange: jest.fn(),
  mutator: jest.fn(),
});

beforeEach(() => {
  jest.resetAllMocks();
});

test('Should render', () => {
  const props = createProps();
  render(<SelectAsyncControl {...props} />, { useRedux: true });
  expect(screen.getByTestId('SelectAsyncControl')).toBeInTheDocument();
});

test('Should send correct props to AsyncSelect component - value props', () => {
  const props = createProps();
  render(<SelectAsyncControl {...props} />, { useRedux: true });

  expect(screen.getByTestId('select-test')).toHaveAttribute(
    'data-data-endpoint',
    props.dataEndpoint,
  );
  expect(screen.getByTestId('select-test')).toHaveAttribute(
    'data-value',
    JSON.stringify(props.value),
  );
  expect(screen.getByTestId('select-test')).toHaveAttribute(
    'data-placeholder',
    props.placeholder,
  );
  expect(screen.getByTestId('select-test')).toHaveAttribute(
    'data-multi',
    'true',
  );
  expect(screen.getByTestId('valueRenderer')).toHaveTextContent(
    'valueRenderer',
  );
});

test('Should send correct props to AsyncSelect component - function onChange multi:true', () => {
  const props = createProps();
  render(<SelectAsyncControl {...props} />, { useRedux: true });
  expect(props.onChange).toBeCalledTimes(0);
  userEvent.click(screen.getByText('onChange'));
  expect(props.onChange).toBeCalledTimes(1);
});

test('Should send correct props to AsyncSelect component - function onChange multi:false', () => {
  const props = createProps();
  render(<SelectAsyncControl {...{ ...props, multi: false }} />, {
    useRedux: true,
  });
  expect(props.onChange).toBeCalledTimes(0);
  userEvent.click(screen.getByText('onChange'));
  expect(props.onChange).toBeCalledTimes(1);
});
