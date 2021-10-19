import {
  emptyQueryResults,
  clearQueryEditors,
} from 'src/SqlLab/utils/reduxStateToLocalStorageHelper';
import { LOCALSTORAGE_MAX_QUERY_AGE_MS } from 'src/SqlLab/constants';
import { queries, defaultQueryEditor } from '../fixtures';

describe('reduxStateToLocalStorageHelper', () => {
  const queriesObj = {};
  beforeEach(() => {
    queries.forEach(q => {
      queriesObj[q.id] = q;
    });
  });

  it('should empty query.results if query.startDttm is > LOCALSTORAGE_MAX_QUERY_AGE_MS', () => {
    // make sure sample data contains old query
    const oldQuery = queries[0];
    const { id, startDttm } = oldQuery;
    expect(Date.now() - startDttm).toBeGreaterThan(
      LOCALSTORAGE_MAX_QUERY_AGE_MS,
    );
    expect(Object.keys(oldQuery.results)).toContain('data');

    const emptiedQuery = emptyQueryResults(queriesObj);
    expect(emptiedQuery[id].startDttm).toBe(startDttm);
    expect(emptiedQuery[id].results).toEqual({});
  });

  it('should only return selected keys for query editor', () => {
    const queryEditors = [defaultQueryEditor];
    expect(Object.keys(queryEditors[0])).toContain('schemaOptions');

    const clearedQueryEditors = clearQueryEditors(queryEditors);
    expect(Object.keys(clearedQueryEditors)[0]).not.toContain('schemaOptions');
  });
});
