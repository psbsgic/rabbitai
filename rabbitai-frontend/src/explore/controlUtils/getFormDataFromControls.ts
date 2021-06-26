
import { QueryFormData } from '@rabbitai-ui/core';
import { ControlStateMapping } from '@rabbitai-ui/chart-controls';

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
