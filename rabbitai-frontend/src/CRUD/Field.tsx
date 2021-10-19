import React, { useCallback } from 'react';
import { css, SupersetTheme } from '@superset-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import { FormItem, FormLabel } from 'src/components/Form';
import './crud.less';

const formItemInlineCss = css`
  .ant-form-item-control-input-content {
    display: flex;
    flex-direction: row;
  }
`;

interface FieldProps<V> {
  fieldKey: string;
  value?: V;
  label: string;
  description?: React.ReactNode;
  control: React.ReactElement;
  onChange: (fieldKey: string, newValue: V) => void;
  compact: boolean;
  inline: boolean;
}

export default function Field<V>({
  fieldKey,
  value,
  label,
  description,
  control,
  onChange,
  compact,
  inline,
}: FieldProps<V>) {
  const onControlChange = useCallback(
    newValue => {
      onChange(fieldKey, newValue);
    },
    [onChange, fieldKey],
  );

  const hookedControl = React.cloneElement(control, {
    value,
    onChange: onControlChange,
  });
  return (
    <FormItem
      label={
        <FormLabel className="m-r-5">
          {label || fieldKey}
          {compact && description && (
            <Tooltip id="field-descr" placement="right" title={description}>
              <i className="fa fa-info-circle m-l-5" />
            </Tooltip>
          )}
        </FormLabel>
      }
      css={inline && formItemInlineCss}
    >
      {hookedControl}
      {!compact && description && (
        <div
          css={(theme: SupersetTheme) => ({
            color: theme.colors.grayscale.base,
            [inline ? 'marginLeft' : 'marginTop']: theme.gridUnit,
          })}
        >
          {description}
        </div>
      )}
    </FormItem>
  );
}
