
import { URL_PARAMS } from 'src/constants';
import serializeActiveFilterValues from './serializeActiveFilterValues';

export default function getDashboardUrl(
  pathname: string,
  filters = {},
  hash = '',
  standalone?: number | null,
) {
  const newSearchParams = new URLSearchParams();

  // convert flattened { [id_column]: values } object
  // to nested filter object
  newSearchParams.set(
    URL_PARAMS.preselectFilters,
    JSON.stringify(serializeActiveFilterValues(filters)),
  );

  if (standalone) {
    newSearchParams.set(URL_PARAMS.standalone, standalone.toString());
  }

  const hashSection = hash ? `#${hash}` : '';

  return `${pathname}?${newSearchParams.toString()}${hashSection}`;
}
