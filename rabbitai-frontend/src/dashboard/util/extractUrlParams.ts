import querystring from 'query-string';
import { JsonObject } from '@superset-ui/core';

const reservedQueryParams = new Set(['standalone', 'edit']);

export type UrlParamType = 'reserved' | 'regular' | 'all';

/**
 * Returns the url params that are used to customize queries
 */
export default function extractUrlParams(
  urlParamType: UrlParamType,
): JsonObject {
  const queryParams = querystring.parse(window.location.search);
  return Object.entries(queryParams).reduce((acc, [key, value]) => {
    if (
      (urlParamType === 'regular' && reservedQueryParams.has(key)) ||
      (urlParamType === 'reserved' && !reservedQueryParams.has(key))
    )
      return acc;
    // if multiple url params share the same key (?foo=bar&foo=baz), they will appear as an array.
    // Only one value can be used for a given query param, so we just take the first one.
    if (Array.isArray(value)) {
      return {
        ...acc,
        [key]: value[0],
      };
    }
    return { ...acc, [key]: value };
  }, {});
}
