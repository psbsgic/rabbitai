
import React from 'react';
import AntDSlider, {
  SliderSingleProps,
  SliderRangeProps,
} from 'antd/lib/slider';

export { SliderSingleProps, SliderRangeProps };

export default function Slider(props: SliderSingleProps | SliderRangeProps) {
  return <AntDSlider {...props} css={{ marginLeft: 0, marginRight: 0 }} />;
}
