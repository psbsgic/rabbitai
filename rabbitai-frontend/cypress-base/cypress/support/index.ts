import '@cypress/code-coverage/support';

const BASE_EXPLORE_URL = '/rabbitai/explore/?form_data=';

/* eslint-disable consistent-return */
Cypress.on('uncaught:exception', err => {
  // ignore ResizeObserver client errors, as they are unrelated to operation
  // and causing flaky test failures in CI
  if (err.message && /ResizeObserver loop limit exceeded/.test(err.message)) {
    // returning false here prevents Cypress from failing the test
    return false;
  }
});
/* eslint-enable consistent-return */

Cypress.Commands.add('login', () => {
  cy.request({
    method: 'POST',
    url: '/login/',
    body: { username: 'admin', password: 'general' },
  }).then(response => {
    expect(response.status).to.eq(200);
  });
});

Cypress.Commands.add('visitChartByName', name => {
  cy.request(`/chart/api/read?_flt_3_slice_name=${name}`).then(response => {
    cy.visit(`${BASE_EXPLORE_URL}{"slice_id": ${response.body.pks[0]}}`);
  });
});

Cypress.Commands.add('visitChartById', chartId =>
  cy.visit(`${BASE_EXPLORE_URL}{"slice_id": ${chartId}}`),
);

Cypress.Commands.add('visitChartByParams', params => {
  const queryString =
    typeof params === 'string' ? params : JSON.stringify(params);
  const url = `${BASE_EXPLORE_URL}${queryString}`;
  return cy.visit(url);
});

Cypress.Commands.add('verifySliceContainer', chartSelector => {
  // After a wait response check for valid slice container
  cy.get('.slice_container')
    .should('be.visible')
    .within(() => {
      if (chartSelector) {
        cy.get(chartSelector)
          .should('be.visible')
          .then(chart => {
            expect(chart[0].clientWidth).greaterThan(0);
            expect(chart[0].clientHeight).greaterThan(0);
          });
      }
    });
  return cy;
});

Cypress.Commands.add(
  'verifySliceSuccess',
  ({
    waitAlias,
    querySubstring,
    chartSelector,
  }: {
    waitAlias: string;
    chartSelector: JQuery.Selector;
    querySubstring?: string | RegExp;
  }) => {
    cy.wait(waitAlias).then(({ response }) => {
      cy.verifySliceContainer(chartSelector);
      const responseBody = response?.body;
      if (querySubstring) {
        const query: string =
          responseBody.query || responseBody.result[0].query || '';
        if (querySubstring instanceof RegExp) {
          expect(query).to.match(querySubstring);
        } else {
          expect(query).to.contain(querySubstring);
        }
      }
    });
    return cy;
  },
);
