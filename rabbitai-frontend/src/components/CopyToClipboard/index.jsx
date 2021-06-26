
import React from 'react';
import PropTypes from 'prop-types';
import { t } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import withToasts from 'src/messageToasts/enhancers/withToasts';
import copyTextToClipboard from 'src/utils/copy';

const propTypes = {
  copyNode: PropTypes.node,
  getText: PropTypes.func,
  onCopyEnd: PropTypes.func,
  shouldShowText: PropTypes.bool,
  text: PropTypes.string,
  wrapped: PropTypes.bool,
  tooltipText: PropTypes.string,
  addDangerToast: PropTypes.func.isRequired,
  addSuccessToast: PropTypes.func.isRequired,
};

const defaultProps = {
  copyNode: <span>Copy</span>,
  onCopyEnd: () => {},
  shouldShowText: true,
  wrapped: true,
  tooltipText: t('Copy to clipboard'),
};

class CopyToClipboard extends React.Component {
  constructor(props) {
    super(props);

    // bindings
    this.copyToClipboard = this.copyToClipboard.bind(this);
    this.onClick = this.onClick.bind(this);
  }

  onClick() {
    if (this.props.getText) {
      this.props.getText(d => {
        this.copyToClipboard(d);
      });
    } else {
      this.copyToClipboard(this.props.text);
    }
  }

  getDecoratedCopyNode() {
    return React.cloneElement(this.props.copyNode, {
      style: { cursor: 'pointer' },
      onClick: this.onClick,
    });
  }

  copyToClipboard(textToCopy) {
    copyTextToClipboard(textToCopy)
      .then(() => {
        this.props.addSuccessToast(t('Copied to clipboard!'));
      })
      .catch(() => {
        this.props.addDangerToast(
          t(
            'Sorry, your browser does not support copying. Use Ctrl / Cmd + C!',
          ),
        );
      })
      .finally(() => {
        this.props.onCopyEnd();
      });
  }

  renderNotWrapped() {
    return (
      <Tooltip
        id="copy-to-clipboard-tooltip"
        placement="top"
        style={{ cursor: 'pointer' }}
        title={this.props.tooltipText}
        trigger={['hover']}
      >
        {this.getDecoratedCopyNode()}
      </Tooltip>
    );
  }

  renderLink() {
    return (
      <span css={{ display: 'inline-flex', alignItems: 'center' }}>
        {this.props.shouldShowText && this.props.text && (
          <span className="m-r-5" data-test="short-url">
            {this.props.text}
          </span>
        )}
        <Tooltip
          id="copy-to-clipboard-tooltip"
          placement="top"
          title={this.props.tooltipText}
          trigger={['hover']}
        >
          {this.getDecoratedCopyNode()}
        </Tooltip>
      </span>
    );
  }

  render() {
    const { wrapped } = this.props;
    if (!wrapped) {
      return this.renderNotWrapped();
    }
    return this.renderLink();
  }
}

export default withToasts(CopyToClipboard);

CopyToClipboard.propTypes = propTypes;
CopyToClipboard.defaultProps = defaultProps;
