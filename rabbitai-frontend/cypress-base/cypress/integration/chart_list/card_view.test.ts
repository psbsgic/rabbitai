import { CHART_LIST } from './chart_list.helper';

describe('chart card view', () => {
  beforeEach(() => {
    cy.login();
    cy.visit(CHART_LIST);
    cy.get('[data-test="card-view"]').click();
  });

  it('should load cards', () => {
    cy.get('[data-test="chart-list-view"]');
    cy.get('[data-test="styled-card"]').should('be.visible');
    cy.get('[data-test="styled-card"]').should('have.length', 25);
  });

  it('should allow to favorite/unfavorite chart card', () => {
    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-selected']")
      .should('not.exist');
    cy.get("[data-test='card-actions']")
      .find("[data-test='favorite-unselected']")
      .first()
      .click();
    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-selected']")
      .should('be.visible');
    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-unselected']")
      .should('not.exist');

    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-unselected']")
      .should('not.exist');
    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-selected']")
      .click();
    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-unselected']")
      .should('be.visible');
    cy.get("[data-test='card-actions']")
      .first()
      .find("[data-test='favorite-selected']")
      .should('not.exist');
  });

  xit('should sort correctly', () => {
    // sort Alphabetical
    cy.get('.Select__control').last().should('be.visible');
    cy.get('.Select__control').last().click();
    cy.get('.Select__menu').contains('Alphabetical').click();
    cy.get('[data-test="chart-list-view"]').should('be.visible');
    cy.get('[data-test="styled-card"]').first().contains('% Rural');

    // sort Recently Modified
    cy.get('.Select__control').last().should('be.visible');
    cy.get('.Select__control').last().click();
    cy.get('.Select__menu').contains('Recently Modified').click();
    cy.get('[data-test="chart-list-view"]').should('be.visible');
    // TODO - next line is/was flaky
    cy.get('[data-test="styled-card"]').first().contains('Unicode Cloud');
    cy.get('[data-test="styled-card"]')
      .last()
      .contains('Life Expectancy VS Rural %');
  });

  // flaky
  xit('should delete correctly', () => {
    // show delete modal
    cy.get('[data-test="more-horiz"]').last().trigger('mouseover');
    cy.get('[data-test="chart-list-delete-option"]')
      .last()
      .should('be.visible');
    cy.get('[data-test="chart-list-delete-option"]')
      .last()
      .contains('Delete')
      .click();
    cy.get('[data-test="Please Confirm-modal"]').should('be.visible');
    cy.get('[data-test="modal-confirm-button"]').should(
      'have.attr',
      'disabled',
    );
    cy.get('[data-test="Please Confirm-modal"]').should('be.visible');
    cy.get("[data-test='delete-modal-input']").type('DELETE');
    cy.get('[data-test="modal-confirm-button"]').should(
      'not.have.attr',
      'disabled',
    );
    cy.get('[data-test="modal-cancel-button"]').click();
  });

  // flaky
  xit('should edit correctly', () => {
    // show edit modal
    cy.get('[data-test="more-horiz"]').last().trigger('mouseover');
    cy.get('[data-test="chart-list-edit-option"]').last().should('be.visible');
    cy.get('[data-test="chart-list-edit-option"]').last().click();
    cy.get('[data-test="properties-edit-modal"]').should('be.visible');
    cy.get('[data-test="properties-modal-name-input"]').should(
      'not.have.value',
    );
    cy.get('[data-test="properties-modal-cancel-button"]')
      .contains('Cancel')
      .click();
  });
});
