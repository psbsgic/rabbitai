import { t, SupersetClient } from '@superset-ui/core';

interface DashboardItem {
  changed_by_name: string;
  changed_on: string;
  creator: string;
  dashboard_link: string;
  dashboard_title: string;
  id: number;
  modified: string;
  url: string;
}

interface Dashboards extends DashboardItem {
  title: string;
}

export const getDashboards = async (
  query: string,
): Promise<(Dashboards | { title: string })[]> => {
  // todo: Build a dedicated endpoint for dashboard searching
  // i.e. rabbitai/v1/api/dashboards?q=${query}
  let response;
  try {
    response = await SupersetClient.get({
      endpoint: `/dashboardasync/api/read?_oc_DashboardModelViewAsync=changed_on&_od_DashboardModelViewAsync=desc&_flt_2_dashboard_title=${query}`,
    });
  } catch (error) {
    return [{ title: t('An error occurred while fetching dashboards') }];
  }
  return response?.json.result.map((item: DashboardItem) => ({
    title: item.dashboard_title,
    ...item,
  }));
};
