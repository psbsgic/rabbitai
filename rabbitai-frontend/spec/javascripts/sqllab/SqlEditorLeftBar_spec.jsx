
import React from 'react';
import configureStore from 'redux-mock-store';
import fetchMock from 'fetch-mock';
import { shallow } from 'enzyme';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { Provider } from 'react-redux';
import '@testing-library/jest-dom/extend-expect';
import thunk from 'redux-thunk';
import SqlEditorLeftBar from 'src/SqlLab/components/SqlEditorLeftBar';
import TableElement from 'src/SqlLab/components/TableElement';
import { rabbitaiTheme, ThemeProvider } from '@rabbitai-ui/core';
import {
  table,
  initialState,
  databases,
  defaultQueryEditor,
  mockedActions,
} from './fixtures';

const mockedProps = {
  actions: mockedActions,
  tables: [table],
  queryEditor: defaultQueryEditor,
  database: databases,
  height: 0,
};
const middlewares = [thunk];
const mockStore = configureStore(middlewares);
const store = mockStore(initialState);
const DATABASE_ENDPOINT = 'glob:*/api/v1/database/?*';
fetchMock.get(DATABASE_ENDPOINT, []);
describe('SqlEditorLeftBar', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallow(<SqlEditorLeftBar {...mockedProps} />, {
      context: { store },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('is valid', () => {
    expect(React.isValidElement(<SqlEditorLeftBar {...mockedProps} />)).toBe(
      true,
    );
  });

  it('renders a TableElement', () => {
    expect(wrapper.find(TableElement)).toExist();
  });
});

describe('Left Panel Expansion', () => {
  it('table should be visible when expanded is true', () => {
    const { container } = render(
      <ThemeProvider theme={rabbitaiTheme}>
        <Provider store={store}>
          <SqlEditorLeftBar {...mockedProps} />
        </Provider>
      </ThemeProvider>,
    );
    const dbSelect = screen.getByText(/select a database/i);
    const schemaSelect = screen.getByText(/select a schema \(0\)/i);
    const dropdown = screen.getByText(/Select table/i);
    const abUser = screen.getByText(/ab_user/i);
    expect(dbSelect).toBeInTheDocument();
    expect(schemaSelect).toBeInTheDocument();
    expect(dropdown).toBeInTheDocument();
    expect(abUser).toBeInTheDocument();
    expect(
      container.querySelector('.ant-collapse-content-active'),
    ).toBeInTheDocument();
  });

  it('should toggle the table when the header is clicked', async () => {
    const collapseMock = jest.fn();
    render(
      <ThemeProvider theme={rabbitaiTheme}>
        <Provider store={store}>
          <SqlEditorLeftBar
            actions={{ ...mockedActions, collapseTable: collapseMock }}
            tables={[table]}
            queryEditor={defaultQueryEditor}
            database={databases}
            height={0}
          />
        </Provider>
      </ThemeProvider>,
    );
    const header = screen.getByText(/ab_user/);
    userEvent.click(header);
    expect(collapseMock).toHaveBeenCalled();
  });
});
