
import React, {
  useRef,
  useEffect,
  Component,
  FunctionComponent,
  ReactElement,
  RefObject,
} from 'react';
import {
  ListChildComponentProps,
  FixedSizeList as WindowedList,
} from 'react-window';
import {
  OptionTypeBase,
  OptionProps,
  MenuListComponentProps,
} from 'react-select';
import { ThemeConfig } from '../styles';

export type WindowedMenuListProps = {
  selectProps: {
    windowListRef?: RefObject<WindowedList>;
    optionHeight?: number;
  };
};

/**
 * MenuListComponentProps should always have `children` elements, as guaranteed
 * by https://github.com/JedWatson/react-select/blob/32ad5c040bdd96cd1ca71010c2558842d684629c/packages/react-select/src/Select.js#L1686-L1719
 *
 * `children` may also be `Component<NoticeProps<OptionType>>` if options are not
 * provided (e.g., when async list is still loading, or no results), but that's
 * not possible because this MenuList will only be rendered when
 * optionsLength > windowThreshold.
 *
 * If may also be `Component<GroupProps<OptionType>>[]` but we are not supporting
 * grouped options just yet.
 */

type MenuListPropsChildren<OptionType> =
  | Component<OptionProps<OptionType>>[]
  | ReactElement[];

export type MenuListProps<
  OptionType extends OptionTypeBase
> = MenuListComponentProps<OptionType> & {
  children: MenuListPropsChildren<OptionType>;
  // theme is not present with built-in @types/react-select, but is actually
  // available via CommonProps.
  theme?: ThemeConfig;
  className?: string;
} & WindowedMenuListProps;

const DEFAULT_OPTION_HEIGHT = 30;

/**
 * Get the index of the last selected option.
 */
function getLastSelected(children: MenuListPropsChildren<any>) {
  return Array.isArray(children)
    ? children.findIndex(
        ({ props: { isFocused = false } = {} }) => isFocused,
      ) || 0
    : -1;
}

/**
 * Calculate probable option height as set in theme configs
 */
function detectHeight({ spacing: { baseUnit, lineHeight } }: ThemeConfig) {
  // Option item expects 2 * baseUnit for each of top and bottom padding.
  return baseUnit * 4 + lineHeight;
}

export default function WindowedMenuList<OptionType extends OptionTypeBase>({
  children,
  ...props
}: MenuListProps<OptionType>) {
  const {
    maxHeight,
    selectProps,
    theme,
    getStyles,
    cx,
    innerRef,
    isMulti,
    className,
  } = props;
  const {
    // Expose react-window VariableSizeList instance and HTML elements
    windowListRef: windowListRef_,
    windowListInnerRef,
  } = selectProps;
  const defaultWindowListRef = useRef<WindowedList>(null);
  const windowListRef = windowListRef_ || defaultWindowListRef;

  // try get default option height from theme configs
  let { optionHeight } = selectProps;
  if (!optionHeight) {
    optionHeight = theme ? detectHeight(theme) : DEFAULT_OPTION_HEIGHT;
  }

  const itemCount = children.length;
  const totalHeight = optionHeight * itemCount;

  const Row: FunctionComponent<ListChildComponentProps> = ({
    data,
    index,
    style,
  }) => <div style={style}>{data[index]}</div>;

  useEffect(() => {
    const lastSelected = getLastSelected(children);
    if (windowListRef.current && lastSelected) {
      windowListRef.current.scrollToItem(lastSelected);
    }
  }, [children, windowListRef]);

  return (
    <WindowedList
      css={getStyles('menuList', props)}
      className={cx(
        {
          'menu-list': true,
          'menu-list--is-multi': isMulti,
        },
        className,
      )}
      ref={windowListRef}
      outerRef={innerRef}
      innerRef={windowListInnerRef}
      height={Math.min(totalHeight, maxHeight)}
      width="100%"
      itemData={children}
      itemCount={children.length}
      itemSize={optionHeight}
    >
      {Row}
    </WindowedList>
  );
}
