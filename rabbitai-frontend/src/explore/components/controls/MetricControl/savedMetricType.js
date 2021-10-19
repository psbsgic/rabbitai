import PropTypes from 'prop-types';

export default PropTypes.shape({
  metric_name: PropTypes.string.isRequired,
  verbose_name: PropTypes.string,
  expression: PropTypes.string.isRequired,
});
