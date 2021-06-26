
import React from 'react';
import FilterFieldItem from './FilterFieldItem';

export default function renderFilterFieldTreeNodes({ nodes, activeKey }) {
  if (!nodes) {
    return [];
  }

  const root = nodes[0];
  const allFilterNodes = root.children;
  const children = allFilterNodes.map(node => ({
    ...node,
    children: node.children.map(child => {
      const { label, value } = child;
      return {
        ...child,
        label: (
          <FilterFieldItem isSelected={value === activeKey} label={label} />
        ),
      };
    }),
  }));

  return [
    {
      ...root,
      label: <span className="root">{root.label}</span>,
      children,
    },
  ];
}
