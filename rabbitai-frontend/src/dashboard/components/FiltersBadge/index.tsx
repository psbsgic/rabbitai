
import React from 'react';
import cx from 'classnames';
import Icon from 'src/components/Icon';
import Icons from 'src/components/Icons';
import DetailsPanelPopover from './DetailsPanel';
import { Pill } from './Styles';
import { Indicator } from './selectors';

export interface FiltersBadgeProps {
  appliedCrossFilterIndicators: Indicator[];
  appliedIndicators: Indicator[];
  unsetIndicators: Indicator[];
  incompatibleIndicators: Indicator[];
  onHighlightFilterSource: (path: string[]) => void;
}

const FiltersBadge = ({
  appliedCrossFilterIndicators,
  appliedIndicators,
  unsetIndicators,
  incompatibleIndicators,
  onHighlightFilterSource,
}: FiltersBadgeProps) => {
  if (
    !appliedCrossFilterIndicators.length &&
    !appliedIndicators.length &&
    !incompatibleIndicators.length &&
    !unsetIndicators.length
  ) {
    return null;
  }

  const isInactive =
    !appliedCrossFilterIndicators.length &&
    !appliedIndicators.length &&
    !incompatibleIndicators.length;

  return (
    <DetailsPanelPopover
      appliedCrossFilterIndicators={appliedCrossFilterIndicators}
      appliedIndicators={appliedIndicators}
      unsetIndicators={unsetIndicators}
      incompatibleIndicators={incompatibleIndicators}
      onHighlightFilterSource={onHighlightFilterSource}
    >
      <Pill
        className={cx(
          'filter-counts',
          !!incompatibleIndicators.length && 'has-incompatible-filters',
          !!appliedCrossFilterIndicators.length && 'has-cross-filters',
          isInactive && 'filters-inactive',
        )}
      >
        <Icon name="filter" />
        {!isInactive && (
          <span data-test="applied-filter-count">
            {appliedIndicators.length + appliedCrossFilterIndicators.length}
          </span>
        )}
        {incompatibleIndicators.length ? (
          <>
            {' '}
            <Icons.AlertSolid />
            <span data-test="incompatible-filter-count">
              {incompatibleIndicators.length}
            </span>
          </>
        ) : null}
      </Pill>
    </DetailsPanelPopover>
  );
};

export default FiltersBadge;
