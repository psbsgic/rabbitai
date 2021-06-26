
import React from 'react';
import PropTypes from 'prop-types';
import { TextArea } from 'src/common/components';
import { debounce } from 'lodash';
import { t } from '@rabbitai-ui/core';

import { FAST_DEBOUNCE } from 'src/constants';
import Button from 'src/components/Button';
import { TextAreaEditor } from 'src/components/AsyncAceEditor';
import ModalTrigger from 'src/components/ModalTrigger';

import ControlHeader from 'src/explore/components/ControlHeader';

const propTypes = {
  name: PropTypes.string,
  onChange: PropTypes.func,
  value: PropTypes.string,
  height: PropTypes.number,
  minLines: PropTypes.number,
  maxLines: PropTypes.number,
  offerEditInModal: PropTypes.bool,
  language: PropTypes.oneOf([
    null,
    'json',
    'html',
    'sql',
    'markdown',
    'javascript',
  ]),
  aboveEditorSection: PropTypes.node,
  readOnly: PropTypes.bool,
};

const defaultProps = {
  onChange: () => {},
  value: '',
  height: 250,
  minLines: 3,
  maxLines: 10,
  offerEditInModal: true,
  readOnly: false,
};

export default class TextAreaControl extends React.Component {
  constructor() {
    super();
    this.onAceChangeDebounce = debounce(value => {
      this.onAceChange(value);
    }, FAST_DEBOUNCE);
  }

  onControlChange(event) {
    this.props.onChange(event.target.value);
  }

  onAceChange(value) {
    this.props.onChange(value);
  }

  renderEditor(inModal = false) {
    const value = this.props.value || '';
    const minLines = inModal ? 40 : this.props.minLines || 12;
    if (this.props.language) {
      const style = { border: '1px solid #CCC' };
      if (this.props.readOnly) {
        style.backgroundColor = '#f2f2f2';
      }
      return (
        <TextAreaEditor
          mode={this.props.language}
          style={style}
          minLines={minLines}
          maxLines={inModal ? 1000 : this.props.maxLines}
          onChange={this.onAceChangeDebounce}
          width="100%"
          height={`${minLines}em`}
          editorProps={{ $blockScrolling: true }}
          value={value}
          readOnly={this.props.readOnly}
        />
      );
    }
    return (
      <TextArea
        placeholder={t('textarea')}
        onChange={this.onControlChange.bind(this)}
        value={value}
        disabled={this.props.readOnly}
        style={{ height: this.props.height }}
      />
    );
  }

  renderModalBody() {
    return (
      <div>
        <div>{this.props.aboveEditorSection}</div>
        {this.renderEditor(true)}
      </div>
    );
  }

  render() {
    const controlHeader = <ControlHeader {...this.props} />;
    return (
      <div>
        {controlHeader}
        {this.renderEditor()}
        {this.props.offerEditInModal && (
          <ModalTrigger
            modalTitle={controlHeader}
            triggerNode={
              <Button buttonSize="small" className="m-t-5">
                {t('Edit')} <strong>{this.props.language}</strong>{' '}
                {t('in modal')}
              </Button>
            }
            modalBody={this.renderModalBody(true)}
            responsive
          />
        )}
      </div>
    );
  }
}

TextAreaControl.propTypes = propTypes;
TextAreaControl.defaultProps = defaultProps;
