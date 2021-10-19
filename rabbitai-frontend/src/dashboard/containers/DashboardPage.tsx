import React, { useEffect, FC } from 'react';
import { t } from '@superset-ui/core';
import { useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';
import { useToasts } from 'src/messageToasts/enhancers/withToasts';
import Loading from 'src/components/Loading';
import {
  useDashboard,
  useDashboardCharts,
  useDashboardDatasets,
} from 'src/common/hooks/apiResources';
import { hydrateDashboard } from 'src/dashboard/actions/hydrate';
import { setDatasources } from 'src/dashboard/actions/datasources';
import injectCustomCss from 'src/dashboard/util/injectCustomCss';

const DashboardContainer = React.lazy(
  () =>
    import(
      /* webpackChunkName: "DashboardContainer" */
      /* webpackPreload: true */
      'src/dashboard/containers/Dashboard'
    ),
);

const DashboardPage: FC = () => {
  const dispatch = useDispatch();
  const { addDangerToast } = useToasts();
  const { idOrSlug } = useParams<{ idOrSlug: string }>();
  const { result: dashboard, error: dashboardApiError } = useDashboard(
    idOrSlug,
  );
  const { result: charts, error: chartsApiError } = useDashboardCharts(
    idOrSlug,
  );
  const { result: datasets, error: datasetsApiError } = useDashboardDatasets(
    idOrSlug,
  );

  const error = dashboardApiError || chartsApiError;
  const readyToRender = Boolean(dashboard && charts);
  const { dashboard_title, css } = dashboard || {};

  useEffect(() => {
    if (readyToRender) {
      dispatch(hydrateDashboard(dashboard, charts));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [readyToRender]);

  useEffect(() => {
    if (dashboard_title) {
      document.title = dashboard_title;
    }
  }, [dashboard_title]);

  useEffect(() => {
    if (css) {
      // returning will clean up custom css
      // when dashboard unmounts or changes
      return injectCustomCss(css);
    }
    return () => {};
  }, [css]);

  useEffect(() => {
    if (datasetsApiError) {
      addDangerToast(
        t('Error loading chart datasources. Filters may not work correctly.'),
      );
    } else {
      dispatch(setDatasources(datasets));
    }
  }, [addDangerToast, datasets, datasetsApiError, dispatch]);

  if (error) throw error; // caught in error boundary
  if (!readyToRender) return <Loading />;

  return <DashboardContainer />;
};

export default DashboardPage;
