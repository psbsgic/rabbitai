
import { getExploreLongUrl } from '.';

const createParams = () => ({
  formData: {
    datasource: 'datasource',
    viz_type: 'viz_type',
  },
  endpointType: 'endpointType',
  allowOverflow: true,
  extraSearch: { same: 'any-string' },
});

test('Should return null if formData.datasource is falsy', () => {
  const params = createParams();
  expect(
    getExploreLongUrl(
      {},
      params.endpointType,
      params.allowOverflow,
      params.extraSearch,
    ),
  ).toBeNull();
});

test('Get url when endpointType:standalone', () => {
  const params = createParams();
  expect(
    getExploreLongUrl(
      params.formData,
      params.endpointType,
      params.allowOverflow,
      params.extraSearch,
    ),
  ).toBe(
    '/rabbitai/explore/?same=any-string&form_data=%7B%22datasource%22%3A%22datasource%22%2C%22viz_type%22%3A%22viz_type%22%7D',
  );
});

test('Get url when endpointType:standalone and allowOverflow:false', () => {
  const params = createParams();
  expect(
    getExploreLongUrl(
      params.formData,
      params.endpointType,
      false,
      params.extraSearch,
    ),
  ).toBe(
    '/rabbitai/explore/?same=any-string&form_data=%7B%22datasource%22%3A%22datasource%22%2C%22viz_type%22%3A%22viz_type%22%7D',
  );
});

test('Get url when endpointType:results', () => {
  const params = createParams();
  expect(
    getExploreLongUrl(
      params.formData,
      'results',
      params.allowOverflow,
      params.extraSearch,
    ),
  ).toBe(
    '/rabbitai/explore_json/?same=any-string&form_data=%7B%22datasource%22%3A%22datasource%22%2C%22viz_type%22%3A%22viz_type%22%7D',
  );
});

test('Get url when endpointType:results and allowOverflow:false', () => {
  const params = createParams();
  expect(
    getExploreLongUrl(params.formData, 'results', false, params.extraSearch),
  ).toBe(
    '/rabbitai/explore_json/?same=any-string&form_data=%7B%22datasource%22%3A%22datasource%22%2C%22viz_type%22%3A%22viz_type%22%7D',
  );
});
