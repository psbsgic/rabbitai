
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import LabeledErrorBoundInput from 'src/components/Form/LabeledErrorBoundInput';

const defaultProps = {
  id: 1,
  label: 'Username',
  name: 'Username',
  validationMethods: () => {},
  errorMessage: '',
  helpText: 'This is a line of example help text',
  value: '',
  placeholder: 'Example placeholder text...',
  type: 'textbox',
};

describe('LabeledErrorBoundInput', () => {
  it('renders a LabeledErrorBoundInput normally, without an error', () => {
    render(<LabeledErrorBoundInput {...defaultProps} />);

    const label = screen.getByText(/username/i);
    const textboxInput = screen.getByRole('textbox');
    const helperText = screen.getByText('This is a line of example help text');

    expect(label).toBeVisible();
    expect(textboxInput).toBeVisible();
    expect(helperText).toBeVisible();
  });

  it('renders a LabeledErrorBoundInput with an error', () => {
    // Pass an error into props, causing errorText to replace helperText
    defaultProps.errorMessage = 'Example error message';
    render(<LabeledErrorBoundInput {...defaultProps} />);

    const label = screen.getByText(/username/i);
    const textboxInput = screen.getByRole('textbox');
    const errorText = screen.getByText(/example error message/i);

    expect(label).toBeVisible();
    expect(textboxInput).toBeVisible();
    expect(errorText).toBeVisible();
  });
});
