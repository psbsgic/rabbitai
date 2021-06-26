
import { styled } from '@rabbitai-ui/core';
import React from 'react';
import Icon from 'src/components/Icon';

export interface SearchInputProps {
  onSubmit: () => void;
  onClear: () => void;
  value: string;
  onChange: React.EventHandler<React.ChangeEvent<HTMLInputElement>>;
  placeholder?: string;
  name?: string;
}

const SearchInputWrapper = styled.div`
  position: relative;
`;

const StyledInput = styled.input`
  width: 200px;
  height: ${({ theme }) => theme.gridUnit * 8}px;
  background-image: none;
  border: 1px solid ${({ theme }) => theme.colors.secondary.light2};
  border-radius: 4px;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  padding: 4px 28px;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  &:focus {
    outline: none;
  }
`;

const commonStyles = `
  position: absolute;
  z-index: 2;
  display: block;
  cursor: pointer;
`;
const SearchIcon = styled(Icon)`
  ${commonStyles};
  top: 4px;
  left: 2px;
`;

const ClearIcon = styled(Icon)`
  ${commonStyles};
  right: 0px;
  top: 4px;
`;

export default function SearchInput({
  onChange,
  onClear,
  onSubmit,
  placeholder = 'Search',
  name,
  value,
}: SearchInputProps) {
  return (
    <SearchInputWrapper>
      <SearchIcon
        data-test="search-submit"
        role="button"
        name="search"
        onClick={() => onSubmit()}
      />
      <StyledInput
        data-test="search-input"
        onKeyDown={e => {
          if (e.key === 'Enter') {
            onSubmit();
          }
        }}
        onBlur={() => onSubmit()}
        placeholder={placeholder}
        onChange={onChange}
        value={value}
        name={name}
      />
      {value && (
        <ClearIcon
          data-test="search-clear"
          role="button"
          name="cancel-x"
          onClick={() => onClear()}
        />
      )}
    </SearchInputWrapper>
  );
}
