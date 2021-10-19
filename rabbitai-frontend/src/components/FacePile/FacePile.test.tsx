import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';

import { Avatar } from 'src/common/components';
import FacePile from '.';
import { getRandomColor } from './utils';

const users = [...new Array(10)].map((_, i) => ({
  first_name: 'user',
  last_name: `${i}`,
  id: i,
}));

describe('FacePile', () => {
  const wrapper = mount(<FacePile users={users} />);

  it('is a valid element', () => {
    expect(wrapper.find(FacePile)).toExist();
  });

  it('renders an Avatar', () => {
    expect(wrapper.find(Avatar)).toExist();
  });

  it('hides overflow', () => {
    expect(wrapper.find(Avatar).length).toBe(5);
  });
});

describe('utils', () => {
  describe('getRandomColor', () => {
    const colors = ['color1', 'color2', 'color3'];

    it('produces the same color for the same input values', () => {
      const name = 'foo';
      expect(getRandomColor(name, colors)).toEqual(
        getRandomColor(name, colors),
      );
    });

    it('produces a different color for different input values', () => {
      expect(getRandomColor('foo', colors)).not.toEqual(
        getRandomColor('bar', colors),
      );
    });

    it('handles non-ascii input values', () => {
      expect(getRandomColor('泰', colors)).toMatchInlineSnapshot(`"color1"`);
      expect(getRandomColor('مُحَمَّد‎', colors)).toMatchInlineSnapshot(
        `"color2"`,
      );
    });
  });
});
