

import React, { FC, useMemo, useState } from 'react';
import { Tree } from 'src/common/components';
import { DASHBOARD_ROOT_ID } from 'src/dashboard/util/constants';
import { useFilterScopeTree } from './state';
import { findFilterScope, getTreeCheckedItems } from './utils';
import { Scope } from '../../../types';

type ScopingTreeProps = {
  forceUpdate: Function;
  updateFormValues: (values: any) => void;
  formScope?: Scope;
  initialScope: Scope;
  chartId?: number;
};

const ScopingTree: FC<ScopingTreeProps> = ({
  formScope,
  initialScope,
  forceUpdate,
  updateFormValues,
  chartId,
}) => {
  const [expandedKeys, setExpandedKeys] = useState<string[]>([
    DASHBOARD_ROOT_ID,
  ]);

  const { treeData, layout } = useFilterScopeTree(chartId);
  const [autoExpandParent, setAutoExpandParent] = useState<boolean>(true);

  const handleExpand = (expandedKeys: string[]) => {
    setExpandedKeys(expandedKeys);
    setAutoExpandParent(false);
  };

  const handleCheck = (checkedKeys: string[]) => {
    forceUpdate();
    const scope = findFilterScope(checkedKeys, layout);
    if (chartId !== undefined) {
      scope.excluded = [...new Set([...scope.excluded, chartId])];
    }
    updateFormValues({
      scope,
    });
  };

  const checkedKeys = useMemo(
    () => getTreeCheckedItems({ ...(formScope || initialScope) }, layout),
    [formScope, initialScope, layout],
  );

  return (
    <Tree
      checkable
      selectable={false}
      onExpand={handleExpand}
      expandedKeys={expandedKeys}
      autoExpandParent={autoExpandParent}
      onCheck={handleCheck}
      checkedKeys={checkedKeys}
      treeData={treeData}
    />
  );
};

export default ScopingTree;
