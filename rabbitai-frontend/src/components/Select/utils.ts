import {
  OptionTypeBase,
  ValueType,
  OptionsType,
  GroupedOptionsType,
} from 'react-select';

import { OptionsType as AntdOptionsType } from './Select';

/**
 * Find Option value that matches a possibly string value.
 *
 * Translate possible string values to `OptionType` objects, fallback to value
 * itself if cannot be found in the options list.
 *
 * Always returns an array.
 */
export function findValue<OptionType extends OptionTypeBase>(
  value: ValueType<OptionType> | string,
  options: GroupedOptionsType<OptionType> | OptionsType<OptionType> = [],
  valueKey = 'value',
): OptionType[] {
  if (value === null || value === undefined || value === '') {
    return [];
  }
  const isGroup = Array.isArray((options[0] || {}).options);
  const flatOptions = isGroup
    ? (options as GroupedOptionsType<OptionType>).flatMap(x => x.options || [])
    : (options as OptionsType<OptionType>);

  const find = (val: OptionType) => {
    const realVal = (value || {}).hasOwnProperty(valueKey)
      ? val[valueKey]
      : val;
    return (
      flatOptions.find(x => x === realVal || x[valueKey] === realVal) || val
    );
  };

  // If value is a single string, must return an Array so `cleanValue` won't be
  // empty: https://github.com/JedWatson/react-select/blob/32ad5c040bdd96cd1ca71010c2558842d684629c/packages/react-select/src/utils.js#L64
  return (Array.isArray(value) ? value : [value]).map(find);
}

export function hasOption(search: string, options: AntdOptionsType) {
  const searchOption = search.trim().toLowerCase();
  return options.find(opt => {
    const { label, value } = opt;
    const labelText = String(label);
    const valueText = String(value);
    return (
      valueText.toLowerCase().includes(searchOption) ||
      labelText.toLowerCase().includes(searchOption)
    );
  });
}
