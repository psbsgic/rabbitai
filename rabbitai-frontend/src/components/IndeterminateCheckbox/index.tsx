import React from 'react';
import { styled } from '@superset-ui/core';
import Icons from 'src/components/Icons';

export interface IndeterminateCheckboxProps {
  indeterminate: boolean;
  id: string;
  checked: boolean;
  onChange: React.EventHandler<React.SyntheticEvent<HTMLInputElement>>;
  title?: string;
  labelText?: string;
}

const CheckboxLabel = styled.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`;

const CheckboxHalf = styled(Icons.CheckboxHalf)`
  color: ${({ theme }) => theme.colors.primary.base};
  cursor: pointer;
`;

const CheckboxOff = styled(Icons.CheckboxOff)`
  color: ${({ theme }) => theme.colors.grayscale.base};
  cursor: pointer;
`;

const CheckboxOn = styled(Icons.CheckboxOn)`
  color: ${({ theme }) => theme.colors.primary.base};
  cursor: pointer;
`;

const HiddenInput = styled.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`;

const InputContainer = styled.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`;

const IndeterminateCheckbox = React.forwardRef(
  (
    {
      indeterminate,
      id,
      checked,
      onChange,
      title = '',
      labelText = '',
    }: IndeterminateCheckboxProps,
    ref: React.MutableRefObject<any>,
  ) => {
    const defaultRef = React.useRef<HTMLInputElement>();
    const resolvedRef = ref || defaultRef;

    React.useEffect(() => {
      resolvedRef.current.indeterminate = indeterminate;
    }, [resolvedRef, indeterminate]);

    return (
      <>
        <InputContainer>
          {indeterminate && <CheckboxHalf />}
          {!indeterminate && checked && <CheckboxOn />}
          {!indeterminate && !checked && <CheckboxOff />}
          <HiddenInput
            name={id}
            id={id}
            type="checkbox"
            ref={resolvedRef}
            checked={checked}
            onChange={onChange}
          />
        </InputContainer>
        <CheckboxLabel title={title} htmlFor={id}>
          {labelText}
        </CheckboxLabel>
      </>
    );
  },
);

export default IndeterminateCheckbox;
