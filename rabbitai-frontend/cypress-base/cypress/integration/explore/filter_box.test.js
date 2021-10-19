import { FORM_DATA_DEFAULTS } from './visualizations/shared.helper';

describe('Edit FilterBox Chart', () => {
  const VIZ_DEFAULTS = { ...FORM_DATA_DEFAULTS, viz_type: 'filter_box' };

  function verify(formData) {
    cy.visitChartByParams(JSON.stringify(formData));
    cy.verifySliceSuccess({ waitAlias: '@getJson' });
  }

  beforeEach(() => {
    cy.login();
    cy.intercept('POST', '/rabbitai/explore_json/**').as('getJson');
  });

  it('should work with default date filter', () => {
    verify(VIZ_DEFAULTS);
    // Filter box should default to having a date filter with no filter selected
    cy.get('div.filter_box').contains('No filter');
  });
});
