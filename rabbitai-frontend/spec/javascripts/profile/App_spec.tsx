import React from 'react';
import { Row, Col } from 'src/common/components';
import { shallow } from 'enzyme';
import App from 'src/profile/components/App';

import { user } from './fixtures';

describe('App', () => {
  const mockedProps = {
    user,
  };
  it('is valid', () => {
    expect(React.isValidElement(<App {...mockedProps} />)).toBe(true);
  });

  it('renders 2 Col', () => {
    const wrapper = shallow(<App {...mockedProps} />);
    expect(wrapper.find(Row)).toExist();
    expect(wrapper.find(Col)).toHaveLength(2);
  });

  it('renders 4 Tabs', () => {
    const wrapper = shallow(<App {...mockedProps} />);
    expect(wrapper.find('[tab]')).toHaveLength(4);
  });
});
