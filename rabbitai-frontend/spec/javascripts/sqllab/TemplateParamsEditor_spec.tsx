import React, { ReactNode } from 'react';
import {
  render,
  fireEvent,
  getByText,
  waitFor,
} from 'spec/helpers/testing-library';
import brace from 'brace';
import { ThemeProvider, supersetTheme } from '@superset-ui/core';

import TemplateParamsEditor from 'src/SqlLab/components/TemplateParamsEditor';

const ThemeWrapper = ({ children }: { children: ReactNode }) => (
  <ThemeProvider theme={supersetTheme}>{children}</ThemeProvider>
);

describe('TemplateParamsEditor', () => {
  it('should render with a title', () => {
    const { container } = render(
      <TemplateParamsEditor code="FOO" language="json" onChange={() => {}} />,
      { wrapper: ThemeWrapper },
    );
    expect(container.querySelector('div[role="button"]')).toBeInTheDocument();
  });

  it('should open a modal with the ace editor', async () => {
    const { container, baseElement } = render(
      <TemplateParamsEditor code="FOO" language="json" onChange={() => {}} />,
      { wrapper: ThemeWrapper },
    );
    fireEvent.click(getByText(container, 'Parameters'));
    const spy = jest.spyOn(brace, 'acequire');
    spy.mockReturnValue({ setCompleters: () => 'foo' });
    await waitFor(() => {
      expect(baseElement.querySelector('#brace-editor')).toBeInTheDocument();
    });
  });
});
