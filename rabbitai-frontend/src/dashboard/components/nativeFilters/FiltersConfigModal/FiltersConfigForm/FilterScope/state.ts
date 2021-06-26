
import { useMemo } from 'react';
import { useSelector } from 'react-redux';
import { t } from '@rabbitai-ui/core';
import { Charts, Layout, RootState } from 'src/dashboard/types';
import { DASHBOARD_ROOT_ID } from 'src/dashboard/util/constants';
import {
  CHART_TYPE,
  DASHBOARD_ROOT_TYPE,
} from 'src/dashboard/util/componentTypes';
import { TreeItem } from './types';
import { buildTree } from './utils';

// eslint-disable-next-line import/prefer-default-export
export function useFilterScopeTree(
  currentChartId?: number,
): {
  treeData: [TreeItem];
  layout: Layout;
} {
  const layout = useSelector<RootState, Layout>(
    ({ dashboardLayout: { present } }) => present,
  );

  const charts = useSelector<RootState, Charts>(({ charts }) => charts);
  const tree = {
    children: [],
    key: DASHBOARD_ROOT_ID,
    type: DASHBOARD_ROOT_TYPE,
    title: t('All panels'),
  };

  // We need to get only nodes that have charts as children or grandchildren
  const validNodes = useMemo(
    () =>
      Object.values(layout).reduce<string[]>((acc, cur) => {
        const { id, parents = [], type, meta } = cur;
        if (type === CHART_TYPE && currentChartId !== meta?.chartId) {
          return [...new Set([...acc, ...parents, id])];
        }
        return acc;
      }, []),
    [layout, currentChartId],
  );

  useMemo(() => {
    buildTree(layout[DASHBOARD_ROOT_ID], tree, layout, charts, validNodes);
  }, [charts, layout, tree]);

  return { treeData: [tree], layout };
}