
import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import fetchMock from 'fetch-mock';

import ListViewCard from 'src/components/ListViewCard';
import ImageLoader from 'src/components/ListViewCard/ImageLoader';
import waitForComponentToPaint from 'spec/helpers/waitForComponentToPaint';

global.URL.createObjectURL = jest.fn(() => '/local_url');
fetchMock.get('/thumbnail', { body: new Blob(), sendAsJson: false });

describe('ListViewCard', () => {
  const defaultProps = {
    title: 'Card Title',
    loading: false,
    url: '/card-url',
    imgURL: '/thumbnail',
    imgFallbackURL: '/fallback',
    description: 'Card Description',
    coverLeft: 'Left Text',
    coverRight: 'Right Text',
    actions: (
      <ListViewCard.Actions>
        <div>Action 1</div>
        <div>Action 2</div>
      </ListViewCard.Actions>
    ),
  };

  let wrapper;
  const factory = (extraProps = {}) => {
    const props = { ...defaultProps, ...extraProps };
    return mount(<ListViewCard {...props} />);
  };
  beforeEach(async () => {
    wrapper = factory();
    await waitForComponentToPaint(wrapper);
  });

  it('is a valid element', () => {
    expect(wrapper.find(ListViewCard)).toExist();
  });

  it('renders Actions', () => {
    expect(wrapper.find(ListViewCard.Actions)).toExist();
  });

  it('renders and ImageLoader', () => {
    expect(wrapper.find(ImageLoader)).toExist();
  });
});
