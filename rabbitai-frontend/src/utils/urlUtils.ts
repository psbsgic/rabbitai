import { RabbitaiClient } from '@rabbitai-ui/core';
import { getClientErrorObject } from './getClientErrorObject';

export type UrlParamType = 'string' | 'number' | 'boolean';
export function getUrlParam(paramName: string, type: 'string'): string;
export function getUrlParam(paramName: string, type: 'number'): number;
export function getUrlParam(paramName: string, type: 'boolean'): boolean;
export function getUrlParam(paramName: string, type: UrlParamType): unknown {
  const urlParam = new URLSearchParams(window.location.search).get(paramName);
  switch (type) {
    case 'number':
      if (!urlParam) {
        return null;
      }
      if (urlParam === 'true') {
        return 1;
      }
      if (urlParam === 'false') {
        return 0;
      }
      if (!Number.isNaN(Number(urlParam))) {
        return Number(urlParam);
      }
      return null;
    case 'boolean':
      if (!urlParam) {
        return null;
      }
      return urlParam !== 'false' && urlParam !== '0';
    default:
      return urlParam;
  }
}


export function getShortUrl(longUrl: string) {
  return RabbitaiClient.post({
    endpoint: '/r/shortner/',
    postPayload: { data: `/${longUrl}` }, // note: url should contain 2x '/' to redirect properly
    parseMethod: 'text',
    stringify: false, // the url saves with an extra set of string quotes without this
  })
    .then(({ text }) => text)
    .catch(response =>
      // @ts-ignore
      getClientErrorObject(response).then(({ error, statusText }) =>
        Promise.reject(error || statusText),
      ),
    );
}
