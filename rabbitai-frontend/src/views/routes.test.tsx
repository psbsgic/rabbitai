import { isFrontendRoute, routes } from './routes';

jest.mock('src/featureFlags', () => ({
  ...jest.requireActual<object>('src/featureFlags'),
  isFeatureEnabled: jest.fn().mockReturnValue(true),
}));

describe('isFrontendRoute', () => {
  it('returns true if a route matches', () => {
    routes.forEach(r => {
      expect(isFrontendRoute(r.path)).toBe(true);
    });
  });

  it('returns false if a route does not match', () => {
    expect(isFrontendRoute('/non-existent/path/')).toBe(false);
  });
});
