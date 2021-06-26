
import { getExploreUrl } from '.';

const createParams = () => ({
  formData: {
    datasource: 'datasource',
    viz_type: 'viz_type',
  },
  endpointType: 'base',
  force: false,
  curUrl: null,
  requestParams: {},
  allowDomainSharding: false,
  method: 'POST',
});

test('Get ExploreUrl with default params', () => {
  const params = createParams();
  expect(getExploreUrl(params)).toBe('http:///rabbitai/explore/');
});

test('Get ExploreUrl with endpointType:full', () => {
  const params = createParams();
  expect(getExploreUrl({ ...params, endpointType: 'full' })).toBe(
    'http:///rabbitai/explore_json/',
  );
});

test('Get ExploreUrl with endpointType:full and method:GET', () => {
  const params = createParams();
  expect(
    getExploreUrl({ ...params, endpointType: 'full', method: 'GET' }),
  ).toBe('http:///rabbitai/explore_json/');
});
