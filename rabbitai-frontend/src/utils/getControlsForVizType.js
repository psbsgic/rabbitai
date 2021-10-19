import memoize from 'lodash/memoize';
import { getChartControlPanelRegistry } from '@superset-ui/core';
import { controls } from '../explore/controls';

const memoizedControls = memoize((vizType, controlPanel) => {
  const controlsMap = {};
  (controlPanel?.controlPanelSections || []).forEach(section => {
    section.controlSetRows.forEach(row => {
      row.forEach(control => {
        if (!control) return;
        if (typeof control === 'string') {
          // For now, we have to look in controls.jsx to get the config for some controls.
          // Once everything is migrated out, delete this if statement.
          controlsMap[control] = controls[control];
        } else if (control.name && control.config) {
          // condition needed because there are elements, e.g. <hr /> in some control configs (I'm looking at you, FilterBox!)
          controlsMap[control.name] = control.config;
        }
      });
    });
  });
  return controlsMap;
});

const getControlsForVizType = vizType => {
  const controlPanel = getChartControlPanelRegistry().get(vizType);
  return memoizedControls(vizType, controlPanel);
};

export default getControlsForVizType;
