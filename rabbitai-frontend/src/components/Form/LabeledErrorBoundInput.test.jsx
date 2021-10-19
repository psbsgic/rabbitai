import React from 'react';
import { render, fireEvent, screen } from 'spec/helpers/testing-library';
import LabeledErrorBoundInput from 'src/components/Form/LabeledErrorBoundInput';

const defaultProps = {
  id: 1,
  label: 'Username',
  name: 'Username',
  validationMethods: () => {},
  errorMessage: '',
  helpText: 'This is a line of example help text',
  hasTooltip: false,
  tooltipText: 'This is a tooltip',
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
  it('renders a LabledErrorBoundInput with a InfoTooltip', async () => {
    defaultProps.hasTooltip = true;
    render(<LabeledErrorBoundInput {...defaultProps} />);

    const label = screen.getByText(/username/i);
    const textboxInput = screen.getByRole('textbox');
    const tooltipIcon = screen.getByRole('img');

    fireEvent.mouseOver(tooltipIcon);

    expect(tooltipIcon).toBeVisible();
    expect(label).toBeVisible();
    expect(textboxInput).toBeVisible();
    expect(await screen.findByText('This is a tooltip')).toBeInTheDocument();
  });
});
