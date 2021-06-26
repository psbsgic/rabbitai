
describe('Annotations', () => {
  beforeEach(() => {
    cy.login();
    cy.intercept('GET', '/rabbitai/explore_json/**').as('getJson');
    cy.intercept('POST', '/rabbitai/explore_json/**').as('postJson');
  });

  it('Create formula annotation y-axis goal line', () => {
    cy.visitChartByName('Num Births Trend');
    cy.verifySliceSuccess({ waitAlias: '@postJson' });

    const layerLabel = 'Goal line';

    cy.get('[data-test=annotation_layers]').click();

    cy.get('[data-test="popover-content"]').within(() => {
      cy.get('[aria-label=Name]').type(layerLabel);
      cy.get('[aria-label=Formula]').type('y=1400000');
      cy.get('button').contains('OK').click();
    });

    cy.get('button[data-test="run-query-button"]').click();
    cy.get('[data-test=annotation_layers]').contains(layerLabel);

    cy.verifySliceSuccess({
      waitAlias: '@postJson',
      chartSelector: 'svg',
    });
    cy.get('.nv-legend-text').should('have.length', 2);
  });
});
