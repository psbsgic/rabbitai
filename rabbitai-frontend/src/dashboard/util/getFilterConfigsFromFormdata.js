
/* eslint-disable camelcase */
import {
  FILTER_CONFIG_ATTRIBUTES,
  TIME_FILTER_LABELS,
  TIME_FILTER_MAP,
} from 'src/explore/constants';

export default function getFilterConfigsFromFormdata(form_data = {}) {
  const {
    date_filter,
    filter_configs = [],
    show_druid_time_granularity,
    show_druid_time_origin,
    show_sqla_time_column,
    show_sqla_time_granularity,
  } = form_data;
  let configs = filter_configs.reduce(
    ({ columns, labels }, config) => {
      let defaultValues = config[FILTER_CONFIG_ATTRIBUTES.DEFAULT_VALUE];

      // treat empty string as null (no default value)
      if (defaultValues === '') {
        defaultValues = null;
      }

      // defaultValue could be ; separated values,
      // could be null or ''
      if (defaultValues && config[FILTER_CONFIG_ATTRIBUTES.MULTIPLE]) {
        defaultValues = config.defaultValue.split(';');
      }

      const updatedColumns = {
        ...columns,
        [config.column]: config.vals || defaultValues,
      };
      const updatedLabels = {
        ...labels,
        [config.column]: config.label,
      };

      return {
        columns: updatedColumns,
        labels: updatedLabels,
      };
    },
    { columns: {}, labels: {} },
  );

  if (date_filter) {
    let updatedColumns = {
      ...configs.columns,
      [TIME_FILTER_MAP.time_range]: form_data.time_range,
    };
    const updatedLabels = {
      ...configs.labels,
      ...Object.entries(TIME_FILTER_MAP).reduce(
        (map, [key, value]) => ({
          ...map,
          [value]: TIME_FILTER_LABELS[key],
        }),
        {},
      ),
    };

    if (show_sqla_time_granularity) {
      updatedColumns = {
        ...updatedColumns,
        [TIME_FILTER_MAP.time_grain_sqla]: form_data.time_grain_sqla,
      };
    }

    if (show_sqla_time_column) {
      updatedColumns = {
        ...updatedColumns,
        [TIME_FILTER_MAP.granularity_sqla]: form_data.granularity_sqla,
      };
    }

    if (show_druid_time_granularity) {
      updatedColumns = {
        ...updatedColumns,
        [TIME_FILTER_MAP.granularity]: form_data.granularity,
      };
    }

    if (show_druid_time_origin) {
      updatedColumns = {
        ...updatedColumns,
        [TIME_FILTER_MAP.druid_time_origin]: form_data.druid_time_origin,
      };
    }

    configs = {
      ...configs,
      columns: updatedColumns,
      labels: updatedLabels,
    };
  }
  return configs;
}
