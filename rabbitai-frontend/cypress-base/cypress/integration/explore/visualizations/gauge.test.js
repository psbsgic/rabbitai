
describe('Visualization > Gauge', () => {
  const GAUGE_FORM_DATA = {
    datasource: '2__table',
    viz_type: 'gauge_chart',
    metric: 'count',
    adhoc_filters: [],
    slice_id: 49,
    row_limit: 10,
  };

  function verify(formData) {
    cy.visitChartByParams(JSON.stringify(formData));
    cy.verifySliceSuccess({ waitAlias: '@getJson' });
  }

  beforeEach(() => {
    cy.login();
    cy.intercept('POST', '/api/v1/chart/data*').as('getJson');
  });

  it('should work', () => {
    verify(GAUGE_FORM_DATA);
    cy.get('.chart-container .gauge_chart canvas').should('have.length', 1);
  });

  it('should work with simple filter', () => {
    verify({
      ...GAUGE_FORM_DATA,
      adhoc_filters: [
        {
          expressionType: 'SIMPLE',
          subject: 'country_code',
          operator: '==',
          comparator: 'USA',
          clause: 'WHERE',
          sqlExpression: null,
          isExtra: false,
          isNew: false,
          filterOptionName: 'filter_jaemvkxd5h_ku22m3wyo',
        },
      ],
    });
    cy.get('.chart-container .gauge_chart canvas').should('have.length', 1);
  });
});
