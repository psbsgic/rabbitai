
import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { mount, shallow } from 'enzyme';

import HighlightedSql from 'src/SqlLab/components/HighlightedSql';
import ModalTrigger from 'src/components/ModalTrigger';
import { rabbitaiTheme, ThemeProvider } from '@rabbitai-ui/core';

describe('HighlightedSql', () => {
  const sql =
    "SELECT * FROM test WHERE something='fkldasjfklajdslfkjadlskfjkldasjfkladsjfkdjsa'";
  it('renders with props', () => {
    expect(React.isValidElement(<HighlightedSql sql={sql} />)).toBe(true);
  });
  it('renders a ModalTrigger', () => {
    const wrapper = shallow(<HighlightedSql sql={sql} />);
    expect(wrapper.find(ModalTrigger)).toExist();
  });
  it('renders a ModalTrigger while using shrink', () => {
    const wrapper = shallow(<HighlightedSql sql={sql} shrink maxWidth={20} />);
    expect(wrapper.find(ModalTrigger)).toExist();
  });
  it('renders two SyntaxHighlighter in modal', () => {
    const wrapper = mount(
      <HighlightedSql
        sql={sql}
        rawSql="SELECT * FORM foo"
        shrink
        maxWidth={5}
      />,
      {
        wrappingComponent: ThemeProvider,
        wrappingComponentProps: {
          theme: rabbitaiTheme,
        },
      },
    );
    const pre = wrapper.find('pre');
    expect(pre).toHaveLength(1);
    pre.simulate('click');
    setTimeout(() => {
      const modalBody = mount(wrapper.state().modalBody);
      expect(modalBody.find(SyntaxHighlighter)).toHaveLength(2);
    }, 10);
  });
});
