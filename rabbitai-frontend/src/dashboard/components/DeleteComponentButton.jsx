import React from 'react';
import PropTypes from 'prop-types';
import Icons from 'src/components/Icons';
import IconButton from './IconButton';

const propTypes = {
  onDelete: PropTypes.func.isRequired,
};

const defaultProps = {};

export default class DeleteComponentButton extends React.PureComponent {
  render() {
    const { onDelete } = this.props;
    return (
      <IconButton onClick={onDelete} icon={<Icons.Trash iconSize="xl" />} />
    );
  }
}

DeleteComponentButton.propTypes = propTypes;
DeleteComponentButton.defaultProps = defaultProps;
