
import { LOCALSTORAGE_MAX_QUERY_AGE_MS } from '../constants';

const PERSISTENT_QUERY_EDITOR_KEYS = new Set([
  'remoteId',
  'autorun',
  'dbId',
  'height',
  'id',
  'latestQueryId',
  'northPercent',
  'queryLimit',
  'schema',
  'selectedText',
  'southPercent',
  'sql',
  'templateParams',
  'title',
  'hideLeftBar',
]);

export function emptyQueryResults(queries) {
  return Object.keys(queries).reduce((accu, key) => {
    const { startDttm, results } = queries[key];
    const query = {
      ...queries[key],
      results:
        Date.now() - startDttm > LOCALSTORAGE_MAX_QUERY_AGE_MS ? {} : results,
    };

    const updatedQueries = {
      ...accu,
      [key]: query,
    };
    return updatedQueries;
  }, {});
}

export function clearQueryEditors(queryEditors) {
  return queryEditors.map(editor =>
    // only return selected keys
    Object.keys(editor)
      .filter(key => PERSISTENT_QUERY_EDITOR_KEYS.has(key))
      .reduce(
        (accumulator, key) => ({
          ...accumulator,
          [key]: editor[key],
        }),
        {},
      ),
  );
}
