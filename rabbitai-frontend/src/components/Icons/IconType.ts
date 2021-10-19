import { IconComponentProps } from '@ant-design/icons/lib/components/Icon';

type AntdIconType = IconComponentProps;
type IconType = AntdIconType & {
  iconColor?: string;
  twoToneColor?: string;
  iconSize?: 's' | 'm' | 'l' | 'xl' | 'xxl';
};

export default IconType;
