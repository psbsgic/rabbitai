import { ReactNode } from 'react';
import {
  DatasourceType,
  ensureIsArray,
  JsonValue,
  QueryFormData,
} from '@superset-ui/core';
import {
  ControlConfig,
  ControlPanelState,
  ControlState,
  ControlType,
  ControlValueValidator,
} from '@superset-ui/chart-controls';
import { getSectionsToRender } from './getSectionsToRender';
import { getControlConfig } from './getControlConfig';

type ValidationError = JsonValue;

/**
 * 执行控件验证。
 *
 * @param control
 * @param processedState
 */
function execControlValidator<T = ControlType>(
  control: ControlState<T>,
  processedState: ControlState<T>,
) {
  const validators = control.validators as ControlValueValidator[] | undefined;
  const { externalValidationErrors = [] } = control;
  const errors: ValidationError[] = [];
  if (validators && validators.length > 0) {
    validators.forEach(validator => {
      const error = validator.call(control, control.value, processedState);
      if (error) {
        errors.push(error);
      }
    });
  }
  const validationErrors = [...errors, ...externalValidationErrors];
  // always reset validation errors even when there is no validator
  return { ...control, validationErrors };
}

/**
 * Clear control values that are no longer in the `choices` list.
 */
function handleMissingChoice<T = ControlType>(control: ControlState<T>) {
  // If the value is not valid anymore based on choices, clear it
  if (
    control.type === 'SelectControl' &&
    !control.freeForm &&
    control.choices &&
    control.value
  ) {
    const alteredControl = { ...control };
    const choices = control.choices as [JsonValue, ReactNode][];
    const value = ensureIsArray(control.value);
    const choiceValues = choices.map(c => c[0]);
    if (control.multi && value.length > 0) {
      alteredControl.value = value.filter(el => choiceValues.includes(el));
      return alteredControl;
    }
    if (!control.multi && !choiceValues.includes(value[0])) {
      alteredControl.value = null;
      return alteredControl;
    }
  }
  return control;
}

/**
 * 应用状态到属性的映射到控件。
 *
 * @param controlState
 * @param controlPanelState
 */
export function applyMapStateToPropsToControl<T = ControlType>(
  controlState: ControlState<T>,
  controlPanelState: Partial<ControlPanelState>,
) {
  const { mapStateToProps } = controlState;
  let state = { ...controlState };
  let { value } = state; // value is current user-input value
  if (mapStateToProps && controlPanelState) {
    state = {
      ...controlState,
      ...mapStateToProps.call(controlState, controlPanelState, controlState),
    };
    // `mapStateToProps` may also provide a value
    value = value || state.value;
  }
  // If default is a function, evaluate it
  if (typeof state.default === 'function') {
    state.default = state.default(state, controlPanelState);
    // if default is still a function, discard
    if (typeof state.default === 'function') {
      delete state.default;
    }
  }
  // If no current value, set it as default
  if (state.default && value === undefined) {
    value = state.default;
  }
  // If a choice control went from multi=false to true, wrap value in array
  if (value && state.multi && !Array.isArray(value)) {
    value = [value];
  }
  state.value = value;
  return execControlValidator(handleMissingChoice(state), state);
}

/**
 * 从控件配置获取控件状态。
 *
 * @param controlConfig 控件配置。
 * @param controlPanelState 控制面板状态。
 * @param value 值。
 */
export function getControlStateFromControlConfig<T = ControlType>(
  controlConfig: ControlConfig<T> | null,
  controlPanelState: Partial<ControlPanelState>,
  value?: JsonValue,
) {
  // skip invalid config values
  if (!controlConfig) {
    return null;
  }
  const controlState = { ...controlConfig, value } as ControlState<T>;
  // only apply mapStateToProps when control states have been initialized
  // or when explicitly didn't provide control panel state (mostly for testing)
  if (
    (controlPanelState && controlPanelState.controls) ||
    controlPanelState === null
  ) {
    return applyMapStateToPropsToControl(controlState, controlPanelState);
  }
  return controlState;
}

/**
 * 获取控件的状态。
 *
 * @param controlKey 控件名称
 * @param vizType 可视类型
 * @param state 状态
 * @param value 值
 */
export function getControlState(
  controlKey: string,
  vizType: string,
  state: Partial<ControlPanelState>,
  value?: JsonValue,
) {
  return getControlStateFromControlConfig(
    getControlConfig(controlKey, vizType),
    state,
    value,
  );
}

/**
 * 获取所有控件状态。
 *
 * @param vizType 可视类型
 * @param datasourceType 数据源类型
 * @param state 状态
 * @param formData 表单数据
 */
export function getAllControlsState(
  vizType: string,
  datasourceType: DatasourceType,
  state: ControlPanelState,
  formData: QueryFormData,
) {
  const controlsState = {};
  getSectionsToRender(vizType, datasourceType).forEach(section =>
    section.controlSetRows.forEach(fieldsetRow =>
      fieldsetRow.forEach(field => {
        if (field && 'config' in field && field.config && field.name) {
          const { config, name } = field;
          controlsState[name] = getControlStateFromControlConfig(
            config,
            state,
            formData[name],
          );
        }
      }),
    ),
  );
  return controlsState;
}
