import React from 'react';
import { Input } from 'antd';
import { styled, css, SupersetTheme } from '@superset-ui/core';
import InfoTooltip from 'src/components/InfoTooltip';
import errorIcon from 'images/icons/error.svg';
import FormItem from './FormItem';
import FormLabel from './FormLabel';

export interface LabeledErrorBoundInputProps {
  label?: string;
  validationMethods:
    | { onBlur: (value: any) => void }
    | { onChange: (value: any) => void };
  errorMessage: string | null;
  helpText?: string;
  required?: boolean;
  hasTooltip?: boolean;
  tooltipText?: string | null;
  id?: string;
  classname?: string;
  [x: string]: any;
}

const StyledInput = styled(Input)`
  margin: ${({ theme }) => `${theme.gridUnit}px 0 ${theme.gridUnit * 2}px`};
`;

const alertIconStyles = (theme: SupersetTheme, hasError: boolean) => css`
  .ant-form-item-children-icon {
    display: none;
  }
  ${hasError &&
  `.ant-form-item-control-input-content {
      position: relative;
      &:after {
        content: ' ';
        display: inline-block;
        background: ${theme.colors.error.base};
        mask: url(${errorIcon});
        mask-size: cover;
        width: ${theme.gridUnit * 4}px;
        height: ${theme.gridUnit * 4}px;
        position: absolute;
        right: ${theme.gridUnit * 1.25}px;
        top: ${theme.gridUnit * 2.75}px;
      }
    }`}
`;

const StyledFormGroup = styled('div')`
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  margin-bottom: ${({ theme }) => theme.gridUnit * 3}px;
  .ant-form-item {
    margin-bottom: 0;
  }
`;

const StyledAlignment = styled.div`
  display: flex;
  align-items: center;
`;

const StyledFormLabel = styled(FormLabel)`
  margin-bottom: 0;
`;

const LabeledErrorBoundInput = ({
  label,
  validationMethods,
  errorMessage,
  helpText,
  required = false,
  hasTooltip = false,
  tooltipText,
  id,
  className,
  ...props
}: LabeledErrorBoundInputProps) => (
  <StyledFormGroup className={className}>
    <StyledAlignment>
      <StyledFormLabel htmlFor={id} required={required}>
        {label}
      </StyledFormLabel>
      {hasTooltip && (
        <InfoTooltip tooltip={`${tooltipText}`} viewBox="0 -1 24 24" />
      )}
    </StyledAlignment>
    <FormItem
      css={(theme: SupersetTheme) => alertIconStyles(theme, !!errorMessage)}
      validateTrigger={Object.keys(validationMethods)}
      validateStatus={errorMessage ? 'error' : 'success'}
      help={errorMessage || helpText}
      hasFeedback={!!errorMessage}
    >
      <StyledInput {...props} {...validationMethods} />
    </FormItem>
  </StyledFormGroup>
);

export default LabeledErrorBoundInput;
