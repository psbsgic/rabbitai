import parseCookie from 'src/utils/parseCookie';
import rison from 'rison';
import shortid from 'shortid';

export default function handleResourceExport(
  resource: string,
  ids: number[],
  done: () => void,
  interval = 200,
): void {
  const token = shortid.generate();
  const url = `/api/v1/${resource}/export/?q=${rison.encode(
    ids,
  )}&token=${token}`;

  // create new iframe for export
  const iframe = document.createElement('iframe');
  iframe.style.display = 'none';
  iframe.src = url;
  document.body.appendChild(iframe);

  const timer = window.setInterval(() => {
    const cookie: { [cookieId: string]: string } = parseCookie();
    if (cookie[token] === 'done') {
      window.clearInterval(timer);
      document.body.removeChild(iframe);
      done();
    }
  }, interval);
}
