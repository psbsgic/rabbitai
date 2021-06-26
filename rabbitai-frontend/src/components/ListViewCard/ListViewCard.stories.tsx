
import React from 'react';
import { action } from '@storybook/addon-actions';
import { withKnobs, boolean, select, text } from '@storybook/addon-knobs';
import DashboardImg from 'images/dashboard-card-fallback.svg';
import ChartImg from 'images/chart-card-fallback.svg';
import { Dropdown, Menu } from 'src/common/components';
import Icon from 'src/components/Icon';
import Icons from 'src/components/Icons';
import FaveStar from 'src/components/FaveStar';
import ListViewCard from '.';

export default {
  title: 'ListViewCard',
  component: ListViewCard,
  decorators: [withKnobs],
};

const imgFallbackKnob = {
  label: 'Fallback/Loading Image',
  options: {
    Dashboard: DashboardImg,
    Chart: ChartImg,
  },
  defaultValue: DashboardImg,
};

export const RabbitaiListViewCard = () => (
  <ListViewCard
    title="Rabbitai Card Title"
    loading={boolean('loading', false)}
    url="/rabbitai/dashboard/births/"
    imgURL={text('imgURL', 'https://picsum.photos/800/600')}
    imgFallbackURL={select(
      imgFallbackKnob.label,
      imgFallbackKnob.options,
      imgFallbackKnob.defaultValue,
    )}
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
    coverLeft="Left Section"
    coverRight="Right Section"
    actions={
      <ListViewCard.Actions>
        <FaveStar
          itemId={0}
          fetchFaveStar={action('fetchFaveStar')}
          saveFaveStar={action('saveFaveStar')}
          isStarred={boolean('isStarred', false)}
        />
        <Dropdown
          overlay={
            <Menu>
              <Menu.Item role="button" tabIndex={0} onClick={action('Delete')}>
                <Icons.Trash /> Delete
              </Menu.Item>
              <Menu.Item role="button" tabIndex={0} onClick={action('Edit')}>
                <Icons.EditAlt /> Edit
              </Menu.Item>
            </Menu>
          }
        >
          <Icon name="more-horiz" />
        </Dropdown>
      </ListViewCard.Actions>
    }
  />
);
