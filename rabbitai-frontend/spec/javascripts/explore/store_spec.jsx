import { getChartControlPanelRegistry } from '@superset-ui/core';
import { applyDefaultFormData } from 'src/explore/store';

describe('store', () => {
  beforeAll(() => {
    getChartControlPanelRegistry().registerValue('test-chart', {
      controlPanelSections: [
        {
          label: 'Test section',
          expanded: true,
          controlSetRows: [['row_limit']],
        },
      ],
    });
  });

  afterAll(() => {
    getChartControlPanelRegistry().remove('test-chart');
  });

  describe('applyDefaultFormData', () => {
    window.featureFlags = {
      SCOPED_FILTER: false,
    };

    it('applies default to formData if the key is missing', () => {
      const inputFormData = {
        datasource: '11_table',
        viz_type: 'test-chart',
      };
      let outputFormData = applyDefaultFormData(inputFormData);
      expect(outputFormData.row_limit).toEqual(10000);

      const inputWithRowLimit = {
        ...inputFormData,
        row_limit: 888,
      };
      outputFormData = applyDefaultFormData(inputWithRowLimit);
      expect(outputFormData.row_limit).toEqual(888);
    });

    it('keeps null if key is defined with null', () => {
      const inputFormData = {
        datasource: '11_table',
        viz_type: 'test-chart',
        row_limit: null,
      };
      const outputFormData = applyDefaultFormData(inputFormData);
      expect(outputFormData.row_limit).toBe(null);
    });
  });
});
