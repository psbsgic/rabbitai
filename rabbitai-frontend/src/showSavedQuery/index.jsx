
import React from 'react';
import ReactDom from 'react-dom';
import Form from 'react-jsonschema-form';
import { interpolate } from 'src/showSavedQuery/utils';
import './index.less';

const scheduleInfoContainer = document.getElementById('schedule-info');
const bootstrapData = JSON.parse(
  scheduleInfoContainer.getAttribute('data-bootstrap'),
);
const config = bootstrapData.common.feature_flags.SCHEDULED_QUERIES;
const { query } = bootstrapData.common;
const scheduleInfo = query.extra_json.schedule_info;
const linkback = config.linkback ? interpolate(config.linkback, query) : null;

if (scheduleInfo && config) {
  // hide instructions when showing schedule info
  config.JSONSCHEMA.description = '';

  ReactDom.render(
    <div>
      <Form
        schema={config.JSONSCHEMA}
        uiSchema={config.UISCHEMA}
        formData={scheduleInfo}
        disabled
      >
        <br />
      </Form>
      {linkback && (
        <div className="linkback">
          <a href={linkback}>
            <i className="fa fa-link" />
            &nbsp; Pipeline status
          </a>
        </div>
      )}
    </div>,
    scheduleInfoContainer,
  );
}
