
import React from 'react';
import { shallow } from 'enzyme';

import AnchorLink from 'src/components/AnchorLink';
import URLShortLinkButton from 'src/components/URLShortLinkButton';

describe('AnchorLink', () => {
  const props = {
    anchorLinkId: 'CHART-123',
  };

  const globalLocation = window.location;
  afterEach(() => {
    window.location = globalLocation;
  });

  beforeEach(() => {
    delete window.location;
    window.location = new URL(`https://path?#${props.anchorLinkId}`);
  });

  afterEach(() => {
    delete global.window.location.value;
  });

  it('should scroll the AnchorLink into view upon mount', async () => {
    const callback = jest.fn();
    const stub = jest.spyOn(document, 'getElementById').mockReturnValue({
      scrollIntoView: callback,
    });

    shallow(<AnchorLink {...props} />);
    await new Promise(r => setTimeout(r, 2000));

    expect(stub).toHaveBeenCalledTimes(1);
  });

  it('should render anchor link with id', () => {
    const wrapper = shallow(<AnchorLink {...props} />);
    expect(wrapper.find(`#${props.anchorLinkId}`)).toExist();
    expect(wrapper.find(URLShortLinkButton)).not.toExist();
  });

  it('should render URLShortLinkButton', () => {
    const wrapper = shallow(<AnchorLink {...props} showShortLinkButton />);
    expect(wrapper.find(URLShortLinkButton)).toExist();
    expect(wrapper.find(URLShortLinkButton)).toHaveProp({ placement: 'right' });

    const targetUrl = wrapper.find(URLShortLinkButton).prop('url');
    const hash = targetUrl.slice(targetUrl.indexOf('#') + 1);
    expect(hash).toBe(props.anchorLinkId);
  });
});
