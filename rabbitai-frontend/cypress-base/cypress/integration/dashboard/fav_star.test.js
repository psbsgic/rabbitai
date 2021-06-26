
import {
  WORLD_HEALTH_DASHBOARD,
  CHECK_DASHBOARD_FAVORITE_ENDPOINT,
} from './dashboard.helper';

describe('Dashboard add to favorite', () => {
  let isFavoriteDashboard = false;

  beforeEach(() => {
    cy.login();

    cy.intercept(CHECK_DASHBOARD_FAVORITE_ENDPOINT).as('countFavStar');
    cy.visit(WORLD_HEALTH_DASHBOARD);

    cy.wait('@countFavStar').then(xhr => {
      isFavoriteDashboard = xhr.response.body.count === 1;
    });
  });

  it('should allow favor/unfavor', () => {
    if (!isFavoriteDashboard) {
      cy.get('[data-test="fave-unfave-icon"]')
        .find('svg')
        .should('have.attr', 'data-test', 'favorite-unselected');
      cy.get('[data-test="fave-unfave-icon"]').trigger('click');
      cy.get('[data-test="fave-unfave-icon"]')
        .find('svg')
        .should('have.attr', 'data-test', 'favorite-selected')
        .and('not.have.attr', 'data-test', 'favorite-unselected');
    } else {
      cy.get('[data-test="fave-unfave-icon"]')
        .find('svg')
        .should('have.attr', 'data-test', 'favorite-unselected')
        .and('not.have.attr', 'data-test', 'favorite-selected');
      cy.get('[data-test="fave-unfave-icon"]').trigger('click');
      cy.get('[data-test="fave-unfave-icon"]')
        .find('svg')
        .should('have.attr', 'data-test', 'favorite-unselected')
        .and('not.have.attr', 'data-test', 'favorite-selected');
    }

    // reset to original fav state
    cy.get('[data-test="fave-unfave-icon"]').trigger('click');
  });
});
