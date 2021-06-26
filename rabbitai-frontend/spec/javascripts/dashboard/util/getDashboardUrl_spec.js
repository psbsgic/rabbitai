
import getDashboardUrl from 'src/dashboard/util/getDashboardUrl';
import { DASHBOARD_FILTER_SCOPE_GLOBAL } from 'src/dashboard/reducers/dashboardFilters';
import { DashboardStandaloneMode } from '../../../../src/dashboard/util/constants';

describe('getChartIdsFromLayout', () => {
  const filters = {
    '35_key': {
      values: ['value'],
      scope: DASHBOARD_FILTER_SCOPE_GLOBAL,
    },
  };

  const globalLocation = window.location;
  afterEach(() => {
    window.location = globalLocation;
  });

  it('should encode filters', () => {
    const url = getDashboardUrl('path', filters);
    expect(url).toBe(
      'path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D',
    );
  });

  it('should encode filters with hash', () => {
    const urlWithHash = getDashboardUrl('path', filters, 'iamhashtag');
    expect(urlWithHash).toBe(
      'path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D#iamhashtag',
    );
  });

  it('should encode filters with standalone', () => {
    const urlWithStandalone = getDashboardUrl(
      'path',
      filters,
      '',
      DashboardStandaloneMode.HIDE_NAV,
    );
    expect(urlWithStandalone).toBe(
      `path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D&standalone=${DashboardStandaloneMode.HIDE_NAV}`,
    );
  });

  it('should encode filters with missing standalone', () => {
    const urlWithStandalone = getDashboardUrl('path', filters, '', null);
    expect(urlWithStandalone).toBe(
      'path?preselect_filters=%7B%2235%22%3A%7B%22key%22%3A%5B%22value%22%5D%7D%7D',
    );
  });
});
