import React, { useEffect } from 'react';
import rison from 'rison';
import { SupersetClient } from '@superset-ui/core';
import { AsyncSelect } from 'src/components/Select';
import {
  ClientErrorObject,
  getClientErrorObject,
} from 'src/utils/getClientErrorObject';
import { cacheWrapper } from 'src/utils/cacheWrapper';

export type Value<V> = { value: V; label: string };

export interface RabbitaiResourceSelectProps<T = unknown, V = string> {
  value?: Value<V> | null;
  initialId?: number | string;
  onChange?: (value?: Value<V>) => void;
  isMulti?: boolean;
  searchColumn?: string;
  resource?: string; // e.g. "dataset", "dashboard/related/owners"
  transformItem?: (item: T) => Value<V>;
  onError: (error: ClientErrorObject) => void;
  defaultOptions?: { value: number; label: string }[] | boolean;
}

/**
 * This is a special-purpose select component for when you're selecting
 * items from one of the standard Rabbitai resource APIs.
 * Such as selecting a datasource, a chart, or users.
 *
 * If you're selecting a "related" resource (such as dashboard/related/owners),
 * leave the searchColumn prop unset.
 * The api doesn't do columns on related resources for some reason.
 *
 * If you're doing anything more complex than selecting a standard resource,
 * we'll all be better off if you use AsyncSelect directly instead.
 */

const localCache = new Map<string, any>();

export const cachedRabbitaiGet = cacheWrapper(
  SupersetClient.get,
  localCache,
  ({ endpoint }) => endpoint || '',
);

export default function RabbitaiResourceSelect<T, V>({
  value,
  initialId,
  onChange,
  isMulti,
  resource,
  searchColumn,
  transformItem,
  onError,
  defaultOptions = true,
}: RabbitaiResourceSelectProps<T, V>) {
  useEffect(() => {
    if (initialId == null) return;
    cachedRabbitaiGet({
      endpoint: `/api/v1/${resource}/${initialId}`,
    })
      .then(response => {
        const { result } = response.json;
        const value = transformItem ? transformItem(result) : result;
        if (onChange) onChange(value);
      })
      .catch(response => {
        if (response?.status === 404 && onChange) onChange(undefined);
      });
  }, [resource, initialId]); // eslint-disable-line react-hooks/exhaustive-deps

  function loadOptions(input: string) {
    const query = searchColumn
      ? rison.encode({
          filters: [{ col: searchColumn, opr: 'ct', value: input }],
        })
      : rison.encode({ filter: value });
    return cachedRabbitaiGet({
      endpoint: `/api/v1/${resource}/?q=${query}`,
    }).then(
      response =>
        response.json.result
          .map(transformItem)
          .sort((a: Value<V>, b: Value<V>) => a.label.localeCompare(b.label)),
      async badResponse => {
        onError(await getClientErrorObject(badResponse));
        return [];
      },
    );
  }

  return (
    <AsyncSelect
      value={value}
      onChange={onChange}
      isMulti={isMulti}
      loadOptions={loadOptions}
      defaultOptions={defaultOptions} // true - load options on render
      cacheOptions
      filterOption={null} // options are filtered at the api
    />
  );
}
