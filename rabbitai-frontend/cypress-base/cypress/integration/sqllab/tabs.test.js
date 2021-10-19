describe('SqlLab query tabs', () => {
  beforeEach(() => {
    cy.login();
    cy.visit('/rabbitai/sqllab');
  });

  it('allows you to create a tab', () => {
    cy.get('[data-test="sql-editor-tabs"]').then(tabList => {
      const initialTabCount = tabList.length;
      // add tab
      cy.get('[data-test="add-tab-icon"]').first().click();
      // wait until we find the new tab
      cy.get('[data-test="sql-editor-tabs"]')
        .children()
        .eq(0)
        .contains(`Untitled Query ${initialTabCount + 1}`);
      cy.get('[data-test="sql-editor-tabs"]')
        .children()
        .eq(0)
        .contains(`Untitled Query ${initialTabCount + 2}`);
    });
  });

  it('allows you to close a tab', () => {
    cy.get('[data-test="sql-editor-tabs"]')
      .children()
      .then(tabListA => {
        const initialTabCount = tabListA.length;

        // open the tab dropdown to remove
        cy.get('[data-test="dropdown-toggle-button"]')
          .children()
          .first()
          .click({
            force: true,
          });

        // first item is close
        cy.get('[data-test="close-tab-menu-option"]').click();

        cy.get('[data-test="sql-editor-tabs"]').should(
          'have.length',
          initialTabCount - 1,
        );
      });
  });
});
