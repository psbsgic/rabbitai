
import { FORM_DATA_DEFAULTS, NUM_METRIC } from './visualizations/shared.helper';

describe('No Results', () => {
  beforeEach(() => {
    cy.login();
    cy.intercept('POST', '/rabbitai/explore_json/**').as('getJson');
  });

  it('No results message shows up', () => {
    const formData = {
      ...FORM_DATA_DEFAULTS,
      metrics: [NUM_METRIC],
      viz_type: 'line',
      adhoc_filters: [
        {
          expressionType: 'SIMPLE',
          subject: 'state',
          operator: 'IN',
          comparator: ['Fake State'],
          clause: 'WHERE',
          sqlExpression: null,
        },
      ],
    };

    cy.visitChartByParams(JSON.stringify(formData));
    cy.wait('@getJson').its('response.statusCode').should('eq', 200);
    cy.get('div.chart-container').contains('No Results');
  });
});
