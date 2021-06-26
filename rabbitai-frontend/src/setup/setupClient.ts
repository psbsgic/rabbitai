
import { RabbitaiClient, logging } from '@rabbitai-ui/core';
import parseCookie from 'src/utils/parseCookie';

export default function setupClient() {
  const csrfNode = document.querySelector<HTMLInputElement>('#csrf_token');
  const csrfToken = csrfNode?.value;

  // when using flask-jwt-extended csrf is set in cookies
  const cookieCSRFToken = parseCookie().csrf_access_token || '';

  RabbitaiClient.configure({
    protocol: ['http:', 'https:'].includes(window?.location?.protocol)
      ? (window?.location?.protocol as 'http:' | 'https:')
      : undefined,
    host: (window.location && window.location.host) || '',
    csrfToken: csrfToken || cookieCSRFToken,
  })
    .init()
    .catch(error => {
      logging.warn('Error initializing RabbitaiClient', error);
    });
}
