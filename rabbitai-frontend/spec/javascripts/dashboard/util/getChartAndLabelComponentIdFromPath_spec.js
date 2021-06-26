
import getChartAndLabelComponentIdFromPath from 'src/dashboard/util/getChartAndLabelComponentIdFromPath';

describe('getChartAndLabelComponentIdFromPath', () => {
  it('should return label and component id', () => {
    const directPathToChild = [
      'ROOT_ID',
      'TABS-aX1uNK-ryo',
      'TAB-ZRgxfD2ktj',
      'ROW-46632bc2',
      'COLUMN-XjlxaS-flc',
      'CHART-x-RMdAtlDb',
      'LABEL-region',
    ];

    expect(getChartAndLabelComponentIdFromPath(directPathToChild)).toEqual({
      label: 'LABEL-region',
      chart: 'CHART-x-RMdAtlDb',
    });
  });
});
