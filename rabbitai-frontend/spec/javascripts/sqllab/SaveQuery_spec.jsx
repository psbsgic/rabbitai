
import React from 'react';
import { shallow } from 'enzyme';
import * as sinon from 'sinon';
import SaveQuery from 'src/SqlLab/components/SaveQuery';
import Modal from 'src/components/Modal';
import Button from 'src/components/Button';
import { FormItem } from 'src/components/Form';

describe('SavedQuery', () => {
  const mockedProps = {
    query: {
      dbId: 1,
      schema: 'main',
      sql: 'SELECT * FROM t',
    },
    defaultLabel: 'untitled',
    animation: false,
  };
  it('is valid', () => {
    expect(React.isValidElement(<SaveQuery />)).toBe(true);
  });
  it('is valid with props', () => {
    expect(React.isValidElement(<SaveQuery {...mockedProps} />)).toBe(true);
  });
  it('has a Modal', () => {
    const wrapper = shallow(<SaveQuery {...mockedProps} />);
    expect(wrapper.find(Modal)).toExist();
  });
  // TODO: eschutho convert test to RTL
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip('has a cancel button', () => {
    const wrapper = shallow(<SaveQuery {...mockedProps} />);
    const modal = wrapper.find(Modal);

    expect(modal.find('[data-test="cancel-query"]')).toHaveLength(1);
  });
  it('has 2 FormItem', () => {
    const wrapper = shallow(<SaveQuery {...mockedProps} />);
    const modal = wrapper.find(Modal);

    expect(modal.find(FormItem)).toHaveLength(2);
  });
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip('has a save button if this is a new query', () => {
    const saveSpy = sinon.spy();
    const wrapper = shallow(<SaveQuery {...mockedProps} onSave={saveSpy} />);
    const modal = wrapper.find(Modal);

    expect(modal.find(Button)).toHaveLength(2);
    modal.find(Button).at(0).simulate('click');
    expect(saveSpy.calledOnce).toBe(true);
  });
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip('has an update button if this is an existing query', () => {
    const updateSpy = sinon.spy();
    const props = {
      ...mockedProps,
      query: {
        ...mockedProps.query,
        remoteId: '42',
      },
    };
    const wrapper = shallow(<SaveQuery {...props} onUpdate={updateSpy} />);
    const modal = wrapper.find(Modal);

    expect(modal.find(Button)).toHaveLength(3);
    modal.find(Button).at(0).simulate('click');
    expect(updateSpy.calledOnce).toBe(true);
  });
});
