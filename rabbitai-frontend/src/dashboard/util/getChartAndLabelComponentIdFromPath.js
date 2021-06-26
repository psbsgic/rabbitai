
import { IN_COMPONENT_ELEMENT_TYPES } from './constants';

export default function getChartAndLabelComponentIdFromPath(directPathToChild) {
  const result = {};

  if (directPathToChild.length > 0) {
    const currentPath = directPathToChild.slice();

    while (currentPath.length) {
      const componentId = currentPath.pop();
      const componentType = componentId.split('-')[0];

      result[componentType.toLowerCase()] = componentId;
      if (!IN_COMPONENT_ELEMENT_TYPES.includes(componentType)) {
        break;
      }
    }
  }

  return result;
}
