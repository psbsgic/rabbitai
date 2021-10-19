import React from 'react';
import * as AntdIcons from '@ant-design/icons/lib/icons';
import { StyledIcon } from './Icon';
import IconType from './IconType';

const AntdEnhancedIcons = Object.keys(AntdIcons)
  .map(k => ({
    [k]: (props: IconType) => (
      <StyledIcon component={AntdIcons[k]} {...props} />
    ),
  }))
  .reduce((l, r) => ({ ...l, ...r }));

export default AntdEnhancedIcons;
