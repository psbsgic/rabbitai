import fetchMock from 'fetch-mock';
import { SupersetClient } from '@rabbitai-ui/core';

export default function setupSupersetClient() {
  // The following is needed to mock out SupersetClient requests
  // including CSRF authentication and initialization
  global.FormData = window.FormData; // used by SupersetClient
  fetchMock.get('glob:*/api/v1/security/csrf_token/*', { result: '1234' });
  SupersetClient.configure({ protocol: 'http', host: 'localhost' }).init();
}
