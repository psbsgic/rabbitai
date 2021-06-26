
import React from 'react';
import PropTypes from 'prop-types';
import { t } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import Label from 'src/components/Label';

const propTypes = {
  dashboardId: PropTypes.number.isRequired,
  isPublished: PropTypes.bool.isRequired,
  savePublished: PropTypes.func.isRequired,
  canEdit: PropTypes.bool.isRequired,
  canSave: PropTypes.bool.isRequired,
};

const draftButtonTooltip = t(
  'This dashboard is not published, it will not show up in the list of dashboards. ' +
    'Click here to publish this dashboard.',
);

const draftDivTooltip = t(
  'This dashboard is not published which means it will not show up in the list of dashboards.' +
    ' Favorite it to see it there or access it by using the URL directly.',
);

const publishedTooltip = t(
  'This dashboard is published. Click to make it a draft.',
);

export default class PublishedStatus extends React.Component {
  componentDidMount() {
    this.togglePublished = this.togglePublished.bind(this);
  }

  togglePublished() {
    this.props.savePublished(this.props.dashboardId, !this.props.isPublished);
  }

  render() {
    // Show everybody the draft badge
    if (!this.props.isPublished) {
      // if they can edit the dash, make the badge a button
      if (this.props.canEdit && this.props.canSave) {
        return (
          <Tooltip
            id="unpublished-dashboard-tooltip"
            placement="bottom"
            title={draftButtonTooltip}
          >
            <Label
              onClick={() => {
                this.togglePublished();
              }}
            >
              {t('Draft')}
            </Label>
          </Tooltip>
        );
      }
      return (
        <Tooltip
          id="unpublished-dashboard-tooltip"
          placement="bottom"
          title={draftDivTooltip}
        >
          <Label>{t('Draft')}</Label>
        </Tooltip>
      );
    }

    // Show the published badge for the owner of the dashboard to toggle
    if (this.props.canEdit && this.props.canSave) {
      return (
        <Tooltip
          id="published-dashboard-tooltip"
          placement="bottom"
          title={publishedTooltip}
        >
          <Label
            onClick={() => {
              this.togglePublished();
            }}
          >
            {t('Published')}
          </Label>
        </Tooltip>
      );
    }

    // Don't show anything if one doesn't own the dashboard and it is published
    return null;
  }
}

PublishedStatus.propTypes = propTypes;
