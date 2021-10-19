import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { Omnibar } from './Omnibar';

test('Must put id on input', () => {
  render(
    <Omnibar
      id="test-id-attribute"
      placeholder="Test Omnibar"
      extensions={[jest.fn().mockResolvedValue([{ title: 'test' }])]}
    />,
  );

  expect(screen.getByPlaceholderText('Test Omnibar')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Test Omnibar')).toHaveAttribute(
    'id',
    'test-id-attribute',
  );
});
