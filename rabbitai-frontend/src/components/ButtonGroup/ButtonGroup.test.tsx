import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import Button from 'src/components/Button';
import ButtonGroup from '.';

test('renders 1 button', () => {
  render(
    <ButtonGroup>
      <Button>Button</Button>
    </ButtonGroup>,
  );
  expect(screen.getByRole('group')).toBeInTheDocument();
});

test('renders 3 buttons', () => {
  render(
    <ButtonGroup>
      <Button>Button</Button>
      <Button>Button</Button>
      <Button>Button</Button>
    </ButtonGroup>,
  );

  expect(screen.getByRole('group').children.length).toEqual(3);
});

test('renders with custom class', () => {
  const customClass = 'custom-class';
  render(
    <ButtonGroup className={customClass}>
      <Button>Button</Button>
    </ButtonGroup>,
  );

  expect(screen.getByRole('group')).toHaveClass(customClass);
});
