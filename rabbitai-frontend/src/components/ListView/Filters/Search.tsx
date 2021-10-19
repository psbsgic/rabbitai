import React, { useState } from 'react';
import SearchInput from 'src/components/SearchInput';
import { FilterContainer, BaseFilter } from './Base';

interface SearchHeaderProps extends BaseFilter {
  Header: string;
  onSubmit: (val: string) => void;
  name: string;
}

export default function SearchFilter({
  Header,
  name,
  initialValue,
  onSubmit,
}: SearchHeaderProps) {
  const [value, setValue] = useState(initialValue || '');
  const handleSubmit = () => {
    if (value) {
      onSubmit(value.trim());
    }
  };
  const onClear = () => {
    setValue('');
    onSubmit('');
  };
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.currentTarget.value);
    if (e.currentTarget.value === '') {
      onClear();
    }
  };

  return (
    <FilterContainer>
      <SearchInput
        data-test="filters-search"
        placeholder={Header}
        name={name}
        value={value}
        onChange={handleChange}
        onSubmit={handleSubmit}
        onClear={onClear}
      />
    </FilterContainer>
  );
}
