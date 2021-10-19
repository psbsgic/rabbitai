import React from 'react';
import { render, screen, fireEvent } from 'spec/helpers/testing-library';
import { DndItemType } from 'src/explore/components/DndItemType';
import OptionWrapper from 'src/explore/components/controls/DndColumnSelectControl/OptionWrapper';

test('renders with default props', () => {
  const { container } = render(
    <OptionWrapper
      index={1}
      clickClose={jest.fn()}
      type={'Column' as DndItemType}
      onShiftOptions={jest.fn()}
    >
      Option
    </OptionWrapper>,
    { useDnd: true },
  );
  expect(container).toBeInTheDocument();
  expect(screen.getByRole('img', { name: 'x-small' })).toBeInTheDocument();
});

test('triggers onShiftOptions on drop', () => {
  const onShiftOptions = jest.fn();
  render(
    <>
      <OptionWrapper
        index={1}
        clickClose={jest.fn()}
        type={'Column' as DndItemType}
        onShiftOptions={onShiftOptions}
      >
        Option 1
      </OptionWrapper>
      <OptionWrapper
        index={2}
        clickClose={jest.fn()}
        type={'Column' as DndItemType}
        onShiftOptions={onShiftOptions}
      >
        Option 2
      </OptionWrapper>
    </>,
    { useDnd: true },
  );

  fireEvent.dragStart(screen.getByText('Option 1'));
  fireEvent.drop(screen.getByText('Option 2'));
  expect(onShiftOptions).toHaveBeenCalled();
});
