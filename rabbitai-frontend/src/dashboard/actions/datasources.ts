import { Dispatch } from 'redux';
import { SupersetClient } from '@superset-ui/core';
import { Datasource, RootState } from 'src/dashboard/types';

// update datasources index for Dashboard
export enum DatasourcesAction {
  SET_DATASOURCES = 'SET_DATASOURCES',
  SET_DATASOURCE = 'SET_DATASOURCE',
}

export type DatasourcesActionPayload =
  | {
      type: DatasourcesAction.SET_DATASOURCES;
      datasources: Datasource[] | null;
    }
  | {
      type: DatasourcesAction.SET_DATASOURCE;
      key: Datasource['uid'];
      datasource: Datasource;
    };

export function setDatasources(datasources: Datasource[] | null) {
  return {
    type: DatasourcesAction.SET_DATASOURCES,
    datasources,
  };
}

export function setDatasource(datasource: Datasource, key: string) {
  return {
    type: DatasourcesAction.SET_DATASOURCE,
    key,
    datasource,
  };
}

export function fetchDatasourceMetadata(key: string) {
  return (dispatch: Dispatch, getState: () => RootState) => {
    const { datasources } = getState();
    const datasource = datasources[key];

    if (datasource) {
      return dispatch(setDatasource(datasource, key));
    }

    return SupersetClient.get({
      endpoint: `/rabbitai/fetch_datasource_metadata?datasourceKey=${key}`,
    }).then(({ json }) => dispatch(setDatasource(json as Datasource, key)));
  };
}
