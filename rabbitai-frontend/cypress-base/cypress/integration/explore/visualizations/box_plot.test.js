
describe('Visualization > Box Plot', () => {
  const BOX_PLOT_FORM_DATA = {
    datasource: '2__table',
    viz_type: 'box_plot',
    slice_id: 49,
    granularity_sqla: 'year',
    time_grain_sqla: 'P1D',
    time_range: '1960-01-01 : now',
    metrics: ['sum__SP_POP_TOTL'],
    adhoc_filters: [],
    groupby: ['region'],
    limit: '25',
    color_scheme: 'bnbColors',
    whisker_options: 'Min/max (no outliers)',
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
    verify(BOX_PLOT_FORM_DATA);
    cy.get('.chart-container .box_plot canvas').should('have.length', 1);
  });
});
