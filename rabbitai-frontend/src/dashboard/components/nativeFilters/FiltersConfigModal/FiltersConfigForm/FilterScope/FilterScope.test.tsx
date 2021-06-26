
import React from 'react';
import { Provider } from 'react-redux';
import {
  render,
  screen,
  fireEvent,
  waitFor,
} from 'spec/helpers/testing-library';
import { mockStoreWithChartsInTabsAndRoot } from 'spec/fixtures/mockStore';
import { Form, FormInstance } from 'src/common/components';
import { NativeFiltersForm } from 'src/dashboard/components/nativeFilters/FiltersConfigModal/types';
import FiltersConfigForm from 'src/dashboard/components/nativeFilters/FiltersConfigModal/FiltersConfigForm/FiltersConfigForm';

describe('FilterScope', () => {
  const save = jest.fn();
  let form: FormInstance<NativeFiltersForm>;
  const mockedProps = {
    filterId: 'DefaultFilterId',
    restoreFilter: jest.fn(),
    parentFilters: [],
    save,
  };

  const MockModal = ({ scope }: { scope?: object }) => {
    const [newForm] = Form.useForm<NativeFiltersForm>();
    form = newForm;
    if (scope) {
      form.setFieldsValue({
        filters: {
          [mockedProps.filterId]: {
            scope,
          },
        },
      });
    }
    return (
      <Provider store={mockStoreWithChartsInTabsAndRoot}>
        <Form form={form}>
          <FiltersConfigForm form={form} {...mockedProps} />
        </Form>
      </Provider>
    );
  };

  const getTreeSwitcher = (order = 0) =>
    document.querySelectorAll('.ant-tree-switcher')[order];

  it('renders "apply to all" filter scope', () => {
    render(<MockModal />);
    expect(screen.queryByRole('tree')).not.toBeInTheDocument();
  });

  it('select tree values with 1 excluded', async () => {
    render(<MockModal />);
    fireEvent.click(screen.getByText('Scoping'));
    fireEvent.click(screen.getByLabelText('Apply to specific panels'));
    expect(screen.getByRole('tree')).not.toBe(null);
    fireEvent.click(getTreeSwitcher(2));
    fireEvent.click(screen.getByText('CHART_ID2'));
    await waitFor(() =>
      expect(
        form.getFieldValue('filters')?.[mockedProps.filterId].scope,
      ).toEqual({
        excluded: [20],
        rootPath: ['ROOT_ID'],
      }),
    );
  });

  it('select 1 value only', async () => {
    render(<MockModal />);
    fireEvent.click(screen.getByText('Scoping'));
    fireEvent.click(screen.getByLabelText('Apply to specific panels'));
    expect(screen.getByRole('tree')).not.toBe(null);
    fireEvent.click(getTreeSwitcher(2));
    fireEvent.click(screen.getByText('CHART_ID2'));
    fireEvent.click(screen.getByText('tab1'));
    await waitFor(() =>
      expect(
        form.getFieldValue('filters')?.[mockedProps.filterId].scope,
      ).toEqual({
        excluded: [18, 20],
        rootPath: ['ROOT_ID'],
      }),
    );
  });

  it('correct init tree with values', async () => {
    render(
      <MockModal
        scope={{
          rootPath: ['TAB_ID'],
          excluded: [],
        }}
      />,
    );
    fireEvent.click(screen.getByText('Scoping'));
    fireEvent.click(screen.getByLabelText('Apply to specific panels'));

    await waitFor(() => {
      expect(screen.getByRole('tree')).toBeInTheDocument();
      expect(
        document.querySelectorAll('.ant-tree-checkbox-checked').length,
      ).toBe(1);
    });
  });
});
