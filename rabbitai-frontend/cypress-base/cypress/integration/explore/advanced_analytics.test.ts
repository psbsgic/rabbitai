describe('Advanced analytics', () => {
  beforeEach(() => {
    cy.login();
    cy.intercept('GET', '/rabbitai/explore_json/**').as('getJson');
    cy.intercept('POST', '/rabbitai/explore_json/**').as('postJson');
  });

  it('Create custom time compare', () => {
    cy.visitChartByName('Num Births Trend');
    cy.verifySliceSuccess({ waitAlias: '@postJson' });

    cy.get('.ant-collapse-header').contains('Advanced Analytics').click();

    cy.get('[data-test=time_compare]').find('.Select__control').click();
    cy.get('[data-test=time_compare]')
      .find('input[type=text]')
      .type('28 days{enter}');

    cy.get('[data-test=time_compare]')
      .find('input[type=text]')
      .type('1 year{enter}');

    cy.get('button[data-test="run-query-button"]').click();
    cy.wait('@postJson');
    cy.reload();
    cy.verifySliceSuccess({
      waitAlias: '@postJson',
      chartSelector: 'svg',
    });

    cy.get('.ant-collapse-header').contains('Advanced Analytics').click();
    cy.get('[data-test=time_compare]')
      .find('.Select__multi-value__label')
      .contains('28 days');
    cy.get('[data-test=time_compare]')
      .find('.Select__multi-value__label')
      .contains('1 year');
  });
});
