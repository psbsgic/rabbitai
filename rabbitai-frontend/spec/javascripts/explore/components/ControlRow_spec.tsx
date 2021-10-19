import React from 'react';
import { render } from 'spec/helpers/testing-library';
import ControlSetRow from 'src/explore/components/ControlRow';

describe('ControlSetRow', () => {
  it('renders a single row with one element', () => {
    const { getAllByText } = render(
      <ControlSetRow controls={[<p>My Control 1</p>]} />,
    );
    expect(getAllByText('My Control 1').length).toBe(1);
  });
  it('renders a single row with two elements', () => {
    const { getAllByText } = render(
      <ControlSetRow controls={[<p>My Control 1</p>, <p>My Control 2</p>]} />,
    );
    expect(getAllByText(/My Control/)).toHaveLength(2);
  });
});
