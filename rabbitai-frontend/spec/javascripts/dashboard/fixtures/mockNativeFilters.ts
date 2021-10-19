import { DataMaskStateWithId } from 'src/dataMask/types';
import { NativeFiltersState } from 'src/dashboard/reducers/types';

export const mockDataMaskInfo: DataMaskStateWithId = {
  DefaultsID: {
    id: 'DefaultId',
    ownState: {},
    filterState: {
      value: [],
    },
  },
};

export const nativeFiltersInfo: NativeFiltersState = {
  filterSets: {
    'set-id': {
      id: 'DefaultsID',
      name: 'Set name',
      nativeFilters: {},
      dataMask: mockDataMaskInfo,
    },
  },
  filters: {
    DefaultsID: {
      cascadeParentIds: [],
      id: 'DefaultsID',
      name: 'test',
      filterType: 'filter_select',
      targets: [
        {
          datasetId: 0,
          column: {
            name: 'test column',
            displayName: 'test column',
          },
        },
      ],
      defaultDataMask: {
        filterState: {
          value: null,
        },
      },
      scope: {
        rootPath: [],
        excluded: [],
      },
      controlValues: {
        allowsMultipleValues: true,
        isRequired: false,
      },
    },
  },
};
