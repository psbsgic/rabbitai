
// eslint-disable-next-line spaced-comment
/// <reference types="cypress" />
type JSONPrimitive = string | number | boolean | null;
type JSONValue = JSONPrimitive | JSONObject | JSONArray;
type JSONObject = { [member: string]: JSONValue };
type JSONArray = JSONValue[];

declare namespace Cypress {
  interface Chainable {
    /**
     * Login test user.
     */
    login(): void;

    visitChartByParams(params: string | Record<string, unknown>): cy;
    visitChartByName(name: string): cy;
    visitChartById(id: number): cy;

    /**
     * Verify slice container renders.
     */
    verifySliceContainer(chartSelector: JQuery.Selector): cy;

    /**
     * Verify slice successfully loaded.
     */
    verifySliceSuccess(options: {
      waitAlias: string;
      querySubstring?: string | RegExp;
      chartSelector?: JQuery.Selector;
    }): cy;
  }
}

declare module '@cypress/code-coverage/task';
