import { throttle } from 'lodash';
import { DASHBOARD_ROOT_TYPE } from 'src/dashboard/util/componentTypes';
import getDropPosition from 'src/dashboard/util/getDropPosition';
import handleScroll from './handleScroll';

const HOVER_THROTTLE_MS = 100;

function handleHover(props, monitor, Component) {
  // this may happen due to throttling
  if (!Component.mounted) return;

  const dropPosition = getDropPosition(monitor, Component);

  const isDashboardRoot =
    Component?.props?.component?.type === DASHBOARD_ROOT_TYPE;
  const scroll = isDashboardRoot ? 'SCROLL_TOP' : null;

  handleScroll(scroll);

  if (!dropPosition) {
    Component.setState(() => ({ dropIndicator: null }));
    return;
  }

  Component.setState(() => ({
    dropIndicator: dropPosition,
  }));
}

// this is called very frequently by react-dnd
export default throttle(handleHover, HOVER_THROTTLE_MS);
