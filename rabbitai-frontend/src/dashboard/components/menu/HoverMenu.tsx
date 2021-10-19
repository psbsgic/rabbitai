import React, { RefObject } from 'react';
import cx from 'classnames';

interface HoverMenuProps {
  position: 'left' | 'top';
  innerRef: RefObject<HTMLDivElement>;
  children: React.ReactNode;
}

export default class HoverMenu extends React.PureComponent<HoverMenuProps> {
  static defaultProps = {
    position: 'left',
    innerRef: null,
    children: null,
  };

  render() {
    const { innerRef, position, children } = this.props;
    return (
      <div
        ref={innerRef}
        className={cx(
          'hover-menu',
          position === 'left' && 'hover-menu--left',
          position === 'top' && 'hover-menu--top',
        )}
      >
        {children}
      </div>
    );
  }
}
