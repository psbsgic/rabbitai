import { styled, useTheme } from '@superset-ui/core';
import React from 'react';
import Icons from 'src/components/Icons';

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
const SearchIcon = styled(Icons.Search)`
  ${commonStyles};
  top: 4px;
  left: 2px;
`;

const ClearIcon = styled(Icons.CancelX)`
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
  const theme = useTheme();
  return (
    <SearchInputWrapper>
      <SearchIcon
        iconColor={theme.colors.grayscale.base}
        data-test="search-submit"
        role="button"
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
          iconColor={theme.colors.grayscale.base}
          onClick={() => onClear()}
        />
      )}
    </SearchInputWrapper>
  );
}
