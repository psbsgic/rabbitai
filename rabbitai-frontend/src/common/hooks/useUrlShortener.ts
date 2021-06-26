import { useState, useEffect } from 'react';
import { getShortUrl as getShortUrlUtil } from 'src/utils/urlUtils';

export function useUrlShortener(url: string): Function {
  const [update, setUpdate] = useState(false);
  const [shortUrl, setShortUrl] = useState('');

  async function getShortUrl() {
    if (update) {
      const newShortUrl = await getShortUrlUtil(url);
      setShortUrl(newShortUrl);
      setUpdate(false);
      return newShortUrl;
    }
    return shortUrl;
  }

  useEffect(() => setUpdate(true), [url]);

  return getShortUrl;
}
