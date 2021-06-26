
import React from 'react';
import cx from 'classnames';

import ChartIcon from 'src/components/ChartIcon';
import { CHART_TYPE } from 'src/dashboard/util/componentTypes';

function traverse({ currentNode = {}, selectedChartId }) {
  if (!currentNode) {
    return null;
  }

  const { label, value, type, children } = currentNode;
  if (children && children.length) {
    const updatedChildren = children.map(child =>
      traverse({ currentNode: child, selectedChartId }),
    );
    return {
      ...currentNode,
      label: (
        <span
          className={cx(`filter-scope-type ${type.toLowerCase()}`, {
            'selected-filter': selectedChartId === value,
          })}
        >
          {type === CHART_TYPE && (
            <span className="type-indicator">
              <ChartIcon />
            </span>
          )}
          {label}
        </span>
      ),
      children: updatedChildren,
    };
  }
  return {
    ...currentNode,
    label: (
      <span
        className={cx(`filter-scope-type ${type.toLowerCase()}`, {
          'selected-filter': selectedChartId === value,
        })}
      >
        {label}
      </span>
    ),
  };
}

export default function renderFilterScopeTreeNodes({ nodes, selectedChartId }) {
  if (!nodes) {
    return [];
  }

  return nodes.map(node => traverse({ currentNode: node, selectedChartId }));
}
