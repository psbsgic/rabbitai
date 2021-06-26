

import React from 'react';
import { styled } from '@rabbitai-ui/core';
import cls from 'classnames';

export type PositionOption =
  | 'floating'
  | 'inline'
  | 'inline-centered'
  | 'normal';
export interface Props {
  position?: PositionOption;
  className?: string;
  image?: string;
}

const LoaderImg = styled.img`
  z-index: 99;
  width: 50px;
  position: relative;
  margin: 10px;
  &.inline {
    margin: 0px;
    width: 30px;
  }
  &.inline-centered {
    margin: 0 auto;
    width: 30px;
    display: block;
  }
  &.floating {
    padding: 0;
    margin: 0;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
`;
export default function Loading({
  position = 'floating',
  image = '/static/assets/images/loading.gif',
  className,
}: Props) {
  return (
    <LoaderImg
      className={cls('loading', position, className)}
      alt="Loading..."
      src={image}
      role="status"
      aria-live="polite"
      aria-label="Loading"
    />
  );
}
