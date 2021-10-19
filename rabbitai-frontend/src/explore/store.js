/* eslint camelcase: 0 */
import { getChartControlPanelRegistry } from '@superset-ui/core';
import { getAllControlsState, getFormDataFromControls } from './controlUtils';
import { controls } from './controls';

/**
 * 处理弃用控件。
 *
 * @param formData
 */
function handleDeprecatedControls(formData) {
  // Reacffectation / handling of deprecated controls
  /* eslint-disable no-param-reassign */

  // y_axis_zero was a boolean forcing 0 to be part of the Y Axis
  if (formData.y_axis_zero) {
    formData.y_axis_bounds = [0, null];
  }
}

/**
 * 获取控件状态。获取设置到状态中的控件对象。控件对象类似于配置控件，仅与当前可视类型相关，实现 mapStateToProps 函数，
 * 添加来自输入数据表单的值键。这还不能成为操作创建者，因为它在“浏览”和“仪表板”视图中都有使用。
 *
 * @param state 状态对象。
 * @param inputFormData 输入数据表单。
 *
 * @returns {{}|*}
 */
export function getControlsState(state, inputFormData) {
  /*
   * Gets a new controls object to put in the state. The controls object
   * is similar to the configuration control with only the controls
   * related to the current viz_type, materializes mapStateToProps functions,
   * adds value keys coming from inputFormData passed here. This can't be an action creator
   * just yet because it's used in both the explore and dashboard views.
   * */

  // Getting a list of active control names for the current viz
  const formData = { ...inputFormData };
  const vizType =
    formData.viz_type || state.common.conf.DEFAULT_VIZ_TYPE || 'table';

  handleDeprecatedControls(formData);

  const controlsState = getAllControlsState(
    vizType,
    state.datasource.type,
    state,
    formData,
  );

  const controlPanelConfig = getChartControlPanelRegistry().get(vizType) || {};
  if (controlPanelConfig.onInit) {
    return controlPanelConfig.onInit(controlsState);
  }

  return controlsState;
}

/**
 * 将指定表单数据设置为默认表单数据。
 *
 * @param inputFormData 表单数据。
 * @returns {{}}
 */
export function applyDefaultFormData(inputFormData) {
  const datasourceType = inputFormData.datasource.split('__')[1];
  const vizType = inputFormData.viz_type;
  const controlsState = getAllControlsState(vizType, datasourceType, null, {
    ...inputFormData,
  });
  const controlFormData = getFormDataFromControls(controlsState);

  const formData = {};
  Object.keys(controlsState)
    .concat(Object.keys(inputFormData))
    .forEach(controlName => {
      if (inputFormData[controlName] === undefined) {
        formData[controlName] = controlFormData[controlName];
      } else {
        formData[controlName] = inputFormData[controlName];
      }
    });

  return formData;
}

const defaultControls = { ...controls };
Object.keys(controls).forEach(f => {
  defaultControls[f].value = controls[f].default;
});

const defaultState = {
  controls: defaultControls,
  form_data: getFormDataFromControls(defaultControls),
};

export { defaultControls, defaultState };
