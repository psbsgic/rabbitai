import React, { ComponentType, FunctionComponent, ReactElement } from 'react';
import Select, {
  Props as SelectProps,
  OptionTypeBase,
  MenuListComponentProps,
  components as defaultComponents,
} from 'react-select';
import WindowedMenuList, { WindowedMenuListProps } from './WindowedMenuList';

const { MenuList: DefaultMenuList } = defaultComponents;

export const DEFAULT_WINDOW_THRESHOLD = 100;

export type WindowedSelectProps<
  OptionType extends OptionTypeBase
> = SelectProps<OptionType> & {
  windowThreshold?: number;
} & WindowedMenuListProps['selectProps'];

export type WindowedSelectComponentType<
  OptionType extends OptionTypeBase
> = FunctionComponent<WindowedSelectProps<OptionType>>;

export function MenuList<OptionType extends OptionTypeBase>({
  children,
  ...props
}: MenuListComponentProps<OptionType> & {
  selectProps: WindowedSelectProps<OptionType>;
}) {
  const { windowThreshold = DEFAULT_WINDOW_THRESHOLD } = props.selectProps;
  if (Array.isArray(children) && children.length > windowThreshold) {
    return (
      <WindowedMenuList {...props}>
        {children as ReactElement[]}
      </WindowedMenuList>
    );
  }
  return <DefaultMenuList {...props}>{children}</DefaultMenuList>;
}

/**
 * Add "windowThreshold" option to a react-select component, turn the options
 * list into a virtualized list when appropriate.
 *
 * @param SelectComponent the React component to render Select
 */
export default function windowed<OptionType extends OptionTypeBase>(
  SelectComponent: ComponentType<SelectProps<OptionType>>,
): WindowedSelectComponentType<OptionType> {
  function WindowedSelect(
    props: WindowedSelectProps<OptionType>,
    ref: React.RefObject<Select<OptionType>>,
  ) {
    const { components: components_ = {}, ...restProps } = props;
    const components = { ...components_, MenuList };
    return <SelectComponent components={components} ref={ref} {...restProps} />;
  }
  return React.forwardRef(WindowedSelect);
}
