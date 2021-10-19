import React from 'react';
import { mount, shallow } from 'enzyme';
import { supersetTheme, ThemeProvider } from '@superset-ui/core';
import { Dropdown, Menu } from 'src/common/components';
import ExploreAdditionalActionsMenu from 'src/explore/components/ExploreAdditionalActionsMenu';

describe('ExploreAdditionalActionsMenu', () => {
  const defaultProps = {
    animation: false,
    queryResponse: {
      query: 'SELECT * FROM foo',
      language: 'sql',
    },
    chartStatus: 'success',
    queryEndpoint: 'localhost',
    latestQueryFormData: {
      datasource: '1__table',
    },
    chartHeight: '30px',
  };

  it('is valid', () => {
    expect(
      React.isValidElement(<ExploreAdditionalActionsMenu {...defaultProps} />),
    ).toBe(true);
  });
  it('renders a dropdown with 3 items', () => {
    const wrapper = mount(<ExploreAdditionalActionsMenu {...defaultProps} />, {
      wrappingComponent: ThemeProvider,
      wrappingComponentProps: {
        theme: supersetTheme,
      },
    });
    const dropdown = wrapper.find(Dropdown);
    const menu = shallow(<div>{dropdown.prop('overlay')}</div>);
    const menuItems = menu.find(Menu.Item);
    expect(menuItems).toHaveLength(3);
  });
});
