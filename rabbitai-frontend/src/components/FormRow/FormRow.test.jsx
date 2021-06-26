
import React from 'react';
import { shallow } from 'enzyme';

import { InfoTooltipWithTrigger } from '@rabbitai-ui/chart-controls';
import { Row, Col } from 'src/common/components';
import TextControl from 'src/explore/components/controls/TextControl';
import FormRow from 'src/components/FormRow';

const defaultProps = {
  label: 'Hello',
  tooltip: 'A tooltip',
  control: <TextControl label="test_cbox" />,
};

describe('FormRow', () => {
  let wrapper;

  const getWrapper = (overrideProps = {}) => {
    const props = {
      ...defaultProps,
      ...overrideProps,
    };
    return shallow(<FormRow {...props} />);
  };

  beforeEach(() => {
    wrapper = getWrapper();
  });

  it('renders an InfoTooltipWithTrigger only if needed', () => {
    expect(wrapper.find(InfoTooltipWithTrigger)).toExist();
    wrapper = getWrapper({ tooltip: null });
    expect(wrapper.find(InfoTooltipWithTrigger)).not.toExist();
  });

  it('renders a Row and 2 Cols', () => {
    expect(wrapper.find(Row)).toExist();
    expect(wrapper.find(Col)).toHaveLength(2);
  });
});
