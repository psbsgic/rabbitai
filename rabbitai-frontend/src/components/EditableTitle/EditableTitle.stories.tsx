import React from 'react';
import EditableTitle, { EditableTitleProps } from '.';

export default {
  title: 'EditableTitle',
  component: EditableTitle,
};

export const InteractiveEditableTitle = (props: EditableTitleProps) => (
  <EditableTitle {...props} />
);

InteractiveEditableTitle.args = {
  canEdit: true,
  editing: false,
  emptyText: 'Empty text',
  multiLine: true,
  noPermitTooltip: 'Not permitted',
  showTooltip: true,
  title: 'Title',
  defaultTitle: 'Default title',
  placeholder: 'Placeholder',
};

InteractiveEditableTitle.argTypes = {
  onSaveTitle: { action: 'onSaveTitle' },
};

InteractiveEditableTitle.story = {
  parameters: {
    knobs: {
      disable: true,
    },
  },
};
