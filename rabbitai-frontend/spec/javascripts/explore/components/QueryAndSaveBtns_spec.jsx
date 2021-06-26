
import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import sinon from 'sinon';

import QueryAndSaveButtons from 'src/explore/components/QueryAndSaveBtns';
import Button from 'src/components/Button';

describe('QueryAndSaveButtons', () => {
  const defaultProps = {
    canAdd: true,
    onQuery: sinon.spy(),
  };

  // It must render
  it('renders', () => {
    expect(
      React.isValidElement(<QueryAndSaveButtons {...defaultProps} />),
    ).toBe(true);
  });

  // Test the output
  describe('output', () => {
    const wrapper = mount(<QueryAndSaveButtons {...defaultProps} />);

    it('renders 2 buttons', () => {
      expect(wrapper.find(Button)).toHaveLength(2);
    });

    it('renders buttons with correct text', () => {
      expect(wrapper.find(Button).at(0).text().trim()).toBe('Run');
      expect(wrapper.find(Button).at(1).text().trim()).toBe('Save');
    });

    it('calls onQuery when query button is clicked', () => {
      const queryButton = wrapper
        .find('[data-test="run-query-button"]')
        .hostNodes();
      queryButton.simulate('click');
      expect(defaultProps.onQuery.called).toBe(true);
    });
  });
});
