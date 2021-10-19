import React from 'react';
import PropTypes from 'prop-types';
import Select from 'src/components/Select';
import { t } from '@superset-ui/core';
import ModalTrigger from 'src/components/ModalTrigger';
import { CssEditor as AceCssEditor } from 'src/components/AsyncAceEditor';

const propTypes = {
  initialCss: PropTypes.string,
  triggerNode: PropTypes.node.isRequired,
  onChange: PropTypes.func,
  templates: PropTypes.array,
};

const defaultProps = {
  initialCss: '',
  onChange: () => {},
};

class CssEditor extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      css: props.initialCss,
    };
    this.changeCss = this.changeCss.bind(this);
    this.changeCssTemplate = this.changeCssTemplate.bind(this);
  }

  componentDidMount() {
    AceCssEditor.preload();
  }

  changeCss(css) {
    this.setState({ css }, () => {
      this.props.onChange(css);
    });
  }

  changeCssTemplate(opt) {
    this.changeCss(opt.css);
  }

  renderTemplateSelector() {
    if (this.props.templates) {
      return (
        <div style={{ zIndex: 10 }}>
          <h5>{t('Load a template')}</h5>
          <Select
            options={this.props.templates}
            placeholder={t('Load a CSS template')}
            onChange={this.changeCssTemplate}
          />
        </div>
      );
    }
    return null;
  }

  render() {
    return (
      <ModalTrigger
        triggerNode={this.props.triggerNode}
        modalTitle={t('CSS')}
        modalBody={
          <div>
            {this.renderTemplateSelector()}
            <div style={{ zIndex: 1 }}>
              <h5>{t('Live CSS editor')}</h5>
              <div style={{ border: 'solid 1px grey' }}>
                <AceCssEditor
                  minLines={12}
                  maxLines={30}
                  onChange={this.changeCss}
                  height="200px"
                  width="100%"
                  editorProps={{ $blockScrolling: true }}
                  enableLiveAutocompletion
                  value={this.state.css || ''}
                />
              </div>
            </div>
          </div>
        }
      />
    );
  }
}

CssEditor.propTypes = propTypes;
CssEditor.defaultProps = defaultProps;

export default CssEditor;
