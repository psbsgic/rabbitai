import React, { FC, useMemo, useState } from 'react';
import { Tree } from 'src/common/components';
import { DASHBOARD_ROOT_ID } from 'src/dashboard/util/constants';
import { Tooltip } from 'src/components/Tooltip';
import Icons from 'src/components/Icons';
import { useFilterScopeTree } from './state';
import { findFilterScope, getTreeCheckedItems } from './utils';
import { Scope } from '../../../types';

type ScopingTreeProps = {
  forceUpdate: Function;
  updateFormValues: (values: any) => void;
  formScope?: Scope;
  initialScope: Scope;
  chartId?: number;
  initiallyExcludedCharts?: number[];
};

const buildTreeLeafTitle = (
  label: string,
  hasTooltip: boolean,
  tooltipTitle?: string,
) => {
  let title = <span>{label}</span>;
  if (hasTooltip) {
    title = (
      <>
        {title}&nbsp;
        <Tooltip title={tooltipTitle}>
          <Icons.Info iconSize="m" />
        </Tooltip>
      </>
    );
  }
  return title;
};

const ScopingTree: FC<ScopingTreeProps> = ({
  formScope,
  initialScope,
  forceUpdate,
  updateFormValues,
  chartId,
  initiallyExcludedCharts = [],
}) => {
  const [expandedKeys, setExpandedKeys] = useState<string[]>([
    DASHBOARD_ROOT_ID,
  ]);

  const { treeData, layout } = useFilterScopeTree(
    chartId,
    initiallyExcludedCharts,
    buildTreeLeafTitle,
  );
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
