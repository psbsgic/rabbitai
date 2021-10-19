describe('AdhocFilters', () => {
  beforeEach(() => {
    cy.login();
    cy.intercept('GET', '/rabbitai/explore_json/**').as('getJson');
    cy.intercept('POST', '/rabbitai/explore_json/**').as('postJson');
    cy.intercept('GET', '/rabbitai/filter/table/*/name').as('filterValues');
    cy.visitChartByName('Boys'); // a table chart
    cy.verifySliceSuccess({ waitAlias: '@postJson' });
  });

  xit('Should not load mathjs when not needed', () => {
    cy.get('script[src*="mathjs"]').should('have.length', 0);
  });

  let numScripts = 0;

  xit('Should load AceEditor scripts when needed', () => {
    cy.get('script').then(nodes => {
      numScripts = nodes.length;
    });

    cy.get('[data-test=adhoc_filters]').within(() => {
      cy.get('.Select__control').scrollIntoView().click();
      cy.get('input[type=text]').focus().type('name{enter}');
      cy.get("div[role='button']").first().click();
    });

    // antd tabs do lazy loading, so we need to click on tab with ace editor
    cy.get('#filter-edit-popover').within(() => {
      cy.get('.ant-tabs-tab').contains('Custom SQL').click();
      cy.get('.ant-tabs-tab').contains('Simple').click();
    });

    cy.get('script').then(nodes => {
      // should load new script chunks for SQL editor
      expect(nodes.length).to.greaterThan(numScripts);
    });
  });

  xit('Set simple adhoc filter', () => {
    cy.get('[data-test=adhoc-filter-simple-value] .Select__control').click();
    cy.get('[data-test=adhoc-filter-simple-value] input[type=text]')
      .focus()
      .type('Jack{enter}', { delay: 20 });

    cy.get('[data-test="adhoc-filter-edit-popover-save-button"]').click();

    cy.get(
      '[data-test=adhoc_filters] .Select__control span.option-label',
    ).contains('name = Jack');

    cy.get('button[data-test="run-query-button"]').click();
    cy.verifySliceSuccess({
      waitAlias: '@postJson',
      chartSelector: 'svg',
    });
  });

  xit('Set custom adhoc filter', () => {
    const filterType = 'name';
    const filterContent = "'Amy' OR name = 'Donald'";

    cy.get('[data-test=adhoc_filters] .Select__control')
      .scrollIntoView()
      .click();

    // remove previous input
    cy.get('[data-test=adhoc_filters] input[type=text]')
      .focus()
      .type('{backspace}');

    cy.get('[data-test=adhoc_filters] input[type=text]')
      .focus()
      .type(`${filterType}{enter}`);

    cy.wait('@filterValues');

    // selecting a new filter should auto-open the popup,
    // so the tabshould be visible by now
    cy.get('#filter-edit-popover #adhoc-filter-edit-tabs-tab-SQL').click();
    cy.get('#filter-edit-popover .ace_content').click();
    cy.get('#filter-edit-popover .ace_text-input').type(filterContent);
    cy.get('[data-test="adhoc-filter-edit-popover-save-button"]').click();

    // check if the filter was saved correctly
    cy.get(
      '[data-test=adhoc_filters] .Select__control span.option-label',
    ).contains(`${filterType} = ${filterContent}`);

    cy.get('button[data-test="run-query-button"]').click();
    cy.verifySliceSuccess({
      waitAlias: '@postJson',
      chartSelector: 'svg',
    });
  });
});
