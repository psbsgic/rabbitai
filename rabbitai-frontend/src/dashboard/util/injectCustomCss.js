
export default function injectCustomCss(css) {
  const className = 'CssEditor-css';
  const head = document.head || document.getElementsByTagName('head')[0];
  let style = document.querySelector(`.${className}`);

  if (!style) {
    style = document.createElement('style');
    style.className = className;
    style.type = 'text/css';
  }

  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    style.innerHTML = css;
  }

  /**
   * Ensures that the style applied is always the last.
   *
   * from: https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild
   * The Node.appendChild() method adds a node to the end of the list of children
   * of a specified parent node. If the given child is a reference to an existing
   * node in the document, appendChild() moves it from its current position to the
   * new position (there is no requirement to remove the node from its parent node
   * before appending it to some other node).
   */

  head.appendChild(style);
}
