
import { isLegacyResponse, parsePostForm } from 'cypress/utils';
import {
  WORLD_HEALTH_CHARTS,
  WORLD_HEALTH_DASHBOARD,
  getChartAliasesBySpec,
  waitForChartLoad,
} from './dashboard.helper';

describe('Dashboard filter', () => {
  before(() => {
    cy.login();
    cy.visit(WORLD_HEALTH_DASHBOARD);
  });

  it('should apply filter', () => {
    WORLD_HEALTH_CHARTS.forEach(waitForChartLoad);
    getChartAliasesBySpec(
      WORLD_HEALTH_CHARTS.filter(({ viz }) => viz !== 'filter_box'),
    ).then(nonFilterChartAliases => {
      cy.get('.Select__placeholder:first').click();

      // should show the filter indicator
      cy.get('svg[data-test="filter"]:visible').should(nodes => {
        expect(nodes.length).to.least(9);
      });

      cy.get('.Select__control:first input[type=text]').type('So', {
        force: true,
        delay: 100,
      });

      cy.get('.Select__menu').first().contains('South Asia').click();

      // should still have all filter indicators
      cy.get('svg[data-test="filter"]:visible').should(nodes => {
        expect(nodes.length).to.least(9);
      });

      cy.get('.filter_box button').click({ force: true });
      cy.wait(nonFilterChartAliases).then(requests => {
        requests.forEach(({ response, request }) => {
          const responseBody = response?.body;
          let requestFilter;
          if (isLegacyResponse(responseBody)) {
            const requestFormData = parsePostForm(request.body);
            const requestParams = JSON.parse(
              requestFormData.form_data as string,
            );
            requestFilter = requestParams.extra_filters[0];
          } else {
            requestFilter = request.body.queries[0].filters[0];
          }
          expect(requestFilter).deep.eq({
            col: 'region',
            op: 'IN',
            val: ['South Asia'],
          });
        });
      });
    });

    // TODO add test with South Asia{enter} type action to select filter
  });
});
