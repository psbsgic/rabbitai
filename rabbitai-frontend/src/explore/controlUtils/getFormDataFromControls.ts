import { QueryFormData } from '@superset-ui/core';
import { ControlStateMapping } from '@superset-ui/chart-controls';

/**
 * 从控件中获取表单数据。
 *
 * @param controlsState 控件状态。
 */
export function getFormDataFromControls(
  controlsState: ControlStateMapping,
): QueryFormData {
  const formData: QueryFormData = {
    viz_type: 'table',
    datasource: '',
  };
  Object.keys(controlsState).forEach(controlName => {
    const control = controlsState[controlName];
    formData[controlName] = control.value;
  });
  return formData;
}
