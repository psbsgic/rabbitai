import React from 'react';
import { shallow } from 'enzyme';
import fetchMock from 'fetch-mock';
import Select from 'src/components/Select';
import AsyncSelect from 'src/components/AsyncSelect';

describe('AsyncSelect', () => {
  afterAll(fetchMock.reset);
  afterEach(fetchMock.resetHistory);

  const dataEndpoint = '/chart/api/read';
  const dataGlob = 'glob:*/chart/api/read';
  fetchMock.get(dataGlob, []);
  fetchMock.resetHistory();

  const mockedProps = {
    dataEndpoint,
    onChange: () => {},
    placeholder: 'Select...',
    mutator: () => [
      { value: 1, label: 'main' },
      { value: 2, label: 'another' },
    ],
    valueRenderer: opt => opt.label,
  };

  it('is valid element', () => {
    expect(React.isValidElement(<AsyncSelect {...mockedProps} />)).toBe(true);
  });

  it('has one select', () => {
    const wrapper = shallow(<AsyncSelect {...mockedProps} />);
    expect(wrapper.find(Select)).toExist();
  });

  it('calls onChange on select change', () => {
    const onChangeSpy = jest.fn();
    const wrapper = shallow(
      <AsyncSelect {...mockedProps} onChange={onChangeSpy} />,
    );

    wrapper.find(Select).simulate('change', { value: 1 });
    expect(onChangeSpy.mock.calls).toHaveLength(1);
  });

  describe('auto select', () => {
    it('should not call onChange if autoSelect=false', () =>
      new Promise(done => {
        expect.assertions(2);

        const onChangeSpy = jest.fn();
        shallow(<AsyncSelect {...mockedProps} onChange={onChangeSpy} />);

        setTimeout(() => {
          expect(fetchMock.calls(dataGlob)).toHaveLength(1);
          expect(onChangeSpy.mock.calls).toHaveLength(0);
          done();
        });
      }));

    it('should auto select the first option if autoSelect=true', () =>
      new Promise(done => {
        expect.assertions(3);

        const onChangeSpy = jest.fn();
        const wrapper = shallow(
          <AsyncSelect {...mockedProps} onChange={onChangeSpy} autoSelect />,
        );

        setTimeout(() => {
          expect(fetchMock.calls(dataGlob)).toHaveLength(1);
          expect(onChangeSpy.mock.calls).toHaveLength(1);
          expect(onChangeSpy).toBeCalledWith(
            wrapper.instance().state.options[0],
          );
          done();
        });
      }));

    it('should not auto select when value prop is set and autoSelect=true', () =>
      new Promise(done => {
        expect.assertions(3);

        const onChangeSpy = jest.fn();
        const wrapper = shallow(
          <AsyncSelect
            {...mockedProps}
            value={2}
            onChange={onChangeSpy}
            autoSelect
          />,
        );

        setTimeout(() => {
          expect(fetchMock.calls(dataGlob)).toHaveLength(1);
          expect(onChangeSpy.mock.calls).toHaveLength(0);
          expect(wrapper.find(Select)).toExist();
          done();
        });
      }));

    it('should call onAsyncError if there is an error fetching options', () => {
      expect.assertions(3);

      const errorEndpoint = 'async/error/';
      const errorGlob = 'glob:*async/error/';
      fetchMock.get(errorGlob, { throws: 'error' });

      const onAsyncError = jest.fn();
      const wrapper = shallow(
        <AsyncSelect
          {...mockedProps}
          dataEndpoint={errorEndpoint}
          onAsyncError={onAsyncError}
        />,
      );

      return wrapper
        .instance()
        .fetchOptions()
        .then(() => {
          // Fails then retries thrice whenever fetching options, which happens twice:
          // once on component mount and once when calling `fetchOptions` again
          expect(fetchMock.calls(errorGlob)).toHaveLength(8);
          expect(onAsyncError.mock.calls).toHaveLength(2);
          expect(onAsyncError).toBeCalledWith('error');

          return Promise.resolve();
        });
    });
  });
});
