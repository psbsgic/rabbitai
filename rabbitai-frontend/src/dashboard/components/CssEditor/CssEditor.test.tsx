
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import { CssEditor as AceCssEditor } from 'src/components/AsyncAceEditor';
import { AceEditorProps } from 'react-ace';
import userEvent from '@testing-library/user-event';
import CssEditor from '.';

jest.mock('src/components/AsyncAceEditor', () => ({
  CssEditor: ({ value, onChange }: AceEditorProps) => (
    <textarea
      defaultValue={value}
      onChange={value => onChange?.(value.target.value)}
    />
  ),
}));

AceCssEditor.preload = () => new Promise(() => {});

test('renders with default props', () => {
  render(<CssEditor triggerNode={<>Click</>} />);
  expect(screen.getByRole('button', { name: 'Click' })).toBeInTheDocument();
});

test('renders with initial CSS', () => {
  const initialCss = 'margin: 10px;';
  render(<CssEditor triggerNode={<>Click</>} initialCss={initialCss} />);
  userEvent.click(screen.getByRole('button', { name: 'Click' }));
  expect(screen.getByText(initialCss)).toBeInTheDocument();
});

test('renders with templates', () => {
  const templates = ['Template A', 'Template B', 'Template C'];
  render(<CssEditor triggerNode={<>Click</>} templates={templates} />);
  userEvent.click(screen.getByRole('button', { name: 'Click' }));
  userEvent.click(screen.getByText('Load a CSS template'));
  templates.forEach(template =>
    expect(screen.getByText(template)).toBeInTheDocument(),
  );
});

test('triggers onChange when using the editor', () => {
  const onChange = jest.fn();
  const initialCss = 'margin: 10px;';
  const additionalCss = 'color: red;';
  render(
    <CssEditor
      triggerNode={<>Click</>}
      initialCss={initialCss}
      onChange={onChange}
    />,
  );
  userEvent.click(screen.getByRole('button', { name: 'Click' }));
  expect(onChange).not.toHaveBeenCalled();
  userEvent.type(screen.getByText(initialCss), additionalCss);
  expect(onChange).toHaveBeenLastCalledWith(initialCss.concat(additionalCss));
});

test('triggers onChange when selecting a template', () => {
  const onChange = jest.fn();
  const templates = ['Template A', 'Template B', 'Template C'];
  render(
    <CssEditor
      triggerNode={<>Click</>}
      templates={templates}
      onChange={onChange}
    />,
  );
  userEvent.click(screen.getByRole('button', { name: 'Click' }));
  userEvent.click(screen.getByText('Load a CSS template'));
  expect(onChange).not.toHaveBeenCalled();
  userEvent.click(screen.getByText('Template A'));
  expect(onChange).toHaveBeenCalledTimes(1);
});
