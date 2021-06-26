
import { getChartDataUri } from '.';

test('Get ChartUri when allowDomainSharding:false', () => {
  expect(
    getChartDataUri({
      path: '/path',
      qs: 'same-string',
      allowDomainSharding: false,
    }),
  ).toEqual({
    _deferred_build: true,
    _parts: {
      duplicateQueryParameters: false,
      escapeQuerySpace: true,
      fragment: null,
      hostname: undefined,
      password: null,
      path: '/path',
      port: '',
      preventInvalidHostname: false,
      protocol: 'http',
      query: 'same-string',
      urn: null,
      username: null,
    },
    _string: '',
  });
});

test('Get ChartUri when allowDomainSharding:true', () => {
  expect(
    getChartDataUri({
      path: '/path-allowDomainSharding-true',
      qs: 'same-string-allowDomainSharding-true',
      allowDomainSharding: true,
    }),
  ).toEqual({
    _deferred_build: true,
    _parts: {
      duplicateQueryParameters: false,
      escapeQuerySpace: true,
      fragment: null,
      hostname: undefined,
      password: null,
      path: '/path-allowDomainSharding-true',
      port: '',
      preventInvalidHostname: false,
      protocol: 'http',
      query: 'same-string-allowDomainSharding-true',
      urn: null,
      username: null,
    },
    _string: '',
  });
});
