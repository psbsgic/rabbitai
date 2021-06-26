
import { parsePostForm, JsonObject } from 'cypress/utils';
import {
  WORLD_HEALTH_DASHBOARD,
  WORLD_HEALTH_CHARTS,
  waitForChartLoad,
} from './dashboard.helper';

describe('Dashboard form data', () => {
  const urlParams = { param1: '123', param2: 'abc' };
  before(() => {
    cy.login();

    cy.visit(WORLD_HEALTH_DASHBOARD, { qs: urlParams });
  });

  it('should apply url params to slice requests', () => {
    cy.intercept('/rabbitai/explore_json/*', request => {
      const requestParams = JSON.parse(
        parsePostForm(request.body).form_data as string,
      );
      expect(requestParams.url_params).deep.eq(urlParams);
    });
    cy.intercept('/api/v1/chart/data?*', request => {
      // TODO: export url params to chart data API
      request.body.queries.forEach((query: { url_params: JsonObject }) => {
        expect(query.url_params).deep.eq(urlParams);
      });
    });

    WORLD_HEALTH_CHARTS.forEach(waitForChartLoad);
  });
});
