
import { IN_COMPONENT_ELEMENT_TYPES } from './constants';

export default function getLeafComponentIdFromPath(directPathToChild = []) {
  if (directPathToChild.length > 0) {
    const currentPath = directPathToChild.slice();

    while (currentPath.length) {
      const componentId = currentPath.pop();
      const componentType = componentId.split('-')[0];

      if (!IN_COMPONENT_ELEMENT_TYPES.includes(componentType)) {
        return componentId;
      }
    }
  }

  return null;
}
