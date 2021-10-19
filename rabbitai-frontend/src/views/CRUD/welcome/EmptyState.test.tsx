import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import EmptyState from 'src/views/CRUD/welcome/EmptyState';

describe('EmptyState', () => {
  const variants = [
    {
      tab: 'Favorite',
      tableName: 'DASHBOARDS',
    },
    {
      tab: 'Mine',
      tableName: 'DASHBOARDS',
    },
    {
      tab: 'Favorite',
      tableName: 'CHARTS',
    },
    {
      tab: 'Mine',
      tableName: 'CHARTS',
    },
    {
      tab: 'Favorite',
      tableName: 'SAVED_QUERIES',
    },
    {
      tab: 'Mine',
      tableName: 'SAVED_QUEREIS',
    },
  ];
  const recents = [
    {
      tab: 'Viewed',
      tableName: 'RECENTS',
    },
    {
      tab: 'Edited',
      tableName: 'RECENTS',
    },
    {
      tab: 'Created',
      tableName: 'RECENTS',
    },
  ];
  variants.forEach(variant => {
    it(`it renders an ${variant.tab} ${variant.tableName} empty state`, () => {
      const wrapper = mount(<EmptyState {...variant} />);
      expect(wrapper).toExist();
      const textContainer = wrapper.find('.ant-empty-description');
      expect(textContainer.text()).toEqual(
        variant.tab === 'Favorite'
          ? "You don't have any favorites yet!"
          : `No ${
              variant.tableName === 'SAVED_QUERIES'
                ? 'saved queries'
                : variant.tableName.toLowerCase()
            } yet`,
      );
      expect(wrapper.find('button')).toHaveLength(1);
    });
  });
  recents.forEach(recent => {
    it(`it renders an ${recent.tab} ${recent.tableName} empty state`, () => {
      const wrapper = mount(<EmptyState {...recent} />);
      expect(wrapper).toExist();
      const textContainer = wrapper.find('.ant-empty-description');
      expect(wrapper.find('.ant-empty-image').children()).toHaveLength(1);
      expect(textContainer.text()).toContain(
        `Recently ${recent.tab.toLowerCase()} charts, dashboards, and saved queries will appear here`,
      );
    });
  });
});
