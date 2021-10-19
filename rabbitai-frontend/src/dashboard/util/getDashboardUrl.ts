import rison from 'rison';
import { JsonObject } from '@superset-ui/core';
import { URL_PARAMS } from 'src/constants';
import replaceUndefinedByNull from './replaceUndefinedByNull';
import serializeActiveFilterValues from './serializeActiveFilterValues';
import { DataMaskState } from '../../dataMask/types';

export default function getDashboardUrl({
  pathname,
  filters = {},
  hash = '',
  standalone,
  dataMask,
}: {
  pathname: string;
  filters: JsonObject;
  hash: string;
  standalone?: number | null;
  dataMask?: DataMaskState;
}) {
  const newSearchParams = new URLSearchParams();

  // convert flattened { [id_column]: values } object
  // to nested filter object
  newSearchParams.set(
    URL_PARAMS.preselectFilters.name,
    JSON.stringify(serializeActiveFilterValues(filters)),
  );

  if (standalone) {
    newSearchParams.set(URL_PARAMS.standalone.name, standalone.toString());
  }

  if (dataMask) {
    newSearchParams.set(
      URL_PARAMS.nativeFilters.name,
      rison.encode(replaceUndefinedByNull(dataMask)),
    );
  }

  const hashSection = hash ? `#${hash}` : '';
  return `${pathname}?${newSearchParams.toString()}${hashSection}`;
}
