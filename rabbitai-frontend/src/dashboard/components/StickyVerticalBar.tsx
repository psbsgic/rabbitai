

import React from 'react';
import { StickyContainer, Sticky } from 'react-sticky';
import { styled } from '@rabbitai-ui/core';
import cx from 'classnames';

const Wrapper = styled.div`
  position: relative;
  width: ${({ theme }) => theme.gridUnit * 8}px;
  flex: 0 0 ${({ theme }) => theme.gridUnit * 8}px;
  /* these animations (which can be enabled with the "animated" class) look glitchy due to chart resizing */
  /* keeping these for posterity, in case we can improve that resizing performance */
  /* &.animated {
    transition: width 0;
    transition-delay: ${({ theme }) => theme.transitionTiming * 2}s;
  } */
  &.open {
    width: 250px;
    flex: 0 0 250px;
    /* &.animated {
      transition-delay: 0s;
    } */
  }
`;

const Contents = styled.div`
  display: grid;
  position: absolute;
  overflow: auto;
  height: 100%;
`;

export interface SVBProps {
  topOffset: number;
  width?: number;
  filtersOpen: boolean;
}

/**
 * A vertical sidebar that uses sticky position to stay
 * fixed on the page after the sitenav is scrolled out of the viewport.
 *
 * TODO use css position: sticky when sufficiently supported
 * (should have better performance)
 */
export const StickyVerticalBar: React.FC<SVBProps> = ({
  topOffset,
  children,
  filtersOpen,
}) => (
  <Wrapper className={cx({ open: filtersOpen })}>
    <StickyContainer>
      <Sticky topOffset={-topOffset} bottomOffset={Infinity}>
        {({
          style,
          isSticky,
          distanceFromTop,
        }: {
          style: any;
          isSticky: boolean;
          distanceFromTop: number;
        }) => (
          <Contents
            style={
              isSticky
                ? {
                    ...style,
                    top: topOffset,
                    height: `calc(100vh - ${topOffset}px)`,
                  }
                : {
                    height: `calc(100vh - ${distanceFromTop}px)`,
                  }
            }
          >
            {children}
          </Contents>
        )}
      </Sticky>
    </StickyContainer>
  </Wrapper>
);
