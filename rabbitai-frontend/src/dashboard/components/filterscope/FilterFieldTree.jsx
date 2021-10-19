import React from 'react';
import PropTypes from 'prop-types';
import CheckboxTree from 'react-checkbox-tree';
import { filterScopeSelectorTreeNodePropShape } from 'src/dashboard/util/propShapes';
import treeIcons from './treeIcons';
import renderFilterFieldTreeNodes from './renderFilterFieldTreeNodes';

const propTypes = {
  activeKey: PropTypes.string,
  nodes: PropTypes.arrayOf(filterScopeSelectorTreeNodePropShape).isRequired,
  checked: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  ).isRequired,
  expanded: PropTypes.arrayOf(
    PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  ).isRequired,
  onCheck: PropTypes.func.isRequired,
  onExpand: PropTypes.func.isRequired,
  onClick: PropTypes.func.isRequired,
};

const defaultProps = {
  activeKey: null,
};

export default function FilterFieldTree({
  activeKey,
  nodes = [],
  checked = [],
  expanded = [],
  onClick,
  onCheck,
  onExpand,
}) {
  return (
    <CheckboxTree
      showExpandAll
      showNodeIcon={false}
      expandOnClick
      nodes={renderFilterFieldTreeNodes({ nodes, activeKey })}
      checked={checked}
      expanded={expanded}
      onClick={onClick}
      onCheck={onCheck}
      onExpand={onExpand}
      icons={treeIcons}
    />
  );
}

FilterFieldTree.propTypes = propTypes;
FilterFieldTree.defaultProps = defaultProps;
