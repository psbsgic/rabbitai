import React from 'react';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import fetchMock from 'fetch-mock';
import * as featureFlags from 'src/featureFlags';
import { Provider } from 'react-redux';
import { supersetTheme, ThemeProvider } from '@superset-ui/core';
import { render, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import userEvent from '@testing-library/user-event';
import * as utils from 'src/utils/common';
import ShareSqlLabQuery from 'src/SqlLab/components/ShareSqlLabQuery';

const mockStore = configureStore([thunk]);
const store = mockStore({});
let isFeatureEnabledMock;

const standardProvider = ({ children }) => (
  <ThemeProvider theme={supersetTheme}>
    <Provider store={store}>{children}</Provider>
  </ThemeProvider>
);

const defaultProps = {
  queryEditor: {
    dbId: 0,
    title: 'query title',
    schema: 'query_schema',
    autorun: false,
    sql: 'SELECT * FROM ...',
    remoteId: 999,
  },
  addDangerToast: jest.fn(),
};

describe('ShareSqlLabQuery', () => {
  const storeQueryUrl = 'glob:*/kv/store/';
  const storeQueryMockId = '123';

  beforeEach(async () => {
    fetchMock.post(storeQueryUrl, () => ({ id: storeQueryMockId }), {
      overwriteRoutes: true,
    });
    fetchMock.resetHistory();
    jest.clearAllMocks();
  });

  afterAll(fetchMock.reset);

  describe('via /kv/store', () => {
    beforeAll(() => {
      isFeatureEnabledMock = jest
        .spyOn(featureFlags, 'isFeatureEnabled')
        .mockImplementation(() => true);
    });

    afterAll(() => {
      isFeatureEnabledMock.restore();
    });

    it('calls storeQuery() with the query when getCopyUrl() is called', async () => {
      await act(async () => {
        render(<ShareSqlLabQuery {...defaultProps} />, {
          wrapper: standardProvider,
        });
      });
      const button = screen.getByRole('button');
      const storeQuerySpy = jest.spyOn(utils, 'storeQuery');
      userEvent.click(button);
      expect(storeQuerySpy.mock.calls).toHaveLength(1);
      storeQuerySpy.mockRestore();
    });
  });

  describe('via saved query', () => {
    beforeAll(() => {
      isFeatureEnabledMock = jest
        .spyOn(featureFlags, 'isFeatureEnabled')
        .mockImplementation(() => false);
    });

    afterAll(() => {
      isFeatureEnabledMock.restore();
    });

    it('does not call storeQuery() with the query when getCopyUrl() is called and feature is not enabled', async () => {
      await act(async () => {
        render(<ShareSqlLabQuery {...defaultProps} />, {
          wrapper: standardProvider,
        });
      });
      const storeQuerySpy = jest.spyOn(utils, 'storeQuery');
      const button = screen.getByRole('button');
      userEvent.click(button);
      expect(storeQuerySpy.mock.calls).toHaveLength(0);
      storeQuerySpy.mockRestore();
    });

    it('button is disabled and there is a request to save the query', async () => {
      const updatedProps = {
        queryEditor: {
          ...defaultProps.queryEditor,
          remoteId: undefined,
        },
      };

      render(<ShareSqlLabQuery {...updatedProps} />, {
        wrapper: standardProvider,
      });
      const button = await screen.findByRole('button', { name: /copy link/i });
      expect(button).toBeDisabled();
    });
  });
});
