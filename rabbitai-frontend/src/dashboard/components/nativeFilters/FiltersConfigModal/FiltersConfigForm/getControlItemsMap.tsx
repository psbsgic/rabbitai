
import {
  CustomControlItem,
  InfoTooltipWithTrigger,
} from '@rabbitai-ui/chart-controls';
import React from 'react';
import { Checkbox } from 'src/common/components';
import { FormInstance } from 'antd/lib/form';
import { getChartControlPanelRegistry, t } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import { getControlItems, setNativeFilterFieldValues } from './utils';
import { NativeFiltersForm } from '../types';
import { StyledRowFormItem } from './FiltersConfigForm';
import { Filter } from '../../types';

export interface ControlItemsProps {
  disabled: boolean;
  forceUpdate: Function;
  form: FormInstance<NativeFiltersForm>;
  filterId: string;
  filterType: string;
  filterToEdit?: Filter;
}

export default function getControlItemsMap({
  disabled,
  forceUpdate,
  form,
  filterId,
  filterType,
  filterToEdit,
}: ControlItemsProps) {
  const controlPanelRegistry = getChartControlPanelRegistry();
  const controlItems =
    getControlItems(controlPanelRegistry.get(filterType)) ?? [];
  const map = {};

  controlItems
    .filter(
      (controlItem: CustomControlItem) =>
        controlItem?.config?.renderTrigger &&
        controlItem.name !== 'sortAscending',
    )
    .forEach(controlItem => {
      const element = (
        <Tooltip
          key={controlItem.name}
          placement="left"
          title={
            controlItem.config.affectsDataMask &&
            disabled &&
            t('Populate "Default value" to enable this control')
          }
        >
          <StyledRowFormItem
            key={controlItem.name}
            name={['filters', filterId, 'controlValues', controlItem.name]}
            initialValue={
              filterToEdit?.controlValues?.[controlItem.name] ??
              controlItem?.config?.default
            }
            valuePropName="checked"
            colon={false}
          >
            <Checkbox
              disabled={controlItem.config.affectsDataMask && disabled}
              onChange={() => {
                if (!controlItem.config.resetConfig) {
                  forceUpdate();
                  return;
                }
                setNativeFilterFieldValues(form, filterId, {
                  defaultDataMask: null,
                });
                forceUpdate();
              }}
            >
              {controlItem.config.label}{' '}
              {controlItem.config.description && (
                <InfoTooltipWithTrigger
                  placement="top"
                  label={controlItem.config.name}
                  tooltip={controlItem.config.description}
                />
              )}
            </Checkbox>
          </StyledRowFormItem>
        </Tooltip>
      );
      map[controlItem.name] = element;
    });
  return map;
}
