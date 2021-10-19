import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import IconButton from 'src/components/IconButton';

const defaultProps = {
  buttonText: 'This is the IconButton text',
  icon: '/images/icons/sql.svg',
};

describe('IconButton', () => {
  it('renders an IconButton', () => {
    render(<IconButton {...defaultProps} />);

    const icon = screen.getByRole('img');
    const buttonText = screen.getByText(/this is the iconbutton text/i);

    expect(icon).toBeVisible();
    expect(buttonText).toBeVisible();
  });
});
