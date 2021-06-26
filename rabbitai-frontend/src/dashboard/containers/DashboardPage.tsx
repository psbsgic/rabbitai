
import React, { useEffect, useState, FC } from 'react';
import { useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';
import Loading from 'src/components/Loading';
import {
  useDashboard,
  useDashboardCharts,
  useDashboardDatasets,
} from 'src/common/hooks/apiResources';
import { ResourceStatus } from 'src/common/hooks/apiResources/apiResources';
import { usePrevious } from 'src/common/hooks/usePrevious';
import { hydrateDashboard } from 'src/dashboard/actions/hydrate';
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
  const { idOrSlug } = useParams<{ idOrSlug: string }>();
  const [isLoaded, setLoaded] = useState(false);
  const dashboardResource = useDashboard(idOrSlug);
  const chartsResource = useDashboardCharts(idOrSlug);
  const datasetsResource = useDashboardDatasets(idOrSlug);
  const isLoading = [dashboardResource, chartsResource, datasetsResource].some(
    resource => resource.status === ResourceStatus.LOADING,
  );
  const wasLoading = usePrevious(isLoading);
  const error = [dashboardResource, chartsResource, datasetsResource].find(
    resource => resource.status === ResourceStatus.ERROR,
  )?.error;

  useEffect(() => {
    if (dashboardResource.result) {
      document.title = dashboardResource.result.dashboard_title;
    }
  }, [dashboardResource.result]);

  useEffect(() => {
    if (
      wasLoading &&
      dashboardResource.status === ResourceStatus.COMPLETE &&
      chartsResource.status === ResourceStatus.COMPLETE &&
      datasetsResource.status === ResourceStatus.COMPLETE
    ) {
      dispatch(
        hydrateDashboard(
          dashboardResource.result,
          chartsResource.result,
          datasetsResource.result,
        ),
      );
      injectCustomCss(dashboardResource.result.css);
      setLoaded(true);
    }
  }, [
    dispatch,
    wasLoading,
    dashboardResource,
    chartsResource,
    datasetsResource,
  ]);

  if (error) throw error; // caught in error boundary

  if (!isLoaded) return <Loading />;
  return <DashboardContainer />;
};

export default DashboardPage;
