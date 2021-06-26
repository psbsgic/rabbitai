
import React from 'react';
import { styledMount as mount } from 'spec/helpers/theming';
import fetchMock from 'fetch-mock';

import ImageLoader from 'src/components/ListViewCard/ImageLoader';
import waitForComponentToPaint from 'spec/helpers/waitForComponentToPaint';

global.URL.createObjectURL = jest.fn(() => '/local_url');
const blob = new Blob([], { type: 'image/png' });

fetchMock.get(
  '/thumbnail',
  { body: blob, headers: { 'Content-Type': 'image/png' } },
  {
    sendAsJson: false,
  },
);

describe('ImageLoader', () => {
  const defaultProps = {
    src: '/thumbnail',
    fallback: '/fallback',
  };

  const factory = (extraProps = {}) => {
    const props = { ...defaultProps, ...extraProps };
    return mount(<ImageLoader {...props} />);
  };

  afterEach(fetchMock.resetHistory);

  it('is a valid element', async () => {
    const wrapper = factory();
    await waitForComponentToPaint(wrapper);
    expect(wrapper.find(ImageLoader)).toExist();
  });

  it('fetches loads the image in the background', async () => {
    const wrapper = factory();
    expect(wrapper.find('div').props().src).toBe('/fallback');
    await waitForComponentToPaint(wrapper);
    expect(fetchMock.calls(/thumbnail/)).toHaveLength(1);
    expect(global.URL.createObjectURL).toHaveBeenCalled();
    expect(wrapper.find('div').props().src).toBe('/local_url');
  });

  it('displays fallback image when response is not an image', async () => {
    fetchMock.once('/thumbnail2', {});
    const wrapper = factory({ src: '/thumbnail2' });
    expect(wrapper.find('div').props().src).toBe('/fallback');
    await waitForComponentToPaint(wrapper);
    expect(fetchMock.calls(/thumbnail2/)).toHaveLength(1);
    expect(wrapper.find('div').props().src).toBe('/fallback');
  });
});
