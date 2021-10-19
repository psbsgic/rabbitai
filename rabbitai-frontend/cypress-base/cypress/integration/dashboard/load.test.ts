import {
  waitForChartLoad,
  WORLD_HEALTH_CHARTS,
  WORLD_HEALTH_DASHBOARD,
} from './dashboard.helper';

describe('Dashboard load', () => {
  beforeEach(() => {
    cy.login();
  });

  it('should load dashboard', () => {
    cy.visit(WORLD_HEALTH_DASHBOARD);
    WORLD_HEALTH_CHARTS.forEach(waitForChartLoad);
  });

  it('should load in edit mode', () => {
    cy.visit(`${WORLD_HEALTH_DASHBOARD}?edit=true&standalone=true`);
    cy.get('[data-test="discard-changes-button"]').should('be.visible');
  });

  it('should load in standalone mode', () => {
    cy.visit(`${WORLD_HEALTH_DASHBOARD}?edit=true&standalone=true`);
    cy.get('#app-menu').should('not.exist');
  });

  it('should load in edit/standalone mode', () => {
    cy.visit(`${WORLD_HEALTH_DASHBOARD}?edit=true&standalone=true`);
    cy.get('[data-test="discard-changes-button"]').should('be.visible');
    cy.get('#app-menu').should('not.exist');
  });

  it('should send log data', () => {
    cy.visit(WORLD_HEALTH_DASHBOARD);
    cy.intercept('/rabbitai/log/?explode=events&dashboard_id=*');
  });
});
