
import React, { FC } from 'react';
import { styled, t } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import { useSelector } from 'react-redux';
import EditableTitle from 'src/components/EditableTitle';
import SliceHeaderControls from 'src/dashboard/components/SliceHeaderControls';
import FiltersBadge from 'src/dashboard/containers/FiltersBadge';
import Icon from 'src/components/Icon';
import { RootState } from 'src/dashboard/types';
import { Slice } from 'src/types/Chart';
import FilterIndicator from 'src/dashboard/components/FiltersBadge/FilterIndicator';

type SliceHeaderProps = {
  innerRef?: string;
  slice: Slice;
  isExpanded?: boolean;
  isCached?: boolean[];
  cachedDttm?: string[];
  updatedDttm?: number;
  updateSliceName?: (arg0: string) => void;
  toggleExpandSlice?: Function;
  forceRefresh?: Function;
  exploreChart?: Function;
  exportCSV?: Function;
  editMode?: boolean;
  isFullSize?: boolean;
  annotationQuery?: object;
  annotationError?: object;
  sliceName?: string;
  rabbitaiCanExplore?: boolean;
  rabbitaiCanShare?: boolean;
  rabbitaiCanCSV?: boolean;
  sliceCanEdit?: boolean;
  componentId: string;
  dashboardId: number;
  filters: object;
  addSuccessToast: Function;
  addDangerToast: Function;
  handleToggleFullSize: Function;
  chartStatus: string;
  formData: object;
};

const annotationsLoading = t('Annotation layers are still loading.');
const annotationsError = t('One ore more annotation layers failed loading.');

const CrossFilterIcon = styled(Icon)`
  fill: ${({ theme }) => theme.colors.grayscale.light5};
  & circle {
    fill: ${({ theme }) => theme.colors.primary.base};
  }
`;

const SliceHeader: FC<SliceHeaderProps> = ({
  innerRef = null,
  forceRefresh = () => ({}),
  updateSliceName = () => ({}),
  toggleExpandSlice = () => ({}),
  exploreChart = () => ({}),
  exportCSV = () => ({}),
  editMode = false,
  annotationQuery = {},
  annotationError = {},
  cachedDttm = null,
  updatedDttm = null,
  isCached = [],
  isExpanded = [],
  sliceName = '',
  rabbitaiCanExplore = false,
  rabbitaiCanShare = false,
  rabbitaiCanCSV = false,
  sliceCanEdit = false,
  slice,
  componentId,
  dashboardId,
  addSuccessToast,
  addDangerToast,
  handleToggleFullSize,
  isFullSize,
  chartStatus,
  formData,
}) => {
  // TODO: change to indicator field after it will be implemented
  const crossFilterValue = useSelector<RootState, any>(
    state => state.dataMask[slice?.slice_id]?.filterState?.value,
  );

  return (
    <div className="chart-header" data-test="slice-header" ref={innerRef}>
      <div className="header-title">
        <EditableTitle
          title={
            sliceName ||
            (editMode
              ? '---' // this makes an empty title clickable
              : '')
          }
          canEdit={editMode}
          emptyText=""
          onSaveTitle={updateSliceName}
          showTooltip={false}
        />
        {!!Object.values(annotationQuery).length && (
          <Tooltip
            id="annotations-loading-tooltip"
            placement="top"
            title={annotationsLoading}
          >
            <i
              role="img"
              aria-label={annotationsLoading}
              className="fa fa-refresh warning"
            />
          </Tooltip>
        )}
        {!!Object.values(annotationError).length && (
          <Tooltip
            id="annoation-errors-tooltip"
            placement="top"
            title={annotationsError}
          >
            <i
              role="img"
              aria-label={annotationsError}
              className="fa fa-exclamation-circle danger"
            />
          </Tooltip>
        )}
      </div>
      <div className="header-controls">
        {!editMode && (
          <>
            {crossFilterValue && (
              <Tooltip
                placement="top"
                title={
                  <FilterIndicator
                    indicator={{
                      value: crossFilterValue,
                      name: t('Emitted values'),
                    }}
                  />
                }
              >
                <CrossFilterIcon name="cross-filter-badge" />
              </Tooltip>
            )}
            <FiltersBadge chartId={slice.slice_id} />
            <SliceHeaderControls
              slice={slice}
              isCached={isCached}
              isExpanded={isExpanded}
              cachedDttm={cachedDttm}
              updatedDttm={updatedDttm}
              toggleExpandSlice={toggleExpandSlice}
              forceRefresh={forceRefresh}
              exploreChart={exploreChart}
              exportCSV={exportCSV}
              rabbitaiCanExplore={rabbitaiCanExplore}
              rabbitaiCanShare={rabbitaiCanShare}
              rabbitaiCanCSV={rabbitaiCanCSV}
              sliceCanEdit={sliceCanEdit}
              componentId={componentId}
              dashboardId={dashboardId}
              addSuccessToast={addSuccessToast}
              addDangerToast={addDangerToast}
              handleToggleFullSize={handleToggleFullSize}
              isFullSize={isFullSize}
              chartStatus={chartStatus}
              formData={formData}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default SliceHeader;
