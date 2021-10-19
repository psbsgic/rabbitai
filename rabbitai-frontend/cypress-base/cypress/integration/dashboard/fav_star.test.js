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
        .find('span')
        .should('have.attr', 'aria-label', 'favorite-unselected');
      cy.get('[data-test="fave-unfave-icon"]').trigger('click');
      cy.get('[data-test="fave-unfave-icon"]')
        .find('span')
        .should('have.attr', 'aria-label', 'favorite-selected')
        .and('not.have.attr', 'aria-label', 'favorite-unselected');
    } else {
      cy.get('[data-test="fave-unfave-icon"]')
        .find('span')
        .should('have.attr', 'aria-label', 'favorite-unselected')
        .and('not.have.attr', 'aria-label', 'favorite-selected');
      cy.get('[data-test="fave-unfave-icon"]').trigger('click');
      cy.get('[data-test="fave-unfave-icon"]')
        .find('span')
        .should('have.attr', 'aria-label', 'favorite-unselected')
        .and('not.have.attr', 'aria-label', 'favorite-selected');
    }

    // reset to original fav state
    cy.get('[data-test="fave-unfave-icon"]').trigger('click');
  });
});
