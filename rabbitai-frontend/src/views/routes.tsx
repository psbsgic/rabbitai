import { FeatureFlag, isFeatureEnabled } from 'src/featureFlags';
import React, { lazy } from 'react';

// not lazy loaded since this is the home page.
import Welcome from 'src/views/CRUD/welcome/Welcome';

const AnnotationLayersList = lazy(
  () =>
    import(
      /* webpackChunkName: "AnnotationLayersList" */ 'src/views/CRUD/annotationlayers/AnnotationLayersList'
    ),
);
const AlertList = lazy(
  () =>
    import(
      /* webpackChunkName: "AlertList" */ 'src/views/CRUD/alert/AlertList'
    ),
);
const AnnotationList = lazy(
  () =>
    import(
      /* webpackChunkName: "AnnotationList" */ 'src/views/CRUD/annotation/AnnotationList'
    ),
);
const ChartList = lazy(
  () =>
    import(
      /* webpackChunkName: "ChartList" */ 'src/views/CRUD/chart/ChartList'
    ),
);
const CssTemplatesList = lazy(
  () =>
    import(
      /* webpackChunkName: "CssTemplatesList" */ 'src/views/CRUD/csstemplates/CssTemplatesList'
    ),
);
const DashboardList = lazy(
  () =>
    import(
      /* webpackChunkName: "DashboardList" */ 'src/views/CRUD/dashboard/DashboardList'
    ),
);
const DashboardPage = lazy(
  () =>
    import(
      /* webpackChunkName: "DashboardPage" */ 'src/dashboard/containers/DashboardPage'
    ),
);
const DatabaseList = lazy(
  () =>
    import(
      /* webpackChunkName: "DatabaseList" */ 'src/views/CRUD/data/database/DatabaseList'
    ),
);
const DatasetList = lazy(
  () =>
    import(
      /* webpackChunkName: "DatasetList" */ 'src/views/CRUD/data/dataset/DatasetList'
    ),
);
const ExecutionLog = lazy(
  () =>
    import(
      /* webpackChunkName: "ExecutionLog" */ 'src/views/CRUD/alert/ExecutionLog'
    ),
);
const QueryList = lazy(
  () =>
    import(
      /* webpackChunkName: "QueryList" */ 'src/views/CRUD/data/query/QueryList'
    ),
);
const SavedQueryList = lazy(
  () =>
    import(
      /* webpackChunkName: "SavedQueryList" */ 'src/views/CRUD/data/savedquery/SavedQueryList'
    ),
);

type Routes = {
  path: string;
  Component: React.ComponentType;
  Fallback?: React.ComponentType;
  props?: React.ComponentProps<any>;
}[];

/**
 * 路由（至少包括路径path和组件Component等属性）对象的列表。
 */
export const routes: Routes = [
  {
    path: '/rabbitai/welcome/',
    Component: Welcome,
  },
  {
    path: '/dashboard/list/',
    Component: DashboardList,
  },
  {
    path: '/rabbitai/dashboard/:idOrSlug/',
    Component: DashboardPage,
  },
  {
    path: '/chart/list/',
    Component: ChartList,
  },
  {
    path: '/tablemodelview/list/',
    Component: DatasetList,
  },
  {
    path: '/databaseview/list/',
    Component: DatabaseList,
  },
  {
    path: '/savedqueryview/list/',
    Component: SavedQueryList,
  },
  {
    path: '/csstemplatemodelview/list/',
    Component: CssTemplatesList,
  },
  {
    path: '/annotationlayermodelview/list/',
    Component: AnnotationLayersList,
  },
  {
    path: '/annotationmodelview/:annotationLayerId/annotation/',
    Component: AnnotationList,
  },
  {
    path: '/rabbitai/sqllab/history/',
    Component: QueryList,
  },
  {
    path: '/alert/list/',
    Component: AlertList,
  },
  {
    path: '/report/list/',
    Component: AlertList,
    props: {
      isReportEnabled: true,
    },
  },
  {
    path: '/alert/:alertId/log/',
    Component: ExecutionLog,
  },
  {
    path: '/report/:alertId/log/',
    Component: ExecutionLog,
    props: {
      isReportEnabled: true,
    },
  },
];

const frontEndRoutes = routes
  .map(r => r.path)
  .reduce(
    (acc, curr) => ({
      ...acc,
      [curr]: true,
    }),
    {},
  );

/**
 * 指定路径是否前端路由。
 *
 * @param path
 */
export function isFrontendRoute(path?: string) {
  if (!isFeatureEnabled(FeatureFlag.ENABLE_REACT_CRUD_VIEWS)) return false;
  if (path) {
    const basePath = path.split(/[?#]/)[0]; // strip out query params and link bookmarks
    return !!frontEndRoutes[basePath];
  }
  return false;
}
