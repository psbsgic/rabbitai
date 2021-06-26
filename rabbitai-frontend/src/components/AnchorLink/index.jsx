
import React from 'react';
import PropTypes from 'prop-types';
import { t } from '@rabbitai-ui/core';

import URLShortLinkButton from 'src/components/URLShortLinkButton';
import getDashboardUrl from 'src/dashboard/util/getDashboardUrl';
import getLocationHash from 'src/dashboard/util/getLocationHash';

const propTypes = {
  anchorLinkId: PropTypes.string.isRequired,
  filters: PropTypes.object,
  showShortLinkButton: PropTypes.bool,
  inFocus: PropTypes.bool,
  placement: PropTypes.oneOf(['right', 'left', 'top', 'bottom']),
};

const defaultProps = {
  inFocus: false,
  showShortLinkButton: false,
  placement: 'right',
  filters: {},
};

class AnchorLink extends React.PureComponent {
  componentDidMount() {
    const hash = getLocationHash();
    const { anchorLinkId } = this.props;

    if (hash && anchorLinkId === hash) {
      this.scrollToView();
    }
  }

  UNSAFE_componentWillReceiveProps(nextProps) {
    const { inFocus = false } = nextProps;
    if (inFocus) {
      this.scrollToView();
    }
  }

  scrollToView(delay = 0) {
    const { anchorLinkId } = this.props;
    const directLinkComponent = document.getElementById(anchorLinkId);
    if (directLinkComponent) {
      setTimeout(() => {
        directLinkComponent.scrollIntoView({
          block: 'center',
          behavior: 'smooth',
        });
      }, delay);
    }
  }

  render() {
    const {
      anchorLinkId,
      filters,
      showShortLinkButton,
      placement,
    } = this.props;
    return (
      <span className="anchor-link-container" id={anchorLinkId}>
        {showShortLinkButton && (
          <URLShortLinkButton
            url={getDashboardUrl(
              window.location.pathname,
              filters,
              anchorLinkId,
            )}
            emailSubject={t('Rabbitai chart')}
            emailContent={t('Check out this chart in dashboard:')}
            placement={placement}
          />
        )}
      </span>
    );
  }
}

AnchorLink.propTypes = propTypes;
AnchorLink.defaultProps = defaultProps;

export default AnchorLink;
