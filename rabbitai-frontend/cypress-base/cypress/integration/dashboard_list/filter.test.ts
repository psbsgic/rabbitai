
import { DASHBOARD_LIST } from './dashboard_list.helper';

describe('dashboard filters card view', () => {
  beforeEach(() => {
    cy.login();
    cy.visit(DASHBOARD_LIST);
    cy.get('[data-test="card-view"]').click();
  });

  it('should filter by owners correctly', () => {
    // filter by owners
    cy.get('.Select__control').first().click();
    cy.get('.Select__menu').contains('alpha user').click();
    cy.get('[data-test="styled-card"]').should('not.exist');
    cy.get('.Select__control').first().click();
    cy.get('.Select__menu').contains('gamma user').click();
    cy.get('[data-test="styled-card"]').should('not.exist');
  });

  it('should filter by me correctly', () => {
    // filter by me
    cy.get('.Select__control').first().click();
    cy.get('.Select__menu').contains('me').click();
    cy.get('[data-test="styled-card"]').its('length').should('be.gt', 0);
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__menu').contains('me').click();
    cy.get('[data-test="styled-card"]').its('length').should('be.gt', 0);
  });

  it('should filter by created by correctly', () => {
    // filter by created by
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__menu').contains('alpha user').click();
    cy.get('.ant-card').should('not.exist');
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__menu').contains('gamma user').click();
    cy.get('.ant-card').should('not.exist');
  });

  it('should filter by published correctly', () => {
    // filter by published
    cy.get('.Select__control').eq(2).click();
    cy.get('.Select__menu').contains('Published').click({ timeout: 5000 });
    cy.get('[data-test="styled-card"]').should('have.length', 2);
    cy.get('[data-test="styled-card"]')
      .first()
      .contains('USA Births Names')
      .should('be.visible');
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__control').eq(1).type('unpub{enter}');
    cy.get('[data-test="styled-card"]').should('have.length', 2);
  });
});

describe('dashboard filters list view', () => {
  beforeEach(() => {
    cy.login();
    cy.visit(DASHBOARD_LIST);
    cy.get('[data-test="list-view"]').click();
  });

  it('should filter by owners correctly', () => {
    // filter by owners
    cy.get('.Select__control').first().click();
    cy.get('.Select__menu').contains('alpha user').click();
    cy.get('[data-test="table-row"]').should('not.exist');
    cy.get('.Select__control').first().click();
    cy.get('.Select__menu').contains('gamma user').click();
    cy.get('[data-test="table-row"]').should('not.exist');
  });

  it('should filter by me correctly', () => {
    // filter by me
    cy.get('.Select__control').first().click();
    cy.get('.Select__menu').contains('me').click();
    cy.get('[data-test="table-row"]').its('length').should('be.gt', 0);
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__menu').contains('me').click();
    cy.get('[data-test="table-row"]').its('length').should('be.gt', 0);
  });

  it('should filter by created by correctly', () => {
    // filter by created by
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__menu').contains('alpha user').click();
    cy.get('[data-test="table-row"]').should('not.exist');
    cy.get('.Select__control').eq(1).click();
    cy.get('.Select__menu').contains('gamma user').click();
    cy.get('[data-test="table-row"]').should('not.exist');
  });

  xit('should filter by published correctly', () => {
    // filter by published
    cy.get('.Select__control').eq(2).click();
    cy.get('.Select__menu').contains('Published').click();
    cy.get('[data-test="table-row"]').should('have.length', 2);
    cy.get('[data-test="table-row"]')
      .first()
      .contains('USA Births Names')
      .should('be.visible');
    cy.get('.Select__control').eq(2).click();
    cy.get('.Select__control').eq(2).type('unpub{enter}');
    cy.get('[data-test="table-row"]').should('have.length', 2);
  });
});
