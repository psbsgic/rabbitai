import React from 'react';
import PropTypes from 'prop-types';
import CheckboxTree from 'react-checkbox-tree';
import { filterScopeSelectorTreeNodePropShape } from 'src/dashboard/util/propShapes';
import renderFilterScopeTreeNodes from './renderFilterScopeTreeNodes';
import treeIcons from './treeIcons';

const propTypes = {
  nodes: PropTypes.arrayOf(filterScopeSelectorTreeNodePropShape).isRequired,
  checked: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  ).isRequired,
  expanded: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  ).isRequired,
  onCheck: PropTypes.func.isRequired,
  onExpand: PropTypes.func.isRequired,
  selectedChartId: PropTypes.number,
};

const defaultProps = {
  selectedChartId: null,
};

const NOOP = () => {};

export default function FilterScopeTree({
  nodes = [],
  checked = [],
  expanded = [],
  onCheck,
  onExpand,
  selectedChartId,
}) {
  return (
    <CheckboxTree
      showExpandAll
      expandOnClick
      showNodeIcon={false}
      nodes={renderFilterScopeTreeNodes({ nodes, selectedChartId })}
      checked={checked}
      expanded={expanded}
      onCheck={onCheck}
      onExpand={onExpand}
      onClick={NOOP}
      icons={treeIcons}
    />
  );
}

FilterScopeTree.propTypes = propTypes;
FilterScopeTree.defaultProps = defaultProps;
