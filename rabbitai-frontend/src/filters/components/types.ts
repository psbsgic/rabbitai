import { SetDataMaskHook } from '@rabbitai-ui/core';


export interface PluginFilterStylesProps {
  height: number;
  width: number;
}

export interface PluginFilterHooks {
  setDataMask: SetDataMaskHook;
  setFocusedFilter: () => void;
  unsetFocusedFilter: () => void;
}
